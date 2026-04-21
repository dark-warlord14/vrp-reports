# Security: heap-use-after-free on components/global_media_controls/public/views/media_item_ui_list_view.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40059272](https://issues.chromium.org/issues/40059272) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>UI |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2022-04-01 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36

Steps to reproduce the problem:
Repro's on chromeOS and Lacros. This issue similar with bug #1312366 but with different stack trace, so I filled the new report.

1. Run python3 http.server and load poc2.html
2. Another terminal run: out/Default/chrome --user-data-dir=/tmp/chromeos http://localhost:8000/poc2.html --ash-debug-shortcuts --ash-dev-shortcuts --ash-host-window-bounds=1000x1000,950+0-1000x1000
3. Click display two and click pip
4. Detach second display

What is the expected behavior?
not crash

What went wrong?
=================================================================
==104994==ERROR: AddressSanitizer: heap-use-after-free on address 0x619000a59050 at pc 0x7f0828910400 bp 0x7ffd95eb6ab0 sp 0x7ffd95eb6aa8
READ of size 8 at 0x619000a59050 thread T0 (chrome)
    #0 0x7f08289103ff in __root buildtools/third_party/libc++/trunk/include/__tree:1079:59
    #1 0x7f08289103ff in std::__Cr::__tree_const_iterator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const, global_media_controls::MediaItemUIView*>, std::__Cr::__tree_node<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const, global_media_controls::MediaItemUIView*>, void*>*, long> std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const, global_media_controls::MediaItemUIView*>, std::__Cr::__map_value_compare<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const, std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const, global_media_controls::MediaItemUIView*>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const>, true>, std::__Cr::allocator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const, global_media_controls::MediaItemUIView*> > >::find<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&) const buildtools/third_party/libc++/trunk/include/__tree:2477:45
    #2 0x7f082890fc95 in find buildtools/third_party/libc++/trunk/include/map:1393:68
    #3 0x7f082890fc95 in ContainsImpl<std::__Cr::map<const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, global_media_controls::MediaItemUIView *, std::__Cr::less<const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >, std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, global_media_controls::MediaItemUIView *> > >, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > > base/containers/contains.h:46:20
    #4 0x7f082890fc95 in Contains<std::__Cr::map<const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, global_media_controls::MediaItemUIView *, std::__Cr::less<const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >, std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, global_media_controls::MediaItemUIView *> > >, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > > base/containers/contains.h:82:10
    #5 0x7f082890fc95 in global_media_controls::MediaItemUIListView::HideItem(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&) components/global_media_controls/public/views/media_item_ui_list_view.cc:86:8
    #6 0x7f084bfef932 in ash::MediaNotificationProviderImpl::HideMediaItem(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&) ash/system/media/media_notification_provider_impl.cc:140:25
    #7 0x7f0828903395 in global_media_controls::MediaSessionItemProducer::RemoveItem(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&) components/global_media_controls/public/media_session_item_producer.cc:387:18
    #8 0x7f0828902984 in global_media_controls::MediaSessionItemProducer::OnRequestIdReleased(base::UnguessableToken const&) components/global_media_controls/public/media_session_item_producer.cc:324:3
    #9 0x7f08289188cd in media_session::mojom::AudioFocusObserverStubDispatch::Accept(media_session::mojom::AudioFocusObserver*, mojo::Message*) gen/services/media_session/public/mojom/audio_focus.mojom.cc:415:13
    #10 0x7f085d4499ec in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:922:54
    #11 0x7f085d458e3f in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #12 0x7f085d44cc76 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:664:20
    #13 0x7f085d462dd5 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #14 0x7f085d461d0a in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:716:7
    #15 0x7f085d458e3f in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #16 0x7f085d43a5b3 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:561:49
    #17 0x7f085d43bea6 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:618:14
    #18 0x7f085d3b5f3a in Run base/callback.h:241:12
    #19 0x7f085d3b5f3a in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #20 0x7f085fe0fe76 in Run base/callback.h:142:12
    #21 0x7f085fe0fe76 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #22 0x7f085fe5baad in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:388:29)> base/task/common/task_annotator.h:74:5
    #23 0x7f085fe5baad in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:386:21
    #24 0x7f085fe5b1c7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:291:41
    #25 0x7f085fe5c781 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #26 0x7f085ff9708c in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #27 0x7f085fe5ce3a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:498:12
    #28 0x7f085fd61b6c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #29 0x7f0841b9a9a6 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1067:18
    #30 0x7f0841b9f471 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #31 0x7f0841b94e6a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #32 0x7f08439b07cf in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10
    #33 0x7f08439b332f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1148:10
    #34 0x7f08439b2768 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1020:12
    #35 0x7f08439accd9 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:407:36
    #36 0x7f08439ad360 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:435:10
    #37 0x55ef238222ba in ChromeMain chrome/app/chrome_main.cc:176:12
    #38 0x7f080da150b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x619000a59050 is located 976 bytes inside of 1008-byte region [0x619000a58c80,0x619000a59070)
