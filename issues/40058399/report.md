# AddressSanitizer: heap-use-after-free in TryProcess ui/base/accelerators/accelerator_manager.cc:152:17

| Field | Value |
|-------|-------|
| **Issue ID** | [40058399](https://issues.chromium.org/issues/40058399) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-01-04 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4761.0 Safari/537.36

Steps to reproduce the problem:
This is found by my fuzzer running on ClusterFuzz, but it cannot be reproduced stably so ClusterFuzz does not automatically open a case.
https://clusterfuzz.com/testcase-detail/4785404576071680 (may require the security team to set permissions)

What is the expected behavior?

What went wrong?
Type of crash
browser process(may cause the sandbox escape)

Did this work before? N/A 

Chrome version: 99.0.4761.0  Channel: n/a
OS Version: 10.0

#Analysis

1. When AcceleratorPressed is called and the "case ui::VKEY_ESCAPE" condition is met[1], RemovePaneFocus will be called
2. RemovePaneFocus will call UnregisterAccelerator finally call the AcceleratorTargetInfo::Unregister function
3. AcceleratorTargetInfo::Unregister will modify targets_ without checking
4. Consider this situation,AcceleratorTargetInfo::TryProcess traverses targets_ and calls AcceleratorPressed[2], and AcceleratorPressed finally calls AcceleratorTargetInfo::Unregister to modify targets_, resulting in a UAF vulnerability

```
//ui/views/accessible_pane_view.cc:171
bool AccessiblePaneView::AcceleratorPressed(
    const ui::Accelerator& accelerator) {
  views::View* focused_view = focus_manager_->GetFocusedView();
  if (!ContainsForFocusSearch(this, focused_view))
    return false;

  using FocusChangeReason = views::FocusManager::FocusChangeReason;
  switch (accelerator.key_code()) {
    case ui::VKEY_ESCAPE: {
      RemovePaneFocus();		<<---[1]---
      View* last_focused_view = last_focused_view_tracker_->view();
      // Ignore |last_focused_view| if it's no longer in the same widget.
--CUT--
    case ui::VKEY_LEFT:

//ui/views/accessible_pane_view.cc:128
void AccessiblePaneView::RemovePaneFocus() {
  focus_manager_->RemoveFocusChangeListener(this);
  pane_has_focus_ = false;

  focus_manager_->UnregisterAccelerator(home_key_, this);
  focus_manager_->UnregisterAccelerator(end_key_, this);
  focus_manager_->UnregisterAccelerator(escape_key_, this);
  focus_manager_->UnregisterAccelerator(left_key_, this);
  focus_manager_->UnregisterAccelerator(right_key_, this);
}

//ui/base/accelerators/accelerator_manager.cc:132
bool AcceleratorManager::AcceleratorTargetInfo::Unregister(
    AcceleratorTarget* target) {
  DCHECK(!targets_.empty());

  // Only one priority handler is allowed, so if we remove the first element we
  // no longer have a priority target.
  if (targets_.front() == target)
    has_priority_handler_ = false;

  // Attempt to remove the target and return true if it was present.
  const size_t original_target_count = targets_.size();
  targets_.remove(target);
  return original_target_count != targets_.size();
}    

//ui/base/accelerators/accelerator_manager.cc:147
bool AcceleratorManager::AcceleratorTargetInfo::TryProcess(
    const Accelerator& accelerator) {
  DCHECK(!targets_.empty());

  for (AcceleratorTarget* target : targets_) {
    if (target->CanHandleAccelerators() &&
        target->AcceleratorPressed(accelerator)) {		<<---[2]---
      return true;
    }
  }

  return false;
}

```

#Patch
Not yet

#asan
=================================================================
==456431==ERROR: AddressSanitizer: heap-use-after-free on address 0x61a0001d16e0 at pc 0x55b833b72898 bp 0x7ffef31d64b0 sp 0x7ffef31d64a8
READ of size 8 at 0x61a0001d16e0 thread T0 (chrome)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x55b833b72897 in TryProcess ui/base/accelerators/accelerator_manager.cc:152:17
    #1 0x55b833b72897 in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator_manager.cc:83:27
    #2 0x55b833b6c78a in ProcessAccelerator ui/views/focus/focus_manager.cc:536:28
    #3 0x55b833b6c78a in views::FocusManager::OnKeyEvent(ui::KeyEvent const&) ui/views/focus/focus_manager.cc:113:7
    #4 0x55b833c837d2 in views::Widget::OnKeyEvent(ui::KeyEvent*) ui/views/widget/widget.cc:1479:27
    #5 0x55b82c364585 in DispatchEvent ui/events/event_dispatcher.cc:190:12
    #6 0x55b82c364585 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #7 0x55b82c363e3c in DispatchEventToTarget ui/events/event_dispatcher.cc:83:14
    #8 0x55b82c363e3c in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #9 0x55b82f49936d in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #10 0x55b82f4af04e in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent*) ui/aura/window_tree_host.cc:363:23
    #11 0x55b82df66aaa in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent*) const ui/base/ime/input_method_base.cc:138:33
    #12 0x55b82df6cfd1 in ui::InputMethodAuraLinux::DispatchKeyEvent(ui::KeyEvent*) ui/base/ime/linux/input_method_auralinux.cc:127:12
    #13 0x55b82f4915f3 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window*, ui::KeyEvent*) ui/aura/window_event_dispatcher.cc:1058:54
    #14 0x55b82f48f39f in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget*, ui::Event*) ui/aura/window_event_dispatcher.cc:546:15
    #15 0x55b82c363d35 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:51:34
    #16 0x55b82f49936d in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #17 0x55b82f4b855f in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #18 0x55b82f4b8159 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:143:12
    #19 0x55b833d5acf7 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:230:38
    #20 0x55b833d55070 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:284:29
    #21 0x55b82c37109b in Run base/callback.h:142:12
    #22 0x55b82c37109b in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:28:25
    #23 0x55b82e0c0152 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1304:3
    #24 0x55b82e0bf4ff in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1257:3
    #25 0x55b82e0c033c in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:0
    #26 0x55b82c3429a4 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:98:29
    #27 0x55b82df22fe4 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #28 0x55b81d01a1ba in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #29 0x55b81d019221 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #30 0x55b81d019221 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #31 0x55b82df30bb4 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #32 0x7f8dd2d2f049 in g_main_context_dispatch
0x61a0001d16e0 is located 96 bytes inside of 1224-byte region [0x61a0001d1680,0x61a0001d1b48)
freed by thread T0 (chrome) here:
    #0 0x55b81ba32c3d in operator delete(void*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x55b8351f4c81 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x55b8351f4c81 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x55b8351f4c81 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x55b8351f4c81 in LocationBarView::FinalizeChip() chrome/browser/ui/views/location_bar/location_bar_view.cc:849:3
    #5 0x55b835595d34 in FinalizeChip chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc:359:25
    #6 0x55b835595d34 in PermissionPromptImpl::~PermissionPromptImpl() chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc:127:7
    #7 0x55b835595e6d in PermissionPromptImpl::~PermissionPromptImpl() chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc:116:47
    #8 0x55b822e6320e in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #9 0x55b822e6320e in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #10 0x55b822e6320e in DeleteBubble components/permissions/permission_request_manager.cc:717:11
    #11 0x55b822e6320e in permissions::PermissionRequestManager::ResetViewStateForCurrentRequest() components/permissions/permission_request_manager.cc:739:5
    #12 0x55b822e61900 in permissions::PermissionRequestManager::FinalizeCurrentRequests(permissions::PermissionAction) components/permissions/permission_request_manager.cc:806:3
    #13 0x55b822e6403d in permissions::PermissionRequestManager::CleanUpRequests() components/permissions/permission_request_manager.cc:836:5
    #14 0x55b822e63824 in permissions::PermissionRequestManager::DidFinishNavigation(content::NavigationHandle*) components/permissions/permission_request_manager.cc:375:3
    #15 0x55b821c98099 in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&>(void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&) content/browser/web_contents/web_contents_impl.h:1502:9
    #16 0x55b821c99482 in content::WebContentsImpl::DidFinishNavigation(content::NavigationHandle*) content/browser/web_contents/web_contents_impl.cc:5515:16
    #17 0x55b82168af0d in content::NavigationRequest::~NavigationRequest() content/browser/renderer_host/navigation_request.cc:1703:20
    #18 0x55b82168db3d in content::NavigationRequest::~NavigationRequest() content/browser/renderer_host/navigation_request.cc:1662:41
    #19 0x55b8216e5498 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #20 0x55b8216e5498 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #21 0x55b8216e5498 in content::Navigator::DidNavigate(content::RenderFrameHostImpl*, content::mojom::DidCommitProvisionalLoadParams const&, std::__1::unique_ptr<content::NavigationRequest, std::__1::default_delete<content::NavigationRequest> >, bool) content/browser/renderer_host/navigator.cc:608:24
    #22 0x55b821734374 in content::RenderFrameHostImpl::DidCommitNavigationInternal(std::__1::unique_ptr<content::NavigationRequest, std::__1::default_delete<content::NavigationRequest> >, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::InlinedStructPtr<content::mojom::DidCommitSameDocumentNavigationParams>) content/browser/renderer_host/render_frame_host_impl.cc:10603:34
    #23 0x55b821731b9c in content::RenderFrameHostImpl::DidCommitNavigation(content::NavigationRequest*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>) content/browser/renderer_host/render_frame_host_impl.cc:11130:8
    #24 0x55b8217c5550 in Invoke<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), content::RenderFrameHostImpl *, content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams> > base/bind_internal.h:535:12
    #25 0x55b8217c5550 in MakeItSo<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), content::RenderFrameHostImpl *, content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams> > base/bind_internal.h:699:12
    #26 0x55b8217c5550 in RunImpl<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), std::__1::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl>, base::internal::UnretainedWrapper<content::NavigationRequest> >, 0UL, 1UL> base/bind_internal.h:772:12
    #27 0x55b8217c5550 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::*)(content::NavigationRequest*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), base::internal::UnretainedWrapper<content::RenderFrameHostImpl>, base::internal::UnretainedWrapper<content::NavigationRequest> >, void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>::RunOnce(base::internal::BindStateBase*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>&&, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>&&) base/bind_internal.h:741:12
    #28 0x55b81f9a124f in Run base/callback.h:142:12
    #29 0x55b81f9a124f in content::mojom::NavigationClient_CommitNavigation_ForwardToCallback::Accept(mojo::Message*) gen/content/common/navigation_client.mojom.cc:983:26
    #30 0x55b82a97e5ed in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:895:23
    #31 0x55b82a990ddd in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #32 0x55b82a982607 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:657:20
    #33 0x55b82c278851 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1008:24
    #34 0x55b82c272788 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:535:12
    #35 0x55b82c272788 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:699:12
    #36 0x55b82c272788 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:772:12
    #37 0x55b82c272788 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #38 0x55b829e48e43 in Run base/callback.h:142:12
    #39 0x55b829e48e43 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #40 0x55b829e88a73 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #41 0x55b829e88a73 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #42 0x55b829e88287 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #43 0x55b829e89641 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #44 0x55b829d4173a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #45 0x55b829e89d07 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #46 0x55b829dc3369 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #47 0x55b820a5aca0 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1048:18
previously allocated by thread T0 (chrome) here:
    #0 0x55b81ba323dd in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55b8351f4b1e in make_unique<PermissionRequestChip, Browser *, permissions::PermissionPrompt::Delegate *&, bool &> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x55b8351f4b1e in LocationBarView::DisplayChip(permissions::PermissionPrompt::Delegate*, bool) chrome/browser/ui/views/location_bar/location_bar_view.cc:835:18
    #3 0x55b835596e3d in PermissionPromptImpl::ShowChip() chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc:326:18
    #4 0x55b835595203 in make_unique<PermissionPromptImpl, Browser *&, content::WebContents *&, permissions::PermissionPrompt::Delegate *&> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:32
    #5 0x55b835595203 in CreatePermissionPrompt(content::WebContents*, permissions::PermissionPrompt::Delegate*) chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc:95:10
    #6 0x55b822e646c6 in Run base/callback.h:241:12
    #7 0x55b822e646c6 in permissions::PermissionRequestManager::ShowBubble() components/permissions/permission_request_manager.cc:674:25
    #8 0x55b822e6cfa0 in Invoke<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager> > base/bind_internal.h:535:12
    #9 0x55b822e6cfa0 in MakeItSo<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager> > base/bind_internal.h:719:5
    #10 0x55b822e6cfa0 in RunImpl<void (permissions::PermissionRequestManager::*)(), std::__1::tuple<base::WeakPtr<permissions::PermissionRequestManager> >, 0UL> base/bind_internal.h:772:12
    #11 0x55b822e6cfa0 in base::internal::Invoker<base::internal::BindState<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #12 0x55b829e48e43 in Run base/callback.h:142:12
    #13 0x55b829e48e43 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #14 0x55b829e88a73 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #15 0x55b829e88a73 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #16 0x55b829e88287 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #17 0x55b829e89641 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #18 0x55b829d4173a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #19 0x55b829e89d07 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #20 0x55b829dc3369 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #21 0x55b820a5aca0 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1048:18
    #22 0x55b820a5f655 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:153:15
    #23 0x55b820a54f07 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #24 0x55b828c11180 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:646:10
    #25 0x55b828c1424f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1160:10
    #26 0x55b828c13322 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1026:12
    #27 0x55b828c0bebc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:398:36
    #28 0x55b828c0dae4 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:426:10
    #29 0x55b81ba34c7e in ChromeMain chrome/app/chrome_main.cc:177:12
    #30 0x7f8dcbd9d82f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/libc-start.c:291
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chrome-test-builds_media_linux-release_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/asan-linux-release-955021/chrome+0x22b4b897) (BuildId: 94dba26ce7fec598)
Shadow bytes around the buggy address:
  0x0c3480032280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3480032290: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c34800322a0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c34800322b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c34800322c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c34800322d0: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd
  0x0c34800322e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c34800322f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3480032300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3480032310: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3480032320: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
