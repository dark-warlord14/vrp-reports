# Security: Heap-use-after-free in BackgroundFetchDelegateBase::CancelDownload 

| Field | Value |
|-------|-------|
| **Issue ID** | [40056027](https://issues.chromium.org/issues/40056027) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2021-05-28 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36

Steps to reproduce the problem:
1. download chromium-asan-887050.zip and unzip
2. `touch no.js` at the same folder of poc.html and start a server `python -m SimpleHTTPServer 8605`
3. "close the network" and ./chrome http://127.0.0.1:8605/poc.html
4. click cancel of download item

What is the expected behavior?

What went wrong?
In function CancelDownload[1] of file components/background_fetch/background_fetch_delegate_base.cc 

Call to Abort [2] will re-assign offline_item_ and free the older offline_item_, however the function GetClient[3] will use it again => UAF.

```
void BackgroundFetchDelegateBase::CancelDownload(const std::string& job_id) {
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);
  JobDetails* job_details = GetJobDetails(job_id);

  if (job_details->job_state == JobDetails::State::kDownloadsComplete ||
      job_details->job_state == JobDetails::State::kJobComplete) {
    // The cancel event arrived after the fetch was complete; ignore it.
    return;
  }

  job_details->cancelled_from_ui = true;
  Abort(job_id);

  if (auto client = GetClient(job_id)) {
    client->OnJobCancelled(
        job_id, blink::mojom::BackgroundFetchFailureReason::CANCELLED_FROM_UI);
  }
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/background_fetch/background_fetch_delegate_base.cc;drc=9fcc9d7b2915b6192ee6810eec54c50deb6313c6;l=154
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/background_fetch/background_fetch_delegate_base.cc;drc=9fcc9d7b2915b6192ee6810eec54c50deb6313c6;l=165
[3] https://source.chromium.org/chromium/chromium/src/+/main:components/background_fetch/background_fetch_delegate_base.cc;l=167;drc=9fcc9d7b2915b6192ee6810eec54c50deb6313c6

=================================================================
==10799==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160002475af at pc 0x555579f79a18 bp 0x7fffffffc6f0 sp 0x7fffffffc6e8
READ of size 1 at 0x6160002475af thread T0 (chrome)
[Detaching after fork from child process 11926]
    #0 0x555579f79a17 in std::__1::__tree_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, void*>*, long> std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails> > >::find<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) buildtools/third_party/libc++/trunk/include/__tree
    #1 0x555579f74c17 in find buildtools/third_party/libc++/trunk/include/map:1380:68
    #2 0x555579f74c17 in GetClient components/background_fetch/background_fetch_delegate_base.cc:518:30
    #3 0x555579f74c17 in background_fetch::BackgroundFetchDelegateBase::CancelDownload(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) components/background_fetch/background_fetch_delegate_base.cc:167:21
    #4 0x55556e607fb7 in DownloadUIModel::ExecuteCommand(DownloadCommands*, DownloadCommands::Command) chrome/browser/download/download_ui_model.cc:603:7
    #5 0x555577d6ca28 in views::MenuModelAdapter::ExecuteCommand(int, int) ui/views/controls/menu/menu_model_adapter.cc:167:12
    #6 0x555577d15093 in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView*, int) ui/views/controls/menu/menu_runner_impl.cc:245:29
    #7 0x555577d188f4 in views::MenuController::ExitMenu() ui/views/controls/menu/menu_controller.cc:3062:13
    #8 0x555577d1d2c1 in views::MenuController::OnMouseReleased(views::SubmenuView*, ui::MouseEvent const&) ui/views/controls/menu/menu_controller.cc:825:7
    #9 0x555577edf4cb in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1428:20
    #10 0x555570ea8c67 in ui::EventHandler::OnEvent(ui::Event*) ui/events/event_handler.cc
    #11 0x555570ea67d9 in DispatchEvent ui/events/event_dispatcher.cc:191:12
    #12 0x555570ea67d9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:140:5
    #13 0x555570ea60a3 in DispatchEventToTarget ui/events/event_dispatcher.cc:84:14
    #14 0x555570ea60a3 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #15 0x55557345f20d in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #16 0x55557347dabf in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #17 0x55557347d763 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #18 0x555577faac77 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:247:38
    #19 0x555577fa5606 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:273:29
    #20 0x555571f44cf3 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1195:34
    #21 0x555571f43fff in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1141:3
    #22 0x555571f44f0c in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #23 0x555570afb044 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:97:29
    #24 0x555571002eb4 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:291:5
    #25 0x5555618a5aba in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #26 0x5555618a4b21 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #27 0x5555618a4b21 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #28 0x555571010d94 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #29 0x7ffff7e2ee8d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51e8d)

0x6160002475af is located 47 bytes inside of 616-byte region [0x616000247580,0x6160002477e8)
freed by thread T0 (chrome) here:
    #0 0x5555603f021d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55556eceb656 in operator() buildtools/third_party/libc++/trunk/include/memory:1335:5
    #2 0x55556eceb656 in reset buildtools/third_party/libc++/trunk/include/memory:1596:7
    #3 0x55556eceb656 in operator= buildtools/third_party/libc++/trunk/include/memory:1515:5
    #4 0x55556eceb656 in OfflineItemModel::OnItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) chrome/browser/download/offline_item_model.cc:237:17
    #5 0x55557a095766 in offline_items_collection::FilteredOfflineItemObserver::OnItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/filtered_offline_item_observer.cc:62:14
    #6 0x55557a09f937 in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/offline_content_provider.cc:42:14
    #7 0x55557a09f937 in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/offline_content_provider.cc:42:14
    #8 0x55556ea76f53 in BackgroundFetchDelegateImpl::DoUpdateUi(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) chrome/browser/background_fetch/background_fetch_delegate_impl.cc:253:3
    #9 0x555579f74c01 in background_fetch::BackgroundFetchDelegateBase::CancelDownload(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) components/background_fetch/background_fetch_delegate_base.cc:165:3
    #10 0x55556e607fb7 in DownloadUIModel::ExecuteCommand(DownloadCommands*, DownloadCommands::Command) chrome/browser/download/download_ui_model.cc:603:7
    #11 0x555577d6ca28 in views::MenuModelAdapter::ExecuteCommand(int, int) ui/views/controls/menu/menu_model_adapter.cc:167:12
    #12 0x555577d15093 in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView*, int) ui/views/controls/menu/menu_runner_impl.cc:245:29
    #13 0x555577d188f4 in views::MenuController::ExitMenu() ui/views/controls/menu/menu_controller.cc:3062:13
    #14 0x555577d1d2c1 in views::MenuController::OnMouseReleased(views::SubmenuView*, ui::MouseEvent const&) ui/views/controls/menu/menu_controller.cc:825:7
    #15 0x555577edf4cb in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1428:20
    #16 0x555570ea8c67 in ui::EventHandler::OnEvent(ui::Event*) ui/events/event_handler.cc
    #17 0x555570ea67d9 in DispatchEvent ui/events/event_dispatcher.cc:191:12
    #18 0x555570ea67d9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:140:5
    #19 0x555570ea60a3 in DispatchEventToTarget ui/events/event_dispatcher.cc:84:14
    #20 0x555570ea60a3 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #21 0x55557345f20d in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #22 0x55557347dabf in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #23 0x55557347d763 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #24 0x555577faac77 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:247:38
    #25 0x555577fa5606 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:273:29
    #26 0x555571f44cf3 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1195:34
    #27 0x555571f43fff in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1141:3
    #28 0x555571f44f0c in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #29 0x555570afb044 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:97:29
    #30 0x555571002eb4 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:291:5
    #31 0x5555618a5aba in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #32 0x5555618a4b21 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #33 0x5555618a4b21 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #34 0x555571010d94 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #35 0x7ffff7e2ee8d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51e8d)

previously allocated by thread T0 (chrome) here:
    #0 0x5555603ef9bd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55556eceb604 in make_unique<offline_items_collection::OfflineItem, const offline_items_collection::OfflineItem &> buildtools/third_party/libc++/trunk/include/memory:2006:28
    #2 0x55556eceb604 in OfflineItemModel::OnItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) chrome/browser/download/offline_item_model.cc:237:19
    #3 0x55557a095766 in offline_items_collection::FilteredOfflineItemObserver::OnItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/filtered_offline_item_observer.cc:62:14
    #4 0x55557a09f937 in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/offline_content_provider.cc:42:14
    #5 0x55557a09f937 in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/offline_content_provider.cc:42:14
    #6 0x55556ea76f53 in BackgroundFetchDelegateImpl::DoUpdateUi(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) chrome/browser/background_fetch/background_fetch_delegate_impl.cc:253:3
    #7 0x555579f73f01 in background_fetch::BackgroundFetchDelegateBase::DownloadUrl(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, GURL const&, net::NetworkTrafficAnnotationTag const&, net::HttpRequestHeaders const&, bool) components/background_fetch/background_fetch_delegate_base.cc:120:3
    #8 0x5555652a7328 in content::BackgroundFetchDelegateProxy::Core::StartRequest(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, url::Origin const&, scoped_refptr<content::BackgroundFetchRequestInfo> const&) content/browser/background_fetch/background_fetch_delegate_proxy.cc:183:15
    #9 0x5555652ad417 in Invoke<void (content::BackgroundFetchDelegateProxy::Core::*)(const std::string &, const url::Origin &, const scoped_refptr<content::BackgroundFetchRequestInfo> &), base::WeakPtr<content::BackgroundFetchDelegateProxy::Core>, std::string, url::Origin, scoped_refptr<content::BackgroundFetchRequestInfo> > base/bind_internal.h:509:12
    #10 0x5555652ad417 in MakeItSo<void (content::BackgroundFetchDelegateProxy::Core::*)(const std::string &, const url::Origin &, const scoped_refptr<content::BackgroundFetchRequestInfo> &), base::WeakPtr<content::BackgroundFetchDelegateProxy::Core>, std::string, url::Origin, scoped_refptr<content::BackgroundFetchRequestInfo> > base/bind_internal.h:668:5
    #11 0x5555652ad417 in RunImpl<void (content::BackgroundFetchDelegateProxy::Core::*)(const std::string &, const url::Origin &, const scoped_refptr<content::BackgroundFetchRequestInfo> &), std::tuple<base::WeakPtr<content::BackgroundFetchDelegateProxy::Core>, std::string, url::Origin, scoped_refptr<content::BackgroundFetchRequestInfo> >, 0UL, 1UL, 2UL, 3UL> base/bind_internal.h:721:12
    #12 0x5555652ad417 in base::internal::Invoker<base::internal::BindState<void (content::BackgroundFetchDelegateProxy::Core::*)(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, url::Origin const&, scoped_refptr<content::BackgroundFetchRequestInfo> const&), base::WeakPtr<content::BackgroundFetchDelegateProxy::Core>, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, url::Origin, scoped_refptr<content::BackgroundFetchRequestInfo> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #13 0x555564e807ac in Run base/callback.h:98:12
    #14 0x555564e807ac in content::RunOrPostTaskOnThread(base::Location const&, content::BrowserThread::ID, base::OnceCallback<void ()>) content/public/browser/browser_thread.cc:19:21
    #15 0x5555652a6a7c in content::BackgroundFetchDelegateProxy::StartRequest(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, url::Origin const&, scoped_refptr<content::BackgroundFetchRequestInfo> const&) content/browser/background_fetch/background_fetch_delegate_proxy.cc:401:3
    #16 0x5555652b7441 in content::BackgroundFetchJobController::StartRequest(scoped_refptr<content::BackgroundFetchRequestInfo>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>) content/browser/background_fetch/background_fetch_job_controller.cc:158:20
    #17 0x5555652b9c30 in content::BackgroundFetchJobController::DidPopNextRequest(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>) content/browser/background_fetch/background_fetch_job_controller.cc:316:3
    #18 0x5555652bde0b in void base::internal::FunctorTraits<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), void>::Invoke<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), base::WeakPtr<content::BackgroundFetchJobController>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo> >(void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), base::WeakPtr<content::BackgroundFetchJobController>&&, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>&&, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>&&, blink::mojom::BackgroundFetchError&&, scoped_refptr<content::BackgroundFetchRequestInfo>&&) base/bind_internal.h:509:12
    #19 0x5555652bdb48 in MakeItSo<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, const content::BackgroundFetchRequestInfo *)>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), base::WeakPtr<content::BackgroundFetchJobController>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, const content::BackgroundFetchRequestInfo *)>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo> > base/bind_internal.h:668:5
    #20 0x5555652bdb48 in RunImpl<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, const content::BackgroundFetchRequestInfo *)>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), std::tuple<base::WeakPtr<content::BackgroundFetchJobController>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, const content::BackgroundFetchRequestInfo *)>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, scoped_refptr<content::BackgroundFetchRequestInfo>)> >, 0UL, 1UL, 2UL> base/bind_internal.h:721:12
    #21 0x5555652bdb48 in base::internal::Invoker<base::internal::BindState<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), base::WeakPtr<content::BackgroundFetchJobController>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)> >, void (blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>)>::RunOnce(base::internal::BindStateBase*, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>&&) base/bind_internal.h:690:12
    #22 0x55556531b018 in base::OnceCallback<void (blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>)>::Run(blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>) && base/callback.h:98:12
    #23 0x55556531aeb9 in content::background_fetch::StartNextPendingRequestTask::FinishWithError(blink::mojom::BackgroundFetchError) content/browser/background_fetch/storage/start_next_pending_request_task.cc:128:24
    #24 0x55556531b7db in Invoke<void (content::background_fetch::StartNextPendingRequestTask::*)(blink::ServiceWorkerStatusCode), base::WeakPtr<content::background_fetch::StartNextPendingRequestTask>, blink::ServiceWorkerStatusCode> base/bind_internal.h:509:12
    #25 0x55556531b7db in MakeItSo<void (content::background_fetch::StartNextPendingRequestTask::*)(blink::ServiceWorkerStatusCode), base::WeakPtr<content::background_fetch::StartNextPendingRequestTask>, blink::ServiceWorkerStatusCode> base/bind_internal.h:668:5
    #26 0x55556531b7db in RunImpl<void (content::background_fetch::StartNextPendingRequestTask::*)(blink::ServiceWorkerStatusCode), std::tuple<base::WeakPtr<content::background_fetch::StartNextPendingRequestTask> >, 0UL> base/bind_internal.h:721:12
    #27 0x55556531b7db in base::internal::Invoker<base::internal::BindState<void (content::background_fetch::StartNextPendingRequestTask::*)(blink::ServiceWorkerStatusCode), base::WeakPtr<content::background_fetch::StartNextPendingRequestTask> >, void (blink::ServiceWorkerStatusCode)>::RunOnce(base::internal::BindStateBase*, blink::ServiceWorkerStatusCode) base/bind_internal.h:690:12
    #28 0x555566349b41 in Run base/callback.h:98:12
    #29 0x555566349b41 in Invoke<base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, blink::ServiceWorkerStatusCode> base/bind_internal.h:608:49
    #30 0x555566349b41 in MakeItSo<base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, blink::ServiceWorkerStatusCode> base/bind_internal.h:648:12
    #31 0x555566349b41 in RunImpl<base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, std::tuple<blink::ServiceWorkerStatusCode>, 0UL> base/bind_internal.h:721:12
    #32 0x555566349b41 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, blink::ServiceWorkerStatusCode>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #33 0x55556daa9ef0 in Run base/callback.h:98:12
    #34 0x55556daa9ef0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #35 0x55556dae46ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:344:23
    #36 0x55556dae3efb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:258:36
    #37 0x55556d9a5d99 in HandleDispatch base/message_loop/message_pump_glib.cc:374:46
    #38 0x55556d9a5d99 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:124:43
    #39 0x7ffff7e2efbc in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/__tree in std::__1::__tree_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, void*>*, long> std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails> > >::find<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)
Shadow bytes around the buggy address:
  0x0c2c80040e60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c80040e70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c80040e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c80040e90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c80040ea0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2c80040eb0: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c2c80040ec0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c80040ed0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c80040ee0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c80040ef0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c2c80040f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==10799==ABORTING

Did this work before? N/A 

Chrome version: 91.0.4472.77  Channel: stable
OS Version: 
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2021-05-28)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-28)

Reproduced on Mac ASAN build 887050 as follows.

1. Put poc.html in a folder
2. touch no.js
3. python3 -m http.server 8605
4. Open Chromium and visit http://127.0.0.1:8605/poc.html, wait for the background fetch to complete
5. Quit Chromium
6. From the command line run Chromium.app/Contents/MacOS/Chromium http://127.0.0.1:8605/poc.html
7. On the keychain dialog which appears, click Deny (or presumably any other option)
8. Immediately as soon as the window appears, you'll see the download start in the bottom left.
9. Immediately click on the pop-up menu and choose Cancel
10. Get ASAN crash as below.

This seems to be subtly different from the Linux instructions: on the Mac, the download completes almost immediately even if WiFi is off. You have to strike fast to cancel the download before it's too late.

In fact there seems to be no point turning off wifi on the Mac - it is equally reproducible with and without the network on, but you have to act fast to cancel the download.

As a browser process bug triggered by web content, this would normally be Critical severity. But I'm assuming that the UI interaction of cancelling the download here is a necessary part of the reproduction and thus I'm downgrading this to High. merc.ouc@, if you know any way to trigger this without UI gestures please let us know.



$ ./Chromium.app/Contents/MacOS/Chromium http://127.0.0.1:8605/poc.html
objc[10138]: Class WebSwapLayerCGL is implemented in both /System/Library/Frameworks/WebKit.framework/Versions/A/Frameworks/WebCore.framework/Versions/A/WebCore (0x7fff82050ad0) and /Users/adetaylor/Downloads/asan-mac-release-870757/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/91.0.4472.0/Libraries/libGLESv2.dylib (0x14a734de8). One of the two will be used. Which one is undefined.
[10129:259:0528/092530.074410:ERROR:keychain_password_mac.mm(83)] Keychain lookup failed: Error Domain=NSOSStatusErrorDomain Code=-128 "userCanceledErr" (-128)
=================================================================
==10129==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160003600af at pc 0x00012d577d18 bp 0x7ffee76318d0 sp 0x7ffee76318c8
READ of size 1 at 0x6160003600af thread T0
    #0 0x12d577d17 in std::__1::__tree_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, void*>*, long> std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails> > >::find<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) __tree
    #1 0x12d5726ea in background_fetch::BackgroundFetchDelegateBase::CancelDownload(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) background_fetch_delegate_base.cc:200
    #2 0x120b813c0 in DownloadUIModel::ExecuteCommand(DownloadCommands*, DownloadCommands::Command) download_ui_model.cc:590
    #3 0x12234c061 in -[MenuControllerCocoa itemSelected:] menu_controller.mm:296
    #4 0x7fff22e9cb0a in -[NSApplication(NSResponder) sendAction:to:from:]+0x11f (AppKit:x86_64+0x25fb0a)
    #5 0x1216b2bfc in __43-[BrowserCrApplication sendAction:to:from:]_block_invoke chrome_browser_application_mac.mm:295
    #6 0x12053cdd9 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xbfe7dd9)
    #7 0x1216b265a in -[BrowserCrApplication sendAction:to:from:] chrome_browser_application_mac.mm:294
    #8 0x7fff22f9fb00 in -[NSMenuItem _corePerformAction]+0x19c (AppKit:x86_64+0x362b00)
    #9 0x7fff22f9f81f in -[NSCarbonMenuImpl performActionWithHighlightingForItemAtIndex:]+0x5e (AppKit:x86_64+0x36281f)
    #10 0x7fff22febdff in -[NSMenu performActionForItemAtIndex:]+0x70 (AppKit:x86_64+0x3aedff)
    #11 0x7fff22febd85 in -[NSMenu _internalPerformActionForItemAtIndex:]+0x51 (AppKit:x86_64+0x3aed85)
    #12 0x7fff22febbcc in -[NSCarbonMenuImpl _carbonCommandProcessEvent:handlerCallRef:]+0x64 (AppKit:x86_64+0x3aebcc)
    #13 0x7fff22f82450 in NSSLMMenuEventHandler+0x435 (AppKit:x86_64+0x345450)
    #14 0x7fff28679dc0 in DispatchEventToHandlers(EventTargetRec*, OpaqueEventRef*, HandlerCallRec*)+0x551 (HIToolbox:x86_64+0x9dc0)
    #15 0x7fff286791e2 in SendEventToEventTargetInternal(OpaqueEventRef*, OpaqueEventTargetRef*, HandlerCallRec*)+0x14a (HIToolbox:x86_64+0x91e2)
    #16 0x7fff2868ea91 in SendEventToEventTarget+0x26 (HIToolbox:x86_64+0x1ea91)
    #17 0x7fff286ee6f6 in SendHICommandEvent(unsigned int, HICommand const*, unsigned int, unsigned int, unsigned char, void const*, OpaqueEventTargetRef*, OpaqueEventTargetRef*, OpaqueEventRef**)+0x16f (HIToolbox:x86_64+0x7e6f6)
    #18 0x7fff287142d0 in SendMenuCommandWithContextAndModifiers+0x2c (HIToolbox:x86_64+0xa42d0)
    #19 0x7fff2871427b in SendMenuItemSelectedEvent+0x15b (HIToolbox:x86_64+0xa427b)
    #20 0x7fff287140ca in FinishMenuSelection(SelectionData*, MenuResult*, MenuResult*)+0x5f (HIToolbox:x86_64+0xa40ca)
    #21 0x7fff288222b0 in PopUpMenuSelectCore(MenuData*, Point, double, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, unsigned int, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x5c3 (HIToolbox:x86_64+0x1b22b0)
    #22 0x7fff288217f2 in _HandlePopUpMenuSelection8(OpaqueMenuRef*, OpaqueEventRef*, unsigned int, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x199 (HIToolbox:x86_64+0x1b17f2)
    #23 0x7fff286f6444 in _HandlePopUpMenuSelectionWithDictionary+0x148 (HIToolbox:x86_64+0x86444)
    #24 0x7fff23149768 in SLMPerformPopUpCarbonMenu+0x8b2 (AppKit:x86_64+0x50c768)
    #25 0x7fff22fe5130 in _NSSLMPopUpCarbonMenu3+0x447 (AppKit:x86_64+0x3a8130)
    #26 0x7fff23086ed4 in -[NSCarbonMenuImpl _popUpContextMenu:withEvent:forView:withFont:]+0xcf (AppKit:x86_64+0x449ed4)
    #27 0x7fff23086d5f in -[NSMenu _popUpContextMenu:withEvent:forView:withFont:]+0xd0 (AppKit:x86_64+0x449d5f)
    #28 0x12bc54816 in views::internal::MenuRunnerImplCocoa::RunMenuAt(views::Widget*, views::MenuButtonController*, gfx::Rect const&, views::MenuAnchorPosition, int, gfx::NativeView) menu_runner_impl_cocoa.mm:413
    #29 0x12cb0d4d6 in DownloadShelfContextMenuView::Run(views::Widget*, gfx::Rect const&, ui::MenuSourceType, base::RepeatingCallback<void ()>) download_shelf_context_menu_view.cc:52
    #30 0x12caf2bd4 in DownloadItemView::DropdownButtonPressed(ui::Event const&) download_item_view.cc:1190
    #31 0x12b8c7768 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) button_controller.cc
    #32 0x123a9644f in ui::EventHandler::OnEvent(ui::Event*) event_handler.cc
    #33 0x123aa3954 in ui::ScopedTargetHandler::OnEvent(ui::Event*) scoped_target_handler.cc:28
    #34 0x123a948a2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:140
    #35 0x123a94150 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:56
    #36 0x12bbdf8ad in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) root_view.cc:480
    #37 0x12bbfb181 in views::Widget::OnMouseEvent(ui::MouseEvent*) widget.cc:1330
    #38 0x12bc3720c in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::__1::unique_ptr<ui::Event, std::__1::default_delete<ui::Event> >) native_widget_mac_ns_window_host.mm:809
    #39 0x127e5e08b in -[BridgedContentView mouseEvent:] bridged_content_view.mm:595
    #40 0x127e5b53d in -[BridgedContentView processCapturedMouseEvent:] bridged_content_view.mm:308
    #41 0x127e6900b in invocation function for block in remote_cocoa::CocoaMouseCapture::ActiveEventTap::Init() mouse_capture.mm:91
    #42 0x7fff22e04b5c in _NSSendEventToObservers+0x14f (AppKit:x86_64+0x1c7b5c)
    #43 0x7fff22e03675 in -[NSApplication(NSEvent) sendEvent:]+0x51 (AppKit:x86_64+0x1c6675)
    #44 0x1216b4644 in __34-[BrowserCrApplication sendEvent:]_block_invoke chrome_browser_application_mac.mm:335
    #45 0x12053cdd9 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xbfe7dd9)
    #46 0x1216b39be in -[BrowserCrApplication sendEvent:] chrome_browser_application_mac.mm:319
    #47 0x7fff230dc978 in -[NSApplication _handleEvent:]+0x40 (AppKit:x86_64+0x49f978)
    #48 0x7fff22c6c69d in -[NSApplication run]+0x26e (AppKit:x86_64+0x2f69d)
    #49 0x12055172a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*) message_pump_mac.mm:717
    #50 0x12054d318 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) message_pump_mac.mm:157
    #51 0x120461c75 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread_controller_with_message_pump_impl.cc:460
    #52 0x12039f6ae in base::RunLoop::Run(base::Location const&) run_loop.cc:133
    #53 0x118c86fe8 in content::BrowserMainLoop::RunMainMessageLoop() browser_main_loop.cc:991
    #54 0x118c8b521 in content::BrowserMainRunnerImpl::Run() browser_main_runner_impl.cc:152
    #55 0x118c8040c in content::BrowserMain(content::MainFunctionParams const&) browser_main.cc:47
    #56 0x120172742 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content_main_runner_impl.cc:1081
    #57 0x1201719e4 in content::ContentMainRunnerImpl::Run(bool) content_main_runner_impl.cc:956
    #58 0x12016ecf6 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content_main.cc:372
    #59 0x12016f30c in content::ContentMain(content::ContentMainParams const&) content_main.cc:398
    #60 0x11455d615 in ChromeMain chrome_main.cc:141
    #61 0x1085cb2df in main chrome_exe_main_mac.cc:114
    #62 0x7fff203a3f3c in start+0x0 (libdyld.dylib:x86_64+0x15f3c)

0x6160003600af is located 47 bytes inside of 616-byte region [0x616000360080,0x6160003602e8)
freed by thread T0 here:
    #0 0x1087c3159  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x45159)
    #1 0x1213026d2 in OfflineItemModel::OnItemUpdated(offline_items_collection::OfflineItem const&, base::Optional<offline_items_collection::UpdateDelta> const&) offline_item_model.cc:237
    #2 0x12d5d4d8b in offline_items_collection::FilteredOfflineItemObserver::OnItemUpdated(offline_items_collection::OfflineItem const&, base::Optional<offline_items_collection::UpdateDelta> const&) filtered_offline_item_observer.cc:62
    #3 0x12d5e04ac in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, base::Optional<offline_items_collection::UpdateDelta> const&) offline_content_provider.cc:42
    #4 0x12d5e04ac in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, base::Optional<offline_items_collection::UpdateDelta> const&) offline_content_provider.cc:42
    #5 0x1209a0ee6 in BackgroundFetchDelegateImpl::DoUpdateUi(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) background_fetch_delegate_impl.cc:288
    #6 0x12d5726d7 in background_fetch::BackgroundFetchDelegateBase::CancelDownload(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) background_fetch_delegate_base.cc:198
    #7 0x120b813c0 in DownloadUIModel::ExecuteCommand(DownloadCommands*, DownloadCommands::Command) download_ui_model.cc:590
    #8 0x12234c061 in -[MenuControllerCocoa itemSelected:] menu_controller.mm:296
    #9 0x7fff22e9cb0a in -[NSApplication(NSResponder) sendAction:to:from:]+0x11f (AppKit:x86_64+0x25fb0a)
    #10 0x1216b2bfc in __43-[BrowserCrApplication sendAction:to:from:]_block_invoke chrome_browser_application_mac.mm:295
    #11 0x12053cdd9 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xbfe7dd9)
    #12 0x1216b265a in -[BrowserCrApplication sendAction:to:from:] chrome_browser_application_mac.mm:294
    #13 0x7fff22f9fb00 in -[NSMenuItem _corePerformAction]+0x19c (AppKit:x86_64+0x362b00)
    #14 0x7fff22f9f81f in -[NSCarbonMenuImpl performActionWithHighlightingForItemAtIndex:]+0x5e (AppKit:x86_64+0x36281f)
    #15 0x7fff22febdff in -[NSMenu performActionForItemAtIndex:]+0x70 (AppKit:x86_64+0x3aedff)
    #16 0x7fff22febd85 in -[NSMenu _internalPerformActionForItemAtIndex:]+0x51 (AppKit:x86_64+0x3aed85)
    #17 0x7fff22febbcc in -[NSCarbonMenuImpl _carbonCommandProcessEvent:handlerCallRef:]+0x64 (AppKit:x86_64+0x3aebcc)
    #18 0x7fff22f82450 in NSSLMMenuEventHandler+0x435 (AppKit:x86_64+0x345450)
    #19 0x7fff28679dc0 in DispatchEventToHandlers(EventTargetRec*, OpaqueEventRef*, HandlerCallRec*)+0x551 (HIToolbox:x86_64+0x9dc0)
    #20 0x7fff286791e2 in SendEventToEventTargetInternal(OpaqueEventRef*, OpaqueEventTargetRef*, HandlerCallRec*)+0x14a (HIToolbox:x86_64+0x91e2)
    #21 0x7fff2868ea91 in SendEventToEventTarget+0x26 (HIToolbox:x86_64+0x1ea91)
    #22 0x7fff286ee6f6 in SendHICommandEvent(unsigned int, HICommand const*, unsigned int, unsigned int, unsigned char, void const*, OpaqueEventTargetRef*, OpaqueEventTargetRef*, OpaqueEventRef**)+0x16f (HIToolbox:x86_64+0x7e6f6)
    #23 0x7fff287142d0 in SendMenuCommandWithContextAndModifiers+0x2c (HIToolbox:x86_64+0xa42d0)
    #24 0x7fff2871427b in SendMenuItemSelectedEvent+0x15b (HIToolbox:x86_64+0xa427b)
    #25 0x7fff287140ca in FinishMenuSelection(SelectionData*, MenuResult*, MenuResult*)+0x5f (HIToolbox:x86_64+0xa40ca)
    #26 0x7fff288222b0 in PopUpMenuSelectCore(MenuData*, Point, double, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, unsigned int, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x5c3 (HIToolbox:x86_64+0x1b22b0)
    #27 0x7fff288217f2 in _HandlePopUpMenuSelection8(OpaqueMenuRef*, OpaqueEventRef*, unsigned int, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x199 (HIToolbox:x86_64+0x1b17f2)
    #28 0x7fff286f6444 in _HandlePopUpMenuSelectionWithDictionary+0x148 (HIToolbox:x86_64+0x86444)
    #29 0x7fff23149768 in SLMPerformPopUpCarbonMenu+0x8b2 (AppKit:x86_64+0x50c768)

previously allocated by thread T0 here:
    #0 0x1087c3010  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x45010)
    #1 0x12029a217 in operator new(unsigned long) new.cpp:67
    #2 0x121302675 in OfflineItemModel::OnItemUpdated(offline_items_collection::OfflineItem const&, base::Optional<offline_items_collection::UpdateDelta> const&) offline_item_model.cc:237
    #3 0x12d5d4d8b in offline_items_collection::FilteredOfflineItemObserver::OnItemUpdated(offline_items_collection::OfflineItem const&, base::Optional<offline_items_collection::UpdateDelta> const&) filtered_offline_item_observer.cc:62
    #4 0x12d5e04ac in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, base::Optional<offline_items_collection::UpdateDelta> const&) offline_content_provider.cc:42
    #5 0x12d5e04ac in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, base::Optional<offline_items_collection::UpdateDelta> const&) offline_content_provider.cc:42
    #6 0x1209a0ee6 in BackgroundFetchDelegateImpl::DoUpdateUi(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) background_fetch_delegate_impl.cc:288
    #7 0x12d573b0a in background_fetch::BackgroundFetchDelegateBase::OnDownloadUpdated(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, unsigned long long, unsigned long long) background_fetch_delegate_base.cc:335
    #8 0x120b25a80 in base::internal::Invoker<base::internal::BindState<void (download::DeferredClientWrapper::*)(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, unsigned long long, unsigned long long), base::WeakPtr<download::DeferredClientWrapper>, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, unsigned long long, unsigned long long>, void ()>::RunOnce(base::internal::BindStateBase*) bind_internal.h:690
    #9 0x120b2421d in download::DeferredClientWrapper::DoRunDeferredClosures() deferred_client_wrapper.cc:195
    #10 0x120b22892 in download::DeferredClientWrapper::OnDownloadUpdated(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, unsigned long long, unsigned long long) deferred_client_wrapper.cc:79
    #11 0x12d2e79ab in base::internal::Invoker<base::internal::BindState<void (download::ControllerImpl::*)(download::DownloadClient, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, unsigned long long, unsigned long long), base::WeakPtr<download::ControllerImpl>, download::DownloadClient, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, unsigned long long, unsigned long long>, void ()>::RunOnce(base::internal::BindStateBase*) bind_internal.h:690
    #12 0x1204229e3 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) task_annotator.cc:173
    #13 0x120460ae4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) thread_controller_with_message_pump_impl.cc:351
    #14 0x1204602c7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:264
    #15 0x12054fd48 in invocation function for block in base::MessagePumpCFRunLoopBase::RunWorkSource(void*) message_pump_mac.mm:361
    #16 0x12053cdd9 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xbfe7dd9)
    #17 0x12054e4f5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*) message_pump_mac.mm:360
    #18 0x7fff20481a8b in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x10 (CoreFoundation:x86_64h+0x81a8b)
    #19 0x7fff204819f3 in __CFRunLoopDoSource0+0xb3 (CoreFoundation:x86_64h+0x819f3)
    #20 0x7fff20481773 in __CFRunLoopDoSources0+0xf1 (CoreFoundation:x86_64h+0x81773)
    #21 0x7fff2048019b in __CFRunLoopRun+0x37c (CoreFoundation:x86_64h+0x8019b)
    #22 0x7fff2047f75b in CFRunLoopRunSpecific+0x232 (CoreFoundation:x86_64h+0x7f75b)
    #23 0x7fff286a1202 in RunCurrentEventLoopInMode+0x123 (HIToolbox:x86_64+0x31202)
    #24 0x7fff288253d0 in SelectItemAndRestoreAllMenuBits(MenuSelectData&, SelectionData*, MenuResult*, MenuResult*)+0x3af (HIToolbox:x86_64+0x1b53d0)
    #25 0x7fff28825eb6 in TrackMenuCommon(MenuSelectData&, unsigned char*, SelectionData*, MenuResult*, MenuResult*)+0x720 (HIToolbox:x86_64+0x1b5eb6)
    #26 0x7fff288221e6 in PopUpMenuSelectCore(MenuData*, Point, double, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, unsigned int, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x4f9 (HIToolbox:x86_64+0x1b21e6)
    #27 0x7fff288217f2 in _HandlePopUpMenuSelection8(OpaqueMenuRef*, OpaqueEventRef*, unsigned int, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x199 (HIToolbox:x86_64+0x1b17f2)
    #28 0x7fff286f6444 in _HandlePopUpMenuSelectionWithDictionary+0x148 (HIToolbox:x86_64+0x86444)
    #29 0x7fff23149768 in SLMPerformPopUpCarbonMenu+0x8b2 (AppKit:x86_64+0x50c768)

SUMMARY: AddressSanitizer: heap-use-after-free __tree in std::__1::__tree_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, void*>*, long> std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails> > >::find<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)
Shadow bytes around the buggy address:
  0x1c2c0006bfc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c2c0006bfd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c2c0006bfe0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c2c0006bff0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c2c0006c000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x1c2c0006c010: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x1c2c0006c020: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0006c030: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0006c040: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0006c050: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x1c2c0006c060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==10129==ABORTING
Received signal 6
 [0x000120515789]
 [0x0001202c1ac3]
 [0x0001205153eb]
 [0x7fff203cdd7d]
 [0x000114442551]
 [0x7fff202dd411]
 [0x0001087e2a96]
 [0x0001087e21c4]
 [0x0001087c9724]
 [0x0001087c8ffa]
 [0x0001087c9a48]
 [0x00012d577d18]
 [0x00012d5726eb]
 [0x000120b813c1]
 [0x00012234c062]
 [0x7fff22e9cb0b]
 [0x0001216b2bfd]
 [0x00012053cdda]
 [0x0001216b265b]
 [0x7fff22f9fb01]
 [0x7fff22f9f820]
 [0x7fff22febe00]
 [0x7fff22febd86]
 [0x7fff22febbcd]
 [0x7fff22f82451]
 [0x7fff28679dc1]
 [0x7fff286791e3]
 [0x7fff2868ea92]
 [0x7fff286ee6f7]
 [0x7fff287142d1]
 [0x7fff2871427c]
 [0x7fff287140cb]
 [0x7fff288222b1]
 [0x7fff288217f3]
 [0x7fff286f6445]
 [0x7fff23149769]
 [0x7fff22fe5131]
 [0x7fff23086ed5]
 [0x7fff23086d60]
 [0x00012bc54817]
 [0x00012cb0d4d7]
 [0x00012caf2bd5]
 [0x00012b8c7769]
 [0x000123a96450]
 [0x000123aa3955]
 [0x000123a948a3]
 [0x000123a94151]
 [0x00012bbdf8ae]
 [0x00012bbfb182]
 [0x00012bc3720d]
 [0x000127e5e08c]
 [0x000127e5b53e]
 [0x000127e6900c]
 [0x7fff22e04b5d]
 [0x7fff22e03676]
 [0x0001216b4645]
 [0x00012053cdda]
 [0x0001216b39bf]
 [0x7fff230dc979]
 [0x7fff22c6c69e]
 [0x00012055172b]
 [0x00012054d319]
 [0x000120461c76]
 [0x00012039f6af]
 [0x000118c86fe9]
 [0x000118c8b522]
 [0x000118c8040d]
 [0x000120172743]
 [0x0001201719e5]
 [0x00012016ecf7]
 [0x00012016f30d]
 [0x00011455d616]
 [0x0001085cb2e0]
 [0x7fff203a3f3d]
 [0x000000000002]
[end of stack trace]
[0528/092642.649215:WARNING:crash_report_exception_handler.cc(240)] UniversalExceptionRaise: (os/kern) failure (5)
Abort trap: 6


[Monorail components: Blink>BackgroundFetch]

### ad...@google.com (2021-05-28)

peter@, are you the right person for this? Thanks!

### [Deleted User] (2021-05-28)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2021-06-01)

A few thoughts -

  (1) GetJobDetails() uses NOTREACHED() to catch the case where no job details can be found, but that's substituted by DCHECK(false) and therefore removed in release builds. That should be a fatal check, or we bail out on nullptrs in CancelDownload() like we do in the other methods.

  (2) The stack trace about usage misses a whole bunch of steps between #3 and #4 -- more than I would expect. I don't actually see where the UAF is happening. +shaktisahu and +rayankans, could you take a look please?



### ad...@google.com (2021-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-15)

peter: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2021-06-22)

any update?

### ra...@chromium.org (2021-06-23)

Sorry, I just got around to this.

I'm not 100% sure what's happening here (I'm unable to reproduce), but from investigating the stack trace + code here are a few comments.

1. The |ui_state_map_|  and |job_details_map_| always erase entries together.
2. Looking at the duplicate stack traces 2 & 3, it looks like we are receiving a delayed update event (BackgroundFetchDelegateImpl::DoUpdateUi) after the job has been marked as complete. An invalid offline_item is then sent to OfflineItemModel::OnItemUpdated, which invokes the copy constructor on invalid data. I sent a fix here  https://chromium-review.googlesource.com/c/chromium/src/+/2983039
3. I have no idea what's happening in stack trace #1. Both repros by merc.ouc@ and adetaylor@ suggest something is going wrong when accessing an item |job_details_map_| in BackgroundFetchDelegateBase::CancelDownload. According to the stack trace from merc.ouc@ this is happening when `GetClient` is called, however that is safe and we check for nullptrs there. We also don't modify the map states at any point in between. I'm wondering if this is also a delayed cancel event when the maps have already been cleared (aborting from the UI after the fetch is & clean-up is complete), and the UAF is happening when we check the job state. I sent a fix for that here: https://chromium-review.googlesource.com/c/chromium/src/+/2982462

### gi...@appspot.gserviceaccount.com (2021-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b218dba987aee43e9d45c457f00cebe2c745adc

commit 9b218dba987aee43e9d45c457f00cebe2c745adc
Author: Rayan Kanso <rayankans@google.com>
Date: Mon Jun 28 12:16:58 2021

[BackgroundFetch] Add safe guard before dispatching update event to OIC.

Bug: 1214199
Change-Id: I78423fe68b9c362dfe4dc8d8e8475108587608a9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2983039
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/master@{#896488}

[modify] https://crrev.com/9b218dba987aee43e9d45c457f00cebe2c745adc/chrome/browser/background_fetch/background_fetch_delegate_impl.cc


### gi...@appspot.gserviceaccount.com (2021-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8af07187730c7ffa6d77bf0750f611dfa50d9c89

commit 8af07187730c7ffa6d77bf0750f611dfa50d9c89
Author: Rayan Kanso <rayankans@google.com>
Date: Mon Jun 28 13:50:39 2021

[BackgroundFetch] Check if job is still valid after cancel event

Bug: 1214199
Change-Id: Ia623625c1f44576d0db963e16df87184141bd0cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2982462
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Cr-Commit-Position: refs/heads/master@{#896511}

[modify] https://crrev.com/8af07187730c7ffa6d77bf0750f611dfa50d9c89/components/background_fetch/background_fetch_delegate_base.cc


### me...@gmail.com (2021-06-29)

It seems that this uaf is sitll reproducible. I test with {896734}. 

=================================================================
==33605==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160000861af at pc 0x559c5e3cc348 bp 0x7ffe3acf7930 sp 0x7ffe3acf7928
READ of size 1 at 0x6160000861af thread T0 (chrome)
    #0 0x559c5e3cc347 in std::__1::__tree_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, void*>*, long> std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails> > >::find<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) buildtools/third_party/libc++/trunk/include/__tree
    #1 0x559c5e3c753d in find buildtools/third_party/libc++/trunk/include/map:1391:68
    #2 0x559c5e3c753d in GetClient components/background_fetch/background_fetch_delegate_base.cc:519:30
    #3 0x559c5e3c753d in background_fetch::BackgroundFetchDelegateBase::CancelDownload(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) components/background_fetch/background_fetch_delegate_base.cc:168:21
    #4 0x559c52841a27 in DownloadUIModel::ExecuteCommand(DownloadCommands*, DownloadCommands::Command) chrome/browser/download/download_ui_model.cc:607:7
    #5 0x559c52f21122 in DownloadCommands::ExecuteCommand(DownloadCommands::Command) chrome/browser/download/download_commands.cc:165:11
    #6 0x559c5c15cf58 in views::MenuModelAdapter::ExecuteCommand(int, int) ui/views/controls/menu/menu_model_adapter.cc:169:12
    #7 0x559c5c103953 in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView*, int) ui/views/controls/menu/menu_runner_impl.cc:245:29
    #8 0x559c5c107204 in views::MenuController::ExitMenu() ui/views/controls/menu/menu_controller.cc:3139:13
    #9 0x559c5c10bbd1 in views::MenuController::OnMouseReleased(views::SubmenuView*, ui::MouseEvent const&) ui/views/controls/menu/menu_controller.cc:827:7
    #10 0x559c5c2cda4b in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1463:20
    #11 0x559c55114ce9 in DispatchEvent ui/events/event_dispatcher.cc:191:12
    #12 0x559c55114ce9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:140:5
    #13 0x559c551145b3 in DispatchEventToTarget ui/events/event_dispatcher.cc:84:14
    #14 0x559c551145b3 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #15 0x559c57e4576d in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #16 0x559c57e63eff in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #17 0x559c57e63ba3 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #18 0x559c5c39a1d7 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:247:38
    #19 0x559c5c394b66 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:273:29
    #20 0x559c562bafa3 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1245:34
    #21 0x559c562ba2af in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1191:3
    #22 0x559c562bb1bc in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #23 0x559c54d62cf4 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:97:29
    #24 0x559c55272b04 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:291:5
    #25 0x559c45f9bc0a in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #26 0x559c45f9ac71 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #27 0x559c45f9ac71 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #28 0x559c55281664 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #29 0x7f426452fe8d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51e8d)

0x6160000861af is located 47 bytes inside of 616-byte region [0x616000086180,0x6160000863e8)
freed by thread T0 (chrome) here:
    #0 0x559c44acfd0d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x559c52f299b6 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x559c52f299b6 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x559c52f299b6 in operator= buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:234:5
    #4 0x559c52f299b6 in OfflineItemModel::OnItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) chrome/browser/download/offline_item_model.cc:237:17
    #5 0x559c5e4e1f86 in offline_items_collection::FilteredOfflineItemObserver::OnItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/filtered_offline_item_observer.cc:62:14
    #6 0x559c5e4ec157 in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/offline_content_provider.cc:42:14
    #7 0x559c5e4ec157 in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/offline_content_provider.cc:42:14
    #8 0x559c52caf33a in BackgroundFetchDelegateImpl::DoUpdateUi(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) chrome/browser/background_fetch/background_fetch_delegate_impl.cc:259:3
    #9 0x559c5e3c7528 in background_fetch::BackgroundFetchDelegateBase::CancelDownload(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) components/background_fetch/background_fetch_delegate_base.cc:166:3
    #10 0x559c52841a27 in DownloadUIModel::ExecuteCommand(DownloadCommands*, DownloadCommands::Command) chrome/browser/download/download_ui_model.cc:607:7
    #11 0x559c52f21122 in DownloadCommands::ExecuteCommand(DownloadCommands::Command) chrome/browser/download/download_commands.cc:165:11
    #12 0x559c5c15cf58 in views::MenuModelAdapter::ExecuteCommand(int, int) ui/views/controls/menu/menu_model_adapter.cc:169:12
    #13 0x559c5c103953 in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView*, int) ui/views/controls/menu/menu_runner_impl.cc:245:29
    #14 0x559c5c107204 in views::MenuController::ExitMenu() ui/views/controls/menu/menu_controller.cc:3139:13
    #15 0x559c5c10bbd1 in views::MenuController::OnMouseReleased(views::SubmenuView*, ui::MouseEvent const&) ui/views/controls/menu/menu_controller.cc:827:7
    #16 0x559c5c2cda4b in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1463:20
    #17 0x559c55114ce9 in DispatchEvent ui/events/event_dispatcher.cc:191:12
    #18 0x559c55114ce9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:140:5
    #19 0x559c551145b3 in DispatchEventToTarget ui/events/event_dispatcher.cc:84:14
    #20 0x559c551145b3 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #21 0x559c57e4576d in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #22 0x559c57e63eff in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #23 0x559c57e63ba3 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #24 0x559c5c39a1d7 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:247:38
    #25 0x559c5c394b66 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:273:29
    #26 0x559c562bafa3 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1245:34
    #27 0x559c562ba2af in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1191:3
    #28 0x559c562bb1bc in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #29 0x559c54d62cf4 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:97:29
    #30 0x559c55272b04 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:291:5
    #31 0x559c45f9bc0a in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #32 0x559c45f9ac71 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #33 0x559c45f9ac71 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #34 0x559c55281664 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #35 0x7f426452fe8d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51e8d)

previously allocated by thread T0 (chrome) here:
    #0 0x559c44acf4ad in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x559c52f29964 in make_unique<offline_items_collection::OfflineItem, const offline_items_collection::OfflineItem &> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x559c52f29964 in OfflineItemModel::OnItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) chrome/browser/download/offline_item_model.cc:237:19
    #3 0x559c5e4e1f86 in offline_items_collection::FilteredOfflineItemObserver::OnItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/filtered_offline_item_observer.cc:62:14
    #4 0x559c5e4ec157 in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/offline_content_provider.cc:42:14
    #5 0x559c5e4ec157 in offline_items_collection::OfflineContentProvider::NotifyItemUpdated(offline_items_collection::OfflineItem const&, absl::optional<offline_items_collection::UpdateDelta> const&) components/offline_items_collection/core/offline_content_provider.cc:42:14
    #6 0x559c52caf33a in BackgroundFetchDelegateImpl::DoUpdateUi(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) chrome/browser/background_fetch/background_fetch_delegate_impl.cc:259:3
    #7 0x559c5e3c6821 in background_fetch::BackgroundFetchDelegateBase::DownloadUrl(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, GURL const&, net::NetworkTrafficAnnotationTag const&, net::HttpRequestHeaders const&, bool) components/background_fetch/background_fetch_delegate_base.cc:120:3
    #8 0x559c49af5b78 in content::BackgroundFetchDelegateProxy::Core::StartRequest(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, url::Origin const&, scoped_refptr<content::BackgroundFetchRequestInfo> const&) content/browser/background_fetch/background_fetch_delegate_proxy.cc:183:15
    #9 0x559c49afbc67 in Invoke<void (content::BackgroundFetchDelegateProxy::Core::*)(const std::string &, const url::Origin &, const scoped_refptr<content::BackgroundFetchRequestInfo> &), base::WeakPtr<content::BackgroundFetchDelegateProxy::Core>, std::string, url::Origin, scoped_refptr<content::BackgroundFetchRequestInfo> > base/bind_internal.h:509:12
    #10 0x559c49afbc67 in MakeItSo<void (content::BackgroundFetchDelegateProxy::Core::*)(const std::string &, const url::Origin &, const scoped_refptr<content::BackgroundFetchRequestInfo> &), base::WeakPtr<content::BackgroundFetchDelegateProxy::Core>, std::string, url::Origin, scoped_refptr<content::BackgroundFetchRequestInfo> > base/bind_internal.h:668:5
    #11 0x559c49afbc67 in RunImpl<void (content::BackgroundFetchDelegateProxy::Core::*)(const std::string &, const url::Origin &, const scoped_refptr<content::BackgroundFetchRequestInfo> &), std::tuple<base::WeakPtr<content::BackgroundFetchDelegateProxy::Core>, std::string, url::Origin, scoped_refptr<content::BackgroundFetchRequestInfo> >, 0UL, 1UL, 2UL, 3UL> base/bind_internal.h:721:12
    #12 0x559c49afbc67 in base::internal::Invoker<base::internal::BindState<void (content::BackgroundFetchDelegateProxy::Core::*)(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, url::Origin const&, scoped_refptr<content::BackgroundFetchRequestInfo> const&), base::WeakPtr<content::BackgroundFetchDelegateProxy::Core>, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, url::Origin, scoped_refptr<content::BackgroundFetchRequestInfo> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #13 0x559c496c92bc in Run base/callback.h:98:12
    #14 0x559c496c92bc in content::RunOrPostTaskOnThread(base::Location const&, content::BrowserThread::ID, base::OnceCallback<void ()>) content/public/browser/browser_thread.cc:19:21
    #15 0x559c49af52cc in content::BackgroundFetchDelegateProxy::StartRequest(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, url::Origin const&, scoped_refptr<content::BackgroundFetchRequestInfo> const&) content/browser/background_fetch/background_fetch_delegate_proxy.cc:401:3
    #16 0x559c49b059c1 in content::BackgroundFetchJobController::StartRequest(scoped_refptr<content::BackgroundFetchRequestInfo>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>) content/browser/background_fetch/background_fetch_job_controller.cc:161:20
    #17 0x559c49b081b0 in content::BackgroundFetchJobController::DidPopNextRequest(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>) content/browser/background_fetch/background_fetch_job_controller.cc:321:3
    #18 0x559c49b0c38b in void base::internal::FunctorTraits<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), void>::Invoke<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), base::WeakPtr<content::BackgroundFetchJobController>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo> >(void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), base::WeakPtr<content::BackgroundFetchJobController>&&, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>&&, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>&&, blink::mojom::BackgroundFetchError&&, scoped_refptr<content::BackgroundFetchRequestInfo>&&) base/bind_internal.h:509:12
    #19 0x559c49b0c0c8 in MakeItSo<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, const content::BackgroundFetchRequestInfo *)>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), base::WeakPtr<content::BackgroundFetchJobController>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, const content::BackgroundFetchRequestInfo *)>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo> > base/bind_internal.h:668:5
    #20 0x559c49b0c0c8 in RunImpl<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, const content::BackgroundFetchRequestInfo *)>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), std::tuple<base::WeakPtr<content::BackgroundFetchJobController>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, const content::BackgroundFetchRequestInfo *)>, base::OnceCallback<void (const content::BackgroundFetchRegistrationId &, scoped_refptr<content::BackgroundFetchRequestInfo>)> >, 0UL, 1UL, 2UL> base/bind_internal.h:721:12
    #21 0x559c49b0c0c8 in base::internal::Invoker<base::internal::BindState<void (content::BackgroundFetchJobController::*)(base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)>, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>), base::WeakPtr<content::BackgroundFetchJobController>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, content::BackgroundFetchRequestInfo const*)>, base::OnceCallback<void (content::BackgroundFetchRegistrationId const&, scoped_refptr<content::BackgroundFetchRequestInfo>)> >, void (blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>)>::RunOnce(base::internal::BindStateBase*, blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>&&) base/bind_internal.h:690:12
    #22 0x559c49b6add8 in base::OnceCallback<void (blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>)>::Run(blink::mojom::BackgroundFetchError, scoped_refptr<content::BackgroundFetchRequestInfo>) && base/callback.h:98:12
    #23 0x559c49b6ac79 in content::background_fetch::StartNextPendingRequestTask::FinishWithError(blink::mojom::BackgroundFetchError) content/browser/background_fetch/storage/start_next_pending_request_task.cc:128:24
    #24 0x559c49b6b59b in Invoke<void (content::background_fetch::StartNextPendingRequestTask::*)(blink::ServiceWorkerStatusCode), base::WeakPtr<content::background_fetch::StartNextPendingRequestTask>, blink::ServiceWorkerStatusCode> base/bind_internal.h:509:12
    #25 0x559c49b6b59b in MakeItSo<void (content::background_fetch::StartNextPendingRequestTask::*)(blink::ServiceWorkerStatusCode), base::WeakPtr<content::background_fetch::StartNextPendingRequestTask>, blink::ServiceWorkerStatusCode> base/bind_internal.h:668:5
    #26 0x559c49b6b59b in RunImpl<void (content::background_fetch::StartNextPendingRequestTask::*)(blink::ServiceWorkerStatusCode), std::tuple<base::WeakPtr<content::background_fetch::StartNextPendingRequestTask> >, 0UL> base/bind_internal.h:721:12
    #27 0x559c49b6b59b in base::internal::Invoker<base::internal::BindState<void (content::background_fetch::StartNextPendingRequestTask::*)(blink::ServiceWorkerStatusCode), base::WeakPtr<content::background_fetch::StartNextPendingRequestTask> >, void (blink::ServiceWorkerStatusCode)>::RunOnce(base::internal::BindStateBase*, blink::ServiceWorkerStatusCode) base/bind_internal.h:690:12
    #28 0x559c4abc0851 in Run base/callback.h:98:12
    #29 0x559c4abc0851 in Invoke<base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, blink::ServiceWorkerStatusCode> base/bind_internal.h:608:49
    #30 0x559c4abc0851 in MakeItSo<base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, blink::ServiceWorkerStatusCode> base/bind_internal.h:648:12
    #31 0x559c4abc0851 in RunImpl<base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, std::tuple<blink::ServiceWorkerStatusCode>, 0UL> base/bind_internal.h:721:12
    #32 0x559c4abc0851 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, blink::ServiceWorkerStatusCode>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #33 0x559c51cdd170 in Run base/callback.h:98:12
    #34 0x559c51cdd170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #35 0x559c51d17949 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #36 0x559c51d170ba in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #37 0x559c51d18301 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #38 0x559c51bd04d9 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #39 0x559c51bd04d9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #40 0x7f426452ffbc in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/__tree in std::__1::__tree_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, void*>*, long> std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails>, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, background_fetch::JobDetails> > >::find<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)
Shadow bytes around the buggy address:
  0x0c2c80008be0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c2c80008bf0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c2c80008c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c2c80008c10: 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c80008c20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2c80008c30: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c2c80008c40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c80008c50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c80008c60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c80008c70: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c2c80008c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==33605==ABORTING


### [Deleted User] (2021-06-29)

peter: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2021-07-01)

Thanks for confirming merc.ouc@

Now that we have eliminated event orders from potentially causing this, it looks like this is being caused by:
- the cancel flow sending a reference to the offline item
- the update flow overwriting the offline item

However, these are synchronous, I don't see any async tasks being queued up. AFAICT these are all running on the UI thread as well, so I'm still unsure how this is happening.

shaktisahu@, since you are more familiar with the offline model stuff, can you confirm if OfflineItemModel can run on a thread other than the UI thread?

### sh...@chromium.org (2021-07-20)

+qinmin@ to comment.  

### qi...@chromium.org (2021-07-20)

Can we add some thread checker to ensure that OfflineItem and BackgroundFetchDelegateBase are running on the ui thread? 

The stacktrace for the BackgroundFetchDelegateBase looks strange, I am wondering if it is caused by some bugs that messes up the stack, like deleting a pointer twice etc?

### qi...@chromium.org (2021-07-20)

could an OfflineItemModel::OnItemUpdated() trigger a synchronous OfflineItemModel::OnItemRemoved() by one of OfflineItemModel's observers?
That will cause a very messy call chain if it happens, and could cause UAF somewhere.

### [Deleted User] (2021-07-27)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-08-19)

rayankans@: qinmin had some suggestions in c#17 and c#18 - can you try those? This is a Severity-High security bug that we should strive to fix soon.

### ra...@chromium.org (2021-08-20)

Sorry about that, I missed it.

The good news however is that I seem to have inadvertently fixed this while working on another issue. Fix: https://chromium-review.googlesource.com/c/chromium/src/+/3100205

I am unable to reproduce this,  can someone else also verify this is no longer happening?

### me...@gmail.com (2021-08-23)

Hi rayankans@, I also unable to reproduce this. Test with chromium-asan-912875.

### am...@chromium.org (2021-08-30)

hi, peter@ and rayankans@, this issue is still opened however, it appears issue is fixed as per comments #27-28. Can you please update it as such? 
It appears that  https://chromium-review.googlesource.com/c/chromium/src/+/3100205 and the prior CLs landed for this bug have already been merged. 

### ra...@chromium.org (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

Requesting merge to stable M92 because latest trunk commit (896511) appears to be after stable branch point (885287).

Not requesting merge to other stable (M93) because latest trunk commit (896511) appears to be prior to other stable branch point (902210). If this is incorrect, please replace the Merge-NA-93 label with Merge-Request-93. If other changes are required to fix this bug completely, please request a merge if necessary.

Not requesting merge to beta (M94) because latest trunk commit (896511) appears to be prior to beta branch point (911515). If this is incorrect, please replace the Merge-NA-94 label with Merge-Request-94. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-02)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2021-09-03)

1. Does your merge fit within the Merge Decision Guidelines?
Yes
2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3100205
3. Has the change landed and been verified on ToT?
Yes
4. Does this change need to be merged into other active release branches (M-1, M+1)?
no
5. Why are these changes required in this milestone after branch?
Security issue
6. Is this a new feature?
No
7. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2021-09-03)

Merge approved for M94 branch:4606 please merege asap

### am...@chromium.org (2021-09-08)

Merge Approved for M93; please merge to branch 4577 by 2pm PDT tomorrow (Thursday, 9 September) to ensure this fix is in next week's stable security refresh. 
Please also merge to branch 4515, as M92 is currently the Extended Stable release channel as we transition to the 4W stable channel release cycle. Thanks. 

### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-08)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thanks for this report as well as letting us know when it was still reproducible! 

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### pb...@google.com (2021-09-10)

All the cherry picks to respective branches are merged :

M94 : https://chromium-review.googlesource.com/c/chromium/src/+/3141726
M93  : https://chromium-review.googlesource.com/c/chromium/src/+/3151944
M92 : https://chromium-review.googlesource.com/c/chromium/src/+/3151844


### pb...@google.com (2021-09-10)

[Empty comment from Monorail migration]

### rz...@google.com (2021-11-08)

Marking as not applicable, not reproducible in M90 (BackgroundFetchDelegateImpl::UpdateUI already has a guard similar to what was added https://crrev.com/c/2983039/3/chrome/browser/background_fetch/background_fetch_delegate_impl.cc and the CancelDowload change is not applicable)

### [Deleted User] (2021-12-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1214199?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056027)*