freed by thread T0 (chrome) here:
    #0 0x55ef238202fd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x7f084ec9df96 in views::View::~View() ui/views/view.cc:254:9
    #2 0x7f084eac5899 in views::BubbleDialogDelegateView::~BubbleDialogDelegateView() ui/views/bubble/bubble_dialog_delegate_view.cc:519:1
    #3 0x7f084c1d221f in ash::TrayBubbleView::~TrayBubbleView() ash/system/tray/tray_bubble_view.cc:293:35
    #4 0x7f084ecf2a03 in views::WidgetDelegate::DeleteDelegate() ui/views/widget/widget_delegate.cc:243:5
    #5 0x7f084ece974c in views::Widget::OnNativeWidgetDestroyed() ui/views/widget/widget.cc:1424:21
    #6 0x7f084ed47246 in OnWindowDestroyed ui/views/widget/native_widget_aura.cc:970:14
    #7 0x7f084ed47246 in non-virtual thunk to views::NativeWidgetAura::OnWindowDestroyed(aura::Window*) ui/views/widget/native_widget_aura.cc
    #8 0x7f084f5f1983 in aura::Window::~Window() ui/aura/window.cc:229:16
    #9 0x7f084f5f2c4b in aura::Window::~Window() ui/aura/window.cc:184:19
    #10 0x7f084bddbb9e in ash::RootWindowController::CloseChildWindows() ash/root_window_controller.cc:715:7
    #11 0x7f084bdd9757 in ash::RootWindowController::Shutdown() ash/root_window_controller.cc:655:3
    #12 0x7f084bc1981e in ash::WindowTreeHostManager::DeleteHost(ash::AshWindowTreeHost*) ash/display/window_tree_host_manager.cc:603:15
    #13 0x7f084bc1a23d in ash::WindowTreeHostManager::OnDisplayRemoved(display::Display const&) ash/display/window_tree_host_manager.cc:654:3
    #14 0x7f084f3ffa1f in display::DisplayManager::NotifyDisplayRemoved(display::Display const&) ui/display/manager/display_manager.cc:2201:14
    #15 0x7f084f3f9126 in display::DisplayManager::UpdateDisplaysWith(std::__Cr::vector<display::ManagedDisplayInfo, std::__Cr::allocator<display::ManagedDisplayInfo> > const&) ui/display/manager/display_manager.cc:1053:5
    #16 0x7f084f4023d4 in display::DisplayManager::AddRemoveDisplay(std::__Cr::vector<display::ManagedDisplayMode, std::__Cr::allocator<display::ManagedDisplayMode> >) ui/display/manager/display_manager.cc:1438:3
    #17 0x7f084b9a4662 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:2131:40
    #18 0x7f084b9a4f6d in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:1705:3
    #19 0x7f0850bf060e in TryProcess ui/base/accelerators/accelerator_manager.cc:153:17
    #20 0x7f0850bf060e in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator_manager.cc:83:27
    #21 0x7f085fe0fe76 in Run base/callback.h:142:12
    #22 0x7f085fe0fe76 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #23 0x7f085fe5baad in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:388:29)> base/task/common/task_annotator.h:74:5
    #24 0x7f085fe5baad in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:386:21
    #25 0x7f085fe5b1c7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:291:41
    #26 0x7f085fe5c781 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #27 0x7f085ff9708c in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #28 0x7f085fe5ce3a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:498:12
    #29 0x7f085fd61b6c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #30 0x7f0841b9a9a6 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1067:18
    #31 0x7f0841b9f471 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #32 0x7f0841b94e6a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #33 0x7f08439b07cf in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10

previously allocated by thread T0 (chrome) here:
    #0 0x55ef2381fa9d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x7f084bfeed70 in make_unique<global_media_controls::MediaItemUIListView, global_media_controls::MediaItemUIListView::SeparatorStyle> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x7f084bfeed70 in ash::MediaNotificationProviderImpl::GetMediaNotificationListView(int) ash/system/media/media_notification_provider_impl.cc:90:7
    #3 0x7f084bff4f7f in ash::MediaTray::ShowBubble() ash/system/media/media_tray.cc:286:41
    #4 0x7f084bff442e in PerformAction ash/system/media/media_tray.cc
    #5 0x7f084bff442e in non-virtual thunk to ash::MediaTray::PerformAction(ui::Event const&) ash/system/media/media_tray.cc
    #6 0x7f084c1b6bbb in ash::ActionableView::ButtonPressed(ui::Event const&) ash/system/tray/actionable_view.cc:83:33
    #7 0x7f084eae80fe in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ui/views/controls/button/button.cc:67:13
    #8 0x7f084eaf071e in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button_controller.cc
    #9 0x7f084f7b9ced in ui::ScopedTargetHandler::OnEvent(ui::Event*) ui/events/scoped_target_handler.cc:28:24
    #10 0x7f084f7ac18b in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #11 0x7f084f7ab6f2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #12 0x7f084f7ab1c6 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #13 0x7f084f7aaf2e in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #14 0x7f084ecd504d in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root_view.cc:485:9
    #15 0x7f084eceb23c in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1566:20
    #16 0x7f084c1748ab in ash::StatusAreaWidget::OnMouseEvent(ui::MouseEvent*) ash/system/status_area_widget.cc:639:18
    #17 0x7f084f7ac18b in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #18 0x7f084f7ab6f2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #19 0x7f084f7ab1c6 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #20 0x7f084f7aaf2e in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #21 0x7f084f7ae3f5 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #22 0x7f084f7b0c20 in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #23 0x7f084f7b1120 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:66:14
    #24 0x7f084f7af7a1 in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #25 0x7f084c9fc095 in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc:1273:12
    #26 0x7f084c9fc5d5 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc:757:12
    #27 0x7f084f7b10d0 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #28 0x7f084f7af7a1 in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #29 0x7f084bc3502a in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/keyboard_driven_event_rewriter.cc:31:12
    #30 0x7f084f7b10d0 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #31 0x7f084f7af7a1 in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/__tree:1079:59 in __root