==456431==ABORTING

## Attachments

- [clusterfuzz-testcase-4785404576071680.zip](attachments/clusterfuzz-testcase-4785404576071680.zip) (application/octet-stream, 71.2 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 14.7 KB)
- [clusterfuzz-testcase-5486264543150080.zip](attachments/clusterfuzz-testcase-5486264543150080.zip) (application/octet-stream, 116.8 KB)
- [Heap-use-after-free READ 8 · ui__AcceleratorManager__Process.pdf](attachments/Heap-use-after-free READ 8 · ui_AcceleratorManager_Process.pdf) (application/pdf, 3.8 MB)

## Timeline

### [Deleted User] (2022-01-04)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-01-04)

```
std::list<AcceleratorTarget*> targets_;
```
The initial analysis may be incorrect. It seems that the problem is because targets_ uses the a raw pointer to PermissionRequestChip, but AcceleratorManager is not get notified when PermissionRequestChip is freed, which leads to UAF.
still work on it~

### dr...@chromium.org (2022-01-05)

This does seem to reproduce sometimes on ClusterFuzz, so triaging to zentaro@chromium.org. The list of gestures is very long, so assigning medium severity for now. m.cooolie@ - if you get a cleaner reproduction, we may want to upgrade this.

[Monorail components: UI>Browser>Accessibility]

### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-01-07)

LocationBarView::FinalizeChip will call to View::UnregisterAccelerators, and finally call UnregisterAccelerators to unregister itself. So UAF can happen, one of the conditional statements must be returned earlier, but I am not familiar with this piece and I don’t know how to create this situation.

```
ui/views/view.cc:3110
void View::UnregisterAccelerators(bool leave_data_intact) {
  if (!accelerators_)
    return;

  if (GetWidget()) {
    if (accelerator_focus_manager_) {
      accelerator_focus_manager_->UnregisterAccelerators(this);
      accelerator_focus_manager_ = nullptr;
    }
```

### ze...@chromium.org (2022-01-10)

I'm taking a look as I get a chance today, but it seems like while the problem does manifest in the accelerator controller - it's actually because another component is not managing it's lifetime correctly.

I'm going to try and get a better understanding of the lifetime here, but likely will reassign to the owner of the LocationBar/AccessibilityPane unless I see something directly wrong int he accelerator controller.

### ze...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### ze...@chromium.org (2022-01-11)

The lifetime here isn't controlled by the accelerator controller. The LocationBarView and chip need to control it's own lifetime wrt to it's interaction with the accelerator controller.

Not sure who the right owner of this is, but the chip needs to unregister itself before it deletes itself.

### el...@chromium.org (2022-01-12)

