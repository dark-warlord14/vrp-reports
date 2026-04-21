# Heap-use-after-free on CaptionBubble::BackToTabButtonPressed

| Field | Value |
|-------|-------|
| **Issue ID** | [40060279](https://issues.chromium.org/issues/40060279) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>LiveCaption |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ev...@google.com |
| **Created** | 2022-07-14 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. Go <https://www.youtube.com/watch?v=8S0FDjFBj8o>
2. Enable live caption from top tab.
3. Enable chrome://flags/#enable-media-foundation-clear
4. Relaunch
5. Go <https://www.youtube.com/watch?v=8S0FDjFBj8o>
6. Play video.
7. "Your browser can't play this video."
8. Click Back to tab button from "Live Caption is not avaliable for this media." tab.

# **Problem Description:**

==14632==ERROR: AddressSanitizer: heap-use-after-free on address 0x11fa59b6d850 at pc 0x7ffa00525e2f bp 0x004060bfd7f0 sp 0x004060bfd838  

READ of size 8 at 0x11fa59b6d850 thread T0  

==14632==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffa00525e2e in captions::CaptionBubble::BackToTabButtonPressed C:\b\s\w\ir\cache\builder\src\components\live\_caption\views\caption\_bubble.cc:693  

#1 0x7ff9f54bc155 in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:111:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:760  

#2 0x7ff9f54b984f in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:648  

#3 0x7ff9f54b5bf5 in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:67  

#4 0x7ff9f8218c10 in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button\_controller.cc:59  

#5 0x7ff9f54fb6e0 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3118  

#6 0x7ff9ff408832 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#7 0x7ff9f647f267 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#8 0x7ff9f647e6b9 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#9 0x7ff9f647dfa3 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#10 0x7ff9f647dcf5 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#11 0x7ff9f8296451 in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:485  

#12 0x7ff9f55253f1 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1567  

#13 0x7ff9f647f267 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#14 0x7ff9f647e6b9 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#15 0x7ff9f647dfa3 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#16 0x7ff9f647dcf5 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#17 0x7ff9fb3a2656 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#18 0x7ff9f8288b25 in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#19 0x7ff9f8288781 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143  

#20 0x7ff9f828828f in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:112  

#21 0x7ff9fb3a0175 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1004  

#22 0x7ff9ff47878a in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3174  

#23 0x7ff9ff47187f in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:358  

#24 0x7ff9ff470f0f in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1027  

#25 0x7ff9f89b231c in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#26 0x7ff9f89b0c38 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#27 0x7ffa9cd21c4b in CallWindowProcW+0x43b (C:\WINDOWS\System32\user32.dll+0x180011c4b)  

#28 0x7ffa9cd20ea5 in DispatchMessageW+0x2b5 (C:\WINDOWS\System32\user32.dll+0x180010ea5)  

#29 0x7ff9f589322f in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:531  

#30 0x7ff9f5890f13 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:498  

#31 0x7ff9f58907b3 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:209  

#32 0x7ff9f588eaa4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#33 0x7ff9f867e23f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:497  

#34 0x7ff9f575c98b in base::RunLoop:

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [back-to-tab-button.jpg](attachments/back-to-tab-button.jpg) (image/jpeg, 47.6 KB)

## Timeline

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-14)

I was able to reproduce at r1021459.

Some clarifications to the repro process:

1. Open Chrome with ASAN.
2. Navigate to https://www.youtube.com/watch?v=8S0FDjFBj8o.
3. After the video starts playing, the media controls UI should be available in the top-right (playlist looking kind of icon).
4. Open the media controls and toggle on Live Caption.
5. Open a new tab to chrome://flags and enable chrome://flags/#enable-media-foundation-clear

Exit Chrome. Relaunch with --enable-logging.
5. Navigate to https://www.youtube.com/watch?v=8S0FDjFBj8o.
6. Click Play, which eventually results in a "browser can't play video".
7. Click "back to tab" button in the top right of the "live caption is not available..." bubble.

Crashes at this point.

https://source.chromium.org/chromium/chromium/src/+/main:components/live_caption/views/caption_bubble.cc;l=676;drc=0fc5b7e4216f36a83791db351ad6ac2617343206 is the UaF line.

Full ASan info:

=================================================================
==30396==ERROR: AddressSanitizer: heap-use-after-free on address 0x122fc10fae70 at pc 0x7ffa4367ddba bp 0x00e690ffdae0 sp 0x00e690ffdb28
READ of size 8 at 0x122fc10fae70 thread T0
==30396==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffa4367ddb9 in captions::CaptionBubble::BackToTabButtonPressed C:\b\s\w\ir\cache\builder\src\components\live_caption\views\caption_bubble.cc:676
    #1 0x7ffa38788fa3 in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:111:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:781
    #2 0x7ffa38786d55 in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:648
    #3 0x7ffa387830d4 in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:67
    #4 0x7ffa3b400292 in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button_controller.cc:59
    #5 0x7ffa3880bc64 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3118
    #6 0x7ffa3e518b91 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped_target_handler.cc:28
    #7 0x7ffa397bff84 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:190
    #8 0x7ffa397bf37f in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:139
    #9 0x7ffa397bec2c in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:83
    #10 0x7ffa397be960 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:55
    #11 0x7ffa3b3bfb19 in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:485
    #12 0x7ffa38835ce1 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1565
    #13 0x7ffa397bff84 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:190
    #14 0x7ffa397bf37f in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:139
    #15 0x7ffa397bec2c in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:83
    #16 0x7ffa397be960 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:55
    #17 0x7ffa3e515d74 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:49
    #18 0x7ffa3b3f6d7b in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:118
    #19 0x7ffa3b3f69c2 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:143
    #20 0x7ffa3b3f64a3 in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:112
    #21 0x7ffa3e558f35 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1004
    #22 0x7ffa428cc7d5 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3261
    #23 0x7ffa428c5263 in views::HWNDMessageHandler::_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:360
    #24 0x7ffa428c48a5 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1092
    #25 0x7ffa3bb6259a in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:306
    #26 0x7ffa3bb60f0c in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #27 0x7ffaac9fe857 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e857)
    #28 0x7ffaac9fe298 in DispatchMessageW+0x258 (C:\Windows\System32\user32.dll+0x18000e298)
    #29 0x7ffa38bb1b9f in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:531
    #30 0x7ffa38bafb0e in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:498
    #31 0x7ffa38baf33f in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:209
    #32 0x7ffa38bad4d9 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #33 0x7ffa3b82891a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:551
    #34 0x7ffa38a7144f in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #35 0x7ffa31371fc9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1036
    #36 0x7ffa313770ab in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:157
    #37 0x7ffa3136aff5 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #38 0x7ffa3862c8db in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678
    #39 0x7ffa3862fee4 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1189
    #40 0x7ffa3862eec8 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1061
    #41 0x7ffa3862b577 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:406
    #42 0x7ffa3862bcdc in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:434
    #43 0x7ffa2d0814ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:182
    #44 0x7ff7b98a56fe in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:162
    #45 0x7ff7b98a2ae4 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:395
    #46 0x7ff7b9ca9d9f in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #47 0x7ffaabd47033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #48 0x7ffaacda2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x122fc10fae70 is located 0 bytes inside of 16-byte region [0x122fc10fae70,0x122fc10fae80)
freed by thread T0 here:
    #0 0x7ff7b9949a3b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffa2d08a7b3 in ThreadProfiler::WorkIdRecorder::~WorkIdRecorder C:\b\s\w\ir\cache\builder\src\chrome\common\profiler\thread_profiler.cc:235
    #2 0x7ffa4320ac39 in captions::LiveCaptionUnavailabilityNotifier::~LiveCaptionUnavailabilityNotifier C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\live_caption_unavailability_notifier.cc:69
    #3 0x7ffa4320cda7 in captions::LiveCaptionUnavailabilityNotifier::~LiveCaptionUnavailabilityNotifier C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\live_caption_unavailability_notifier.cc:69
    #4 0x7ffa38dd7b89 in mojo::InterfaceEndpointClient::NotifyError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:696
    #5 0x7ffa38dede8e in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1016
    #6 0x7ffa38de7bb4 in mojo::internal::MultiplexRouter::ProcessTasks C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:929
    #7 0x7ffa38de4a90 in mojo::internal::MultiplexRouter::OnPipeConnectionError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:839
    #8 0x7ffa38dcd8fe in mojo::Connector::HandleError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:688
    #9 0x7ffa38e2468f in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #10 0x7ffa38afd674 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #11 0x7ffa3b826d11 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:406
    #12 0x7ffa3b825eee in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:284
    #13 0x7ffa38baf406 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:214
    #14 0x7ffa38bad4d9 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #15 0x7ffa3b82891a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:551
    #16 0x7ffa38a7144f in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #17 0x7ffa31371fc9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1036
    #18 0x7ffa313770ab in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:157
    #19 0x7ffa3136aff5 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #20 0x7ffa3862c8db in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678
    #21 0x7ffa3862fee4 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1189
    #22 0x7ffa3862eec8 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1061
    #23 0x7ffa3862b577 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:406
    #24 0x7ffa3862bcdc in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:434
    #25 0x7ffa2d0814ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:182
    #26 0x7ff7b98a56fe in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:162
    #27 0x7ff7b98a2ae4 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:395