Shadow bytes around the buggy address:
  0x0c32801431b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32801431c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32801431d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32801431e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32801431f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c3280143200: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fa fa
  0x0c3280143210: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3280143220: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3280143230: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3280143240: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3280143250: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==104994==ABORTING

Did this work before? N/A 

Chrome version: 102.0.4967.0  Channel: dev
OS Version: linux-chromeOS

## Attachments

- deleted (application/octet-stream, 0 B)
- [poc2.html](attachments/poc2.html) (text/plain, 518 B)
- [youtube.html](attachments/youtube.html) (text/plain, 1.7 KB)
- deleted (application/octet-stream, 0 B)
- [1312419_asan_device.log](attachments/1312419_asan_device.log) (text/plain, 33.5 KB)

## Timeline

### [Deleted User] (2022-04-01)

[Empty comment from Monorail migration]

### hc...@google.com (2022-04-01)

Switching to OS Chrome for ChromeOS sheriff to pick up as per description.

### ps...@google.com (2022-04-05)

@kaznacheev - could you help identify the right owner for this?


[Monorail components: Internals>Views]

### ps...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-05)

[Empty comment from Monorail migration]

### ka...@chromium.org (2022-04-05)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Views UI>Shell>StatusArea>MediaControls]

### li...@google.com (2022-04-06)

=> steimel@ for cros media session

### st...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### st...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5574493bedbb579740b90f672a24d1d0ba85954a

commit 5574493bedbb579740b90f672a24d1d0ba85954a
Author: Tommy Steimel <steimel@chromium.org>
Date: Tue Apr 12 00:18:21 2022

ChromeOS Global Media Controls: Use weak pointer instead of raw pointer

This CL changes ash::MediaNotificationProviderImpl's pointer to its
open list view from a raw pointer (that *never* changed back to null,
even after the dialog was closed) to a weak pointer.

Bug: 1312419
Change-Id: Idc7201fa41a853cba08e9caf9a92e661c0268bc3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3574095
Reviewed-by: Ahmed Mehfooz <amehfooz@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#991286}

[modify] https://crrev.com/5574493bedbb579740b90f672a24d1d0ba85954a/ash/system/media/media_notification_provider_impl.cc
[modify] https://crrev.com/5574493bedbb579740b90f672a24d1d0ba85954a/components/global_media_controls/public/views/media_item_ui_list_view.cc
[modify] https://crrev.com/5574493bedbb579740b90f672a24d1d0ba85954a/components/global_media_controls/public/views/media_item_ui_list_view.h
[modify] https://crrev.com/5574493bedbb579740b90f672a24d1d0ba85954a/ash/system/media/media_notification_provider_impl.h
[modify] https://crrev.com/5574493bedbb579740b90f672a24d1d0ba85954a/ash/system/media/media_notification_provider_impl_unittest.cc


### st...@chromium.org (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-15)

adding/adding back severity based on Chrome OS sheriffing, as this was originally triaged by Chrome OS but incorrect label was used 

### rh...@gmail.com (2022-04-16)

steimel@:

Thanks for expedited fixing this issue and the fixes in https://crbug.com/chromium/1312419#c10 works well and has no longer crash.

amy@ and Chrome OS security:
The screen cast below how I demonstrate on a real device, the purpose the demonstrate is to bump up the security severity. I tested on version 102.0.4967.0  same as in https://crbug.com/chromium/1312419#c0.




### [Deleted User] (2022-04-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-16)

Not requesting merge to dev (M102) because latest trunk commit (991286) appears to be prior to dev branch point (992738). If this is incorrect, please replace the Merge-NA-102 label with Merge-Request-102. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Congratulations, Rheza on another one. The VRP Panel has decided to award you $3,000 for this report as well given the user interaction required and that this issue is not web accessible. Thank you for reporting this issue to us! 


### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@google.com (2022-10-12)

UI>Shell>StatusArea issues owned by System UI team have migrated to buganizer. Moving MediaControls subcomponent issues to Internals>Media>UI

[Monorail components: Internals>Media>UI]

### jm...@google.com (2022-10-12)

[Empty comment from Monorail migration]

[Monorail components: -UI>Shell>StatusArea>MediaControls]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1312419?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1312366]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059272)*