@m.cooolie a link [1] in the description says "Invalid test case!". Could you please double-check that it is a correct one. 

[1] https://clusterfuzz.com/testcase-detail/4785404576071680

### el...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-01-12)

re https://crbug.com/chromium/1284293#c13
Is it impossible to reproduce stably and cause clusterfuzz to be automatically deleted? I have seen some cases that cannot be reproduced stably, and there will be such a description"Will be auto-deleted on Wed, Jan 19, 2022 if flaky crash no longer seen"

### m....@gmail.com (2022-01-12)

I have a test case backup

### el...@chromium.org (2022-01-14)

Thank you for the backup! I wasn't able to reproduce the crash.

zentaro@ based on LocationBarView::FinalizeChip() and that line [1] chip as a view unregisters itself. Because there is no a clear way to reproduce it,  I'm removing the release block label. 

[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/views/view.cc;l=2653;drc=054e08864177603f17edbc111db7ebc8586906bd 

### [Deleted User] (2022-01-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-01-19)

clusterfuzz give a new one.
https://clusterfuzz.com/testcase-detail/5486264543150080


### m....@gmail.com (2022-01-21)

RE https://crbug.com/chromium/1284293#c17

#RCA
1. When TryProcess is called, a AcceleratorTargetInfo object is copied to prevent targets_ from being modified[1]
2. This will also lead to UAF, because when target is unregistered[2], the object pointer is still kept in the copied list.
3. The attached ASAN log is exactly what UAF caused by this situation

ps.Please CC the security team and ask them to link https://clusterfuzz.com/testcase-detail/5486264543150080 to this ISSUE, otherwise clusterfuzz will delete 5486264543150080 soon

```
bool AcceleratorManager::Process(const Accelerator& accelerator) {
  const AcceleratorTargetInfo* target_info = accelerators_.Find(accelerator);
  if (!target_info)
    return false;

  // If the accelerator is in the map, the target list should not be empty.
  DCHECK(target_info->HasTargets());

  // We have to copy the target list here, because processing the accelerator
  // event handler may modify the list.
  AcceleratorTargetInfo target_info_copy(*target_info);		<<[1]
  return target_info_copy.TryProcess(accelerator);
}


void AcceleratorManager::Unregister(const Accelerator& accelerator,
                                    AcceleratorTarget* target) {
  DCHECK(target);
  AcceleratorTargetInfo* target_info = accelerators_.Find(accelerator); <<[2]
  DCHECK(target_info) << "Unregistering non-existing accelerator";

  const bool was_registered = target_info->Unregister(target);
  DCHECK(was_registered) << "Unregistering accelerator for wrong target";

  // If the last target for the accelerator is removed, then erase the
  // entry from the map.
  if (!target_info->HasTargets())
    accelerators_.Erase(accelerator);
}
```


### ze...@chromium.org (2022-01-24)

I still haven't had a chance to take another look at this bug. Will take a second look tomorrow.

### ze...@chromium.org (2022-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

ashleydp: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@google.com (2022-01-26)

[Empty comment from Monorail migration]

### as...@google.com (2022-01-26)

Which ClusterFuzz test is being run and how do I get access?

### as...@google.com (2022-01-27)

In addition to access, can I also get instructions on how to run the test locally?

### m....@gmail.com (2022-01-27)

Re https://crbug.com/chromium/1284293#c26 
This link https://clusterfuzz.com/testcase-detail/5486264543150080 requires the security team to set permissions. I will provide a backup here, but the testcase cannot be reproduced stably, so manual analysis may be required. I am also looking at it, but I have not been able to reproduce.

### ze...@chromium.org (2022-01-27)

One thing I just realized which possibly affects the severity of this is that there appears to be non-default flags enabled.

The memory in question here is a PermissionChip that was created in PermissionPromptImpl::ShowChip()

All 3 calls to ShowChip are gaurded by the function ShouldCurrentRequestUseChip() or ShouldCurrentRequestUseQuietChip()

chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc on lines 164, 276, 285

Those two functions require the following features enabled 

permissions::features::kPermissionChip
permissions::features::kPermissionQuietChip

These features are both off by default;

https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/features.cc;l=32
https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/features.cc;l=38

Based on that this issue was introduced with this CL:

- https://chromium-review.googlesource.com/c/chromium/src/+/2690644


So are we enabling non-default flags in the fuzzers?

Based on this - if we have finch experiments with this flag we should stop them, but otherwise this code path doesn't seem possible without these flags being on.

That being said I haven't yet identified where in the lifecycle mangement something went wrong here.


### ze...@chromium.org (2022-01-28)

Also elklm@

There's lots of out of date references to the flag quiet-notification-prompts
https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_prompt.h;l=74;bpv=1;bpt=1?q=quiet-notification-prompts

And looks like that was removed here - https://chromium-review.googlesource.com/c/chromium/src/+/3231316



### el...@chromium.org (2022-01-28)

Both kPermissionChip and kPermissionQuietChip are currently at 1% stable. 

Thank you regarding `quiet-notification-prompts`, I will clean up comments.

### en...@chromium.org (2022-01-28)

I assume the fuzzer is using `fieldtrial_testing_config.json`, and this is how these features get enabled? See:
https://source.chromium.org/chromium/chromium/src/+/main:testing/variations/fieldtrial_testing_config.json;l=4769-4808;drc=650a0403dca1c2315462ea227e5d06318e333cb1

 1) Given that these launches are on the critical path and blocking other important launches, it is critical for us to track this down and fix as soon as possible. It looks like deterministic repro is hard, do we have enough confidence in our static code analysis to fix the logic error it without being able to repro?

 2) Was this regression introduced in M99, or does it affect the current/upcoming Stable versions (97 and 98) as well?

 3) Is "Medium" still the appropriate severity given what we learned about this issue? Did we come up with more streamlined repro paths? https://crbug.com/chromium/1284293#c3 refers to many user gestures needed, but I am not sure where that information is coming from.