previously allocated by thread T0 here:
    #0 0x7ff7b9949b3b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffa4bc3b62e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffa4677213d in captions::CaptionBubbleContextBrowser::Create C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\accessibility\caption_bubble_context_views.cc:20
    #3 0x7ffa4320a30a in captions::LiveCaptionUnavailabilityNotifier::LiveCaptionUnavailabilityNotifier C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\live_caption_unavailability_notifier.cc:52
    #4 0x7ffa4320a097 in captions::LiveCaptionUnavailabilityNotifier::Create C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\live_caption_unavailability_notifier.cc:39
    #5 0x7ffa3ebef46c in chrome::internal::BindMediaFoundationRendererNotifierHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_interface_binders.cc:616
    #6 0x7ffa31368473 in base::internal::Invoker<base::internal::BindState<void (*)(content::RenderFrameHost *, mojo::PendingReceiver<blink::mojom::BackgroundFetchService>)>,void (content::RenderFrameHost *, mojo::PendingReceiver<blink::mojom::BackgroundFetchService>)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:781
    #7 0x7ffa31368701 in mojo::internal::BinderContextTraits<content::RenderFrameHost *>::BindGenericReceiver<blink::mojom::BackgroundFetchService> C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\binder_map_internal.h:39
    #8 0x7ffa313688d5 in base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (const content::ServiceWorkerVersionBaseInfo &, mojo::PendingReceiver<blink::mojom::NativeIOHost>)> &, const content::ServiceWorkerVersionBaseInfo &, mojo::ScopedHandleBase<mojo::MessagePipeHandle>),base::RepeatingCallback<void (const content::ServiceWorkerVersionBaseInfo &, mojo::PendingReceiver<blink::mojom::NativeIOHost>)> >,void (const content::ServiceWorkerVersionBaseInfo &, mojo::ScopedHandleBase<mojo::MessagePipeHandle>)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:781
    #9 0x7ffa31f94628 in mojo::internal::GenericCallbackBinderWithContext<content::RenderFrameHost *>::RunCallbackWithContext C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\binder_map_internal.h:120
    #10 0x7ffa31f93e5d in mojo::internal::GenericCallbackBinderWithContext<content::RenderFrameHost *>::BindInterface C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\binder_map_internal.h:101
    #11 0x7ffa31f93aeb in mojo::BinderMapWithContext<content::RenderFrameHost *>::TryBind C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\binder_map.h:104
    #12 0x7ffa31f937ee in content::BrowserInterfaceBrokerImpl<content::RenderFrameHostImpl,content::RenderFrameHost *>::BindInterface C:\b\s\w\ir\cache\builder\src\content\browser\browser_interface_broker_impl.h:90
    #13 0x7ffa31f933f1 in content::BrowserInterfaceBrokerImpl<content::RenderFrameHostImpl,content::RenderFrameHost *>::GetInterface C:\b\s\w\ir\cache\builder\src\content\browser\browser_interface_broker_impl.h:60
    #14 0x7ffa2fec3ea8 in blink::mojom::BrowserInterfaceBrokerStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\browser_interface_broker.mojom.cc:185
    #15 0x7ffa38dd38a6 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:935
    #16 0x7ffa3b95f516 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48
    #17 0x7ffa38dd7672 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:666
    #18 0x7ffa38deb9aa in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1096
    #19 0x7ffa38dea89a in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:716
    #20 0x7ffa3b95f61e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #21 0x7ffa38dce5ca in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561
    #22 0x7ffa38dcfe4b in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:618
    #23 0x7ffa38e2468f in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #24 0x7ffa38afd674 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #25 0x7ffa3b826d11 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:406
    #26 0x7ffa3b825eee in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:284
    #27 0x7ffa38baf406 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:214

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\components\live_caption\views\caption_bubble.cc:676 in captions::CaptionBubble::BackToTabButtonPressed
Shadow bytes around the buggy address:
  0x0471b8f1f570: f7 fa fd fa f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x0471b8f1f580: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x0471b8f1f590: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fa
  0x0471b8f1f5a0: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x0471b8f1f5b0: f7 fa fd fa f7 fa fd fd f7 fa fd fd f7 fa fd fa
=>0x0471b8f1f5c0: f7 fa fd fa f7 fa fd fa f7 fa 00 fa f7 fa[fd]fd
  0x0471b8f1f5d0: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x0471b8f1f5e0: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x0471b8f1f5f0: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x0471b8f1f600: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x0471b8f1f610: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
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