If the issue does affect Stable, and if we decide that the severity is "High", we should put both the Permission Chip and the Permission Quiet Chip experiments on hold until we figure this out, that is, do not move forward to 10% and also roll back the 1% Stable experiment. So it sounds like answering questions (2) and (3) are the first steps here.

### ze...@chromium.org (2022-01-28)

1) Given that we didn't realize that these flags needed to be enabled - it's not surprising no-one was able to repro. 

That seems like a bit of flaw in the reporting of these bugs. If we are randomly enabling flags while fuzzing, it would be useful to get a summary of what flags were changed or at least their current state so that we don't waste time trying to repro something in a state that could never happen.

And are we able to re-run such a fuzzer ensuring that these flags are always on?

Additionally the link to the fuzzer results is now dead again.

2) It appears so far to have been introduced in the CL in #28 which is M93 (behind the flag). But that's not conclusive, something after the feature was introduced could have broken the lifecycle management. But given that literally every View in the system registers and unregisters itself successfully with the accelerator manager and we aren't seeing similar issues with anything but this PermissionChip - I'm inclined to think there is something specific about the way this component specifically is being handled.

3) Given that it's behind a flag, I think we should stop the finch experiment and this can be medium in terms of security. If the feature is of high importance from a product perspective that's a different issue, we need to solve the problem before enabling the feature again. But the security risk is not there if the flag is off.