### dc...@chromium.org (2022-07-14)

The line in question is from https://crrev.com/7ba47d250e46af1335906ef41d888a8d996c7b5c, so this affects extended.

While the repro mechanism is Windows-specific, I don't think the ASan crash is. I don't think Android has the same UI here, so I'm only tagging with desktop systems.

Similarly, while the repro mechanism requires enabling a disabled-by-default feature, it really just relies on the "live caption not supported" bubble being displayed, which I don't think requires this feature. So I am not tagging this with impact none.

Medium despite being a browser process use-after-free because user interaction (as far as I know) is required to enable live caption, and user interaction is required to click the "back to tab" button in the bubble.

(+abigailbklein@google.com, please feel free to correct any of the analysis above if it's not correct. I'm not particularly familiar with this area)

[Monorail components: Internals>Media>LiveCaption]

### dc...@chromium.org (2022-07-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-14)

In particular, if you feel this should be "High" instead of "Medium" because it's easier to reach than I've suggested above, that would be an important clarification :)

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### sa...@gmail.com (2022-07-14)

This video just crashes when the live caption feature or Picture-in-Picture mode is on. 
But I couldn't find anything else here that would just make the video crash. So I had to use #enable-media-foundation-clear .

I used the code below which could cause the crash but here all the context is gone as the whole page crashed.

 try { var b = new Blob([new Uint8Array(1024 * 1024 * 1024), new Uint8Array(1024 * 1024 * 1024), new Uint8Array(1024 * 1024 * 1024), new Uint8Array(1024 * 1024 * 1024)]); } catch {}


If you know of a feature that will just make the video crash, please share it with me and I can increase the report to minimal user interaction.

I haven't sent a report for a long time, I think I've encountered something like this before.

Thanks!

Samet B.

### ab...@google.com (2022-07-14)

Triage to Evan for the media foundation/Live Caption collision.

### [Deleted User] (2022-07-15)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ev...@google.com (2022-07-26)

I'm unable to reproduce this issue at r1027416 with the gn args:

is_asan=true
is_debug=false
is_component_build=true
use_goma=true

Screen recording: https://drive.google.com/file/d/18q771194LiZ6UxusxMZjE5IGc1eUN9Lm/view?usp=sharing&resourcekey=0-PxMjQJQCyfpdc0W2MlPXPg

dcheng@ - Did you repro this on a physical Windows machine? The pipeline behaves differently when on a physical machine vs. CRD-ing into a machine.

### sa...@gmail.com (2022-07-30)

Hey evliu@, I can help you if you share the video publicly.

### th...@chromium.org (2022-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-10)

evliu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-24)

evliu: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2022-09-01)

ping

### sa...@gmail.com (2022-09-16)

ping

### ev...@google.com (2022-09-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f75ccca910973a12a575592f464e941cb773ce5

commit 0f75ccca910973a12a575592f464e941cb773ce5
Author: Evan Liu <evliu@google.com>
Date: Tue Sep 20 20:45:59 2022

Close the media foundation error message when the audio stream stops

This CL updates the LiveCaptionUnavailabilityNotifier to close the
caption bubble upon its destruction.

Bug: 1344514
Change-Id: Iaad99c2c3eaabbb173940019c5593ccbbfff169b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3902408
Reviewed-by: Abigail Klein <abigailbklein@google.com>
Commit-Queue: Evan Liu <evliu@google.com>
Cr-Commit-Position: refs/heads/main@{#1049323}

[modify] https://crrev.com/0f75ccca910973a12a575592f464e941cb773ce5/chrome/browser/accessibility/live_caption_unavailability_notifier.cc
[modify] https://crrev.com/0f75ccca910973a12a575592f464e941cb773ce5/components/live_caption/live_caption_controller.h
[modify] https://crrev.com/0f75ccca910973a12a575592f464e941cb773ce5/components/live_caption/views/caption_bubble_controller_views.h
[modify] https://crrev.com/0f75ccca910973a12a575592f464e941cb773ce5/chrome/test/BUILD.gn
[add] https://crrev.com/0f75ccca910973a12a575592f464e941cb773ce5/chrome/browser/accessibility/live_caption_unavailability_notifier_browsertest.cc
[modify] https://crrev.com/0f75ccca910973a12a575592f464e941cb773ce5/components/live_caption/caption_bubble_controller.h


### ev...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-30)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a very heavily mitigated [1] security bug. Thank you for your efforts and reporting this issue to us! 

[1] https://g.co/chrome/vrp 

### sa...@gmail.com (2022-09-30)

yayyyyyyyyyyyyyyy


### am...@google.com (2022-10-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1344514?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1351684]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060279)*