Now that we know these flags have to be on we can have another attempt at repro'ing. From the asan.txt is #20 it looked like finalization/destruction of the chip happen due to a change in fullscreen state. I did try to repro this scenario ie. trigger a permission, then try to go fullscreen. However with the default bubble it blocks the fullscreen request, and that's how I realized that this code path isn't even possible.

So that would be the next manual thing I would check is show the chip then try to go full screen or vice versa.

### ze...@chromium.org (2022-01-28)

Looking a little closer the state here is that only one of the flags are enabled not both. Based on the fact that the Chip is of type PermissionRequestType not PermissionQuietChip and the stack include LocationBarView::DisplayChip not LocationBarView::DisplayQuietChip.

Based on that the state of the flags are;

permissions::features::kPermissionChip              <- Set to true
permissions::features::kPermissionQuietChip     <- Leave false

### ze...@chromium.org (2022-01-28)

In #33 where I said PermissionRequestType I meant PermissionRequestChip

### ze...@chromium.org (2022-01-31)

I tried experimenting with going full screen while the chip is shown and still can't repro.

re#20 - Can you actually confirm with a known code path that an item in the list is being deleted during TryProcess? And is this the only use case that does this?

I'm not going to have time to keep investigating this week.

### ze...@chromium.org (2022-02-01)

I'm removing the RBS label since this can't be repro'd and based on analysis this can only happen with non-default flags enabled.

### ze...@chromium.org (2022-02-01)

Can one of the owners of this feature continue the investigation here?

### [Deleted User] (2022-02-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2022-02-01)

In the meantime elklm@ found a deterministic repro and is working on a fix. Going to update this thread shortly.

### el...@chromium.org (2022-02-01)

I was able to reproduce it.

Requirements:
OS (where I was able to verify): Linux or Windows
Version: Stable 97.0.4692.99
Enabled flags: #permission-chip (optional #permission-quiet-chip for the quiet prompts)

Steps:
1. navigate to https://permission.site/
2. Click on "Location" button. A permission prompt in form of a chip will be shown.
3. Press F6. The chip will be focused.
4. Go to a Chrome menu (3 dots) and click on a full screen icon (near Zoom). The browser will go into the fullscreen mode. The location bar will be removed, the chip will be removed as well. the permission request will be displayed in form of the default permission prompt bubble.
5. Close the bubble via X. (or any other buttons)
6. press Esc or left / right arrows key. 


I assume that CromeOS and MacOS are affected as well.

### en...@chromium.org (2022-02-01)

Quick alternative: In Step (4), pressing F11 works too.

### el...@chromium.org (2022-02-01)

Alternative steps (no fullscreen needed):

1. Navigate to https://permission.site/
2. Click on "Location" button. A permission prompt in form of a chip will be shown.
3. Press F6 to focus the chip.
4. Wait around 18 seconds until chip disappears. 
6. Press Esc or left / right arrows key. 

### gi...@appspot.gserviceaccount.com (2022-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7125ad12cdfd41bce01723aa4769b853e655d8de

commit 7125ad12cdfd41bce01723aa4769b853e655d8de
Author: Illia Klimov <elklm@google.com>
Date: Wed Feb 02 16:18:26 2022

Unregister Accelerators when AccessiblePaneView is destroyed.

This CL makes sure that a focus change listener and all Accelerators are
unregistered when the AccessiblePaneView is going to be destroyed.

Bug: 1284293
Change-Id: Icd11523be7ab5728e181148a8fd1baec5349513e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3429899
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#966217}

[modify] https://crrev.com/7125ad12cdfd41bce01723aa4769b853e655d8de/ui/views/accessible_pane_view.cc


### el...@chromium.org (2022-02-02)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

Merge review required: M99 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-03)

Merge review required: M98 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2022-02-03)

Label clean-up:
 -- Removing RBS, because the UAF is in a Finch-controlled feature.
 -- Tentatively setting severity to high given the minimized repro with relatively few user interactions needed (see https://crbug.com/chromium/1284293#c42).
 -- Targeting M98, we would like to catch the stable respin going out on Feb 15.

@elklm, let's turn off the 1% experiment until the fix lands on Stable.

### en...@chromium.org (2022-02-03)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

High-severity security issue that is blocking the roll-out of three Finch-controlled launches.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3429899

3. Have the changes been released and tested on canary?
Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
This is a memory safety issue in a new feature, that is being rolled out using Finch, and is presently at 50% of Canary/Dev/Beta and 1% of Stable (we will roll this latter back until the fix lands on Stable).

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
The product team verified on macOS and Windows, but manual verification would be good. See repro steps in https://crbug.com/chromium/1284293#c40 and #42.

### am...@chromium.org (2022-02-05)

Thanks for all the information, from a security perspective, the amount of user gesture in https://crbug.com/chromium/1284293#c42 is not what we would consider minimal or relatively few, but this is a browser process UAF and the amount of user gesture does make this rather borderline medium. Feature blocking prioritization is important, but should be considered separate from security severity or security impact decisions. That being said, it's preferable that -when changes to security severity are made outside the sheriffs decisions - it occurs when erring on the side of caution by raising the severity rather than lowering. 

Merge approved to M99, please merge to branch 4844 at your earliest convenience. 


### gi...@appspot.gserviceaccount.com (2022-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1d216da25a847e2acb53d42df543d0f6cb2c8f62

commit 1d216da25a847e2acb53d42df543d0f6cb2c8f62
Author: Illia Klimov <elklm@google.com>
Date: Mon Feb 07 17:45:55 2022

Unregister Accelerators when AccessiblePaneView is destroyed.

This CL makes sure that a focus change listener and all Accelerators are
unregistered when the AccessiblePaneView is going to be destroyed.

(cherry picked from commit 7125ad12cdfd41bce01723aa4769b853e655d8de)

Bug: 1284293
Change-Id: Icd11523be7ab5728e181148a8fd1baec5349513e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3429899
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#966217}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3440398
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/4844@{#305}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/1d216da25a847e2acb53d42df543d0f6cb2c8f62/ui/views/accessible_pane_view.cc


### [Deleted User] (2022-02-07)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2022-02-08)

Updating FoundIn milestone to M97, which is the earliest version where the permission chip / quiet chip was enabled (for a 1% Stable experiment).

In the meantime:
 -- We have investigated potentially simplifying the repro, and believe there might exist a more robust POC where the only user interaction needed is pressing F6, which makes us lean more toward the High severity rating.
 -- We have rolled back the 1% Stable Finch experiments with PermissionChip/PermissionQuietChip on Monday, and will restart once the fix lands on Stable, but with the understanding that the security severity or security impact decisions will be made independently from launch plans for the feature.

### am...@chromium.org (2022-02-09)

thank you for adding these updates, engedy@! 

Given the simplified repro and how the commit's (7125ad12cdfd41bce01723aa4769b853e655d8de) performance on canary and dev, merge approved to M98, please go ahead and merge to branch 4758 by EOD Thursday, 10 February so this fix can be included in next week's Stable channel respin -- thank you! 

### rz...@google.com (2022-02-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-09)

1. Number of CLs needed for this fix and links to them.
1 CL, https://crrev.com/c/3449214

2. Level of complexity (High, Medium, Low - Explain)
Low, no conflicts

3. Has this been merged to a stable release? beta release?
98, 99

4. Overall Recommendation (Yes, No)
Yes

### gm...@google.com (2022-02-09)

Merge reject as it's behind flag and not Applicable for M96.

### gm...@google.com (2022-02-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aed01dce16abfb7f98b800785ddd2d265ba2b570

commit aed01dce16abfb7f98b800785ddd2d265ba2b570
Author: Illia Klimov <elklm@google.com>
Date: Wed Feb 09 17:25:13 2022

[M96-LTS] Unregister Accelerators when AccessiblePaneView is destroyed.

This CL makes sure that a focus change listener and all Accelerators are
unregistered when the AccessiblePaneView is going to be destroyed.

(cherry picked from commit 7125ad12cdfd41bce01723aa4769b853e655d8de)

Bug: 1284293
Change-Id: Icd11523be7ab5728e181148a8fd1baec5349513e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3429899
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#966217}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449214
Reviewed-by: Illia Klimov <elklm@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1464}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/aed01dce16abfb7f98b800785ddd2d265ba2b570/ui/views/accessible_pane_view.cc


### gi...@appspot.gserviceaccount.com (2022-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/068ee7a3c1ef206a43e4e0ebf1bb05296e553457

commit 068ee7a3c1ef206a43e4e0ebf1bb05296e553457
Author: Illia Klimov <elklm@google.com>
Date: Wed Feb 09 17:37:20 2022

[M98] Unregister Accelerators when AccessiblePaneView is destroyed.

This CL makes sure that a focus change listener and all Accelerators are
unregistered when the AccessiblePaneView is going to be destroyed.

(cherry picked from commit 7125ad12cdfd41bce01723aa4769b853e655d8de)

Bug: 1284293
Change-Id: Icd11523be7ab5728e181148a8fd1baec5349513e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3429899
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#966217}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3450213
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#1121}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/068ee7a3c1ef206a43e4e0ebf1bb05296e553457/ui/views/accessible_pane_view.cc


### gi...@appspot.gserviceaccount.com (2022-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/86a179919cb880bfc1cfafa22ba4934ac7f4fe9c

commit 86a179919cb880bfc1cfafa22ba4934ac7f4fe9c
Author: Illia Klimov <elklm@chromium.org>
Date: Wed Feb 09 17:48:33 2022

Revert "[M96-LTS] Unregister Accelerators when AccessiblePaneView is destroyed."

This reverts commit aed01dce16abfb7f98b800785ddd2d265ba2b570.

Reason for revert: The merge into M96 was rejected.

Original change's description:
> [M96-LTS] Unregister Accelerators when AccessiblePaneView is destroyed.
>
> This CL makes sure that a focus change listener and all Accelerators are
> unregistered when the AccessiblePaneView is going to be destroyed.
>
> (cherry picked from commit 7125ad12cdfd41bce01723aa4769b853e655d8de)
>
> Bug: 1284293
> Change-Id: Icd11523be7ab5728e181148a8fd1baec5349513e
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3429899
> Commit-Queue: Illia Klimov <elklm@chromium.org>
> Cr-Original-Commit-Position: refs/heads/main@{#966217}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449214
> Reviewed-by: Illia Klimov <elklm@chromium.org>
> Reviewed-by: Peter Kasting <pkasting@chromium.org>
> Commit-Queue: Peter Kasting <pkasting@chromium.org>
> Cr-Commit-Position: refs/branch-heads/4664@{#1464}
> Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

Bug: 1284293
Change-Id: I4533e15589e90850bb82a178ae7cdb454c64ef45
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3447255
Auto-Submit: Illia Klimov <elklm@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1465}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/86a179919cb880bfc1cfafa22ba4934ac7f4fe9c/ui/views/accessible_pane_view.cc


### el...@chromium.org (2022-02-09)

To avoid confusion, we prepared a CL for the M96 merge in advance and accidentally submitted it. The CL was reverted because the M96 merge request was rejected.

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thanks for your efforts and reporting this issue to us! 

### m....@gmail.com (2022-02-12)

re https://crbug.com/chromium/1284293#c68 Thanks.
This one also found through ClusterFuzzcan i get  Fuzzer Bonus for this~

### am...@chromium.org (2022-02-14)

Sorry, we could track this report down anywhere on clusterfuzz unfortunately. The fuzzer bonus is rewarded when your fuzzer running on ClusterFuzz automatically produces the report complete with test case, data from reproduction, such as symbolized stack trace and mitigating the need for a lot of security and developer time to reproduce and hunt down relevant data. Also, fuzzer bonus is offered to reward for the fuzzer reliably producing consistent future reports if a similar issue is encountered, without the need for human intervention to file the report. So, unfortunately, we are unable to provide the fuzzer bonus in these cases. 

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/340bb1764ae05f1c059e79e770e6bb3044cfff40

commit 340bb1764ae05f1c059e79e770e6bb3044cfff40
Author: Illia Klimov <elklm@google.com>
Date: Tue Feb 15 18:49:27 2022

Reland "[M96-LTS] Unregister Accelerators when AccessiblePaneView is destroyed."

This is a reland of aed01dce16abfb7f98b800785ddd2d265ba2b570

Original change's description:
> [M96-LTS] Unregister Accelerators when AccessiblePaneView is destroyed.
>
> This CL makes sure that a focus change listener and all Accelerators are
> unregistered when the AccessiblePaneView is going to be destroyed.
>
> (cherry picked from commit 7125ad12cdfd41bce01723aa4769b853e655d8de)
>
> Bug: 1284293,1295221
> Change-Id: Icd11523be7ab5728e181148a8fd1baec5349513e
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3429899
> Commit-Queue: Illia Klimov <elklm@chromium.org>
> Cr-Original-Commit-Position: refs/heads/main@{#966217}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449214
> Reviewed-by: Illia Klimov <elklm@chromium.org>
> Reviewed-by: Peter Kasting <pkasting@chromium.org>
> Commit-Queue: Peter Kasting <pkasting@chromium.org>
> Cr-Commit-Position: refs/branch-heads/4664@{#1464}
> Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

Bug: 1295221
Change-Id: I14a2bb210c190dcc245221766d4199b9fe46b04c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3461534
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Illia Klimov <elklm@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1474}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/340bb1764ae05f1c059e79e770e6bb3044cfff40/ui/views/accessible_pane_view.cc


### [Deleted User] (2022-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1284293?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1295221]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058399)*
