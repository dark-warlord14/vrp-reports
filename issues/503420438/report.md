# Security: Heap-use-after-free in PasskeyResetWebContentsObserver::MaybeRunCallback


| Field | Value |
|-------|-------|
| **Issue ID** | [503420438](https://issues.chromium.org/issues/503420438) |
| **Status** | Verified |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Chrome Version** | 147.0.0.0 |
| **Reporter** | me...@gmail.com |
| **Created** | 2026-04-17 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Apply `change.diff` to Chromium and compile with ASAN enabled
2. Start the PoC HTTP server: `python3 server.py` (from the `poc/` directory)
3. Run Chrome: `./out/asan/chrome --no-sandbox --gaia-url=http://localhost:8080 http://localhost:8080/`
4. Wait until the popup show, click the "Next" button, UAF occurs.

# Problem Description

## Introduction

Please note that this is the re-submit of [issue 503013396](https://issues.chromium.org/issues/503013396), the new patch don't need to patch the CHECK in ~WebContents. And all the patch is made to show the popup, which doesn't influence the logic to trigger the UAF.
This is a security vulnerability in the browser process that **does not** rely on a compromised renderer, but it requires a essential user interaction. The `change.diff` file is used solely to simulate a GPM enclave passkey-reset flow without a real Google account(Just in order to show the popup in Chromium) and does not influence Chrome's original logic.

## Bisect

This issue is introduced in this commit: 55e4d79e7a5923e18ab7f0a06107ac32e67f2035
This affect Stable 128.0.6613.84.

## Patch Explanation

### 1. `chrome_web_authentication_delegate.cc`

`BrowserProvidedPasskeysAvailable` returns `false` when no account is signed in, blocking the enclave path. Change `false` → `true` to bypass this gate.

### 2. `chrome_authenticator_request_delegate.cc`

Invert `HasPrimaryAccount` → `!HasPrimaryAccount` so `GPMEnclaveController` is constructed when there is no account, instead of when there is one.

### 3. `gpm_enclave_controller.cc`

`OnEnclaveLoaded` normally fetches account state from Google's servers. Append a synchronous fake call to `OnAccountStateDownloaded` with `kIrrecoverable` state so the UI proceeds immediately without a real network response.

### 4. `authenticator_request_dialog_model.cc`

The `kGPMTrustThisComputerCreation` dialog calls `GetGpmAccountEmail()`, which CHECKs for a signed-in account. Replace the CHECK with a null guard so it returns `""` instead of crashing.

### 5. `authenticator_request_window.cc`

- **URLs → localhost:8080**: so our server can trigger `MaybeRunCallback` via HTTP redirect.

# Additional Comments

## Analysis

**Vulnerability Summary**

The vulnerability is a **Use-After-Free (UAF)** caused by the synchronous execution of a callback that deletes the `this` object. Subsequent write to a member variable of the deleted object results in memory corruption.

In `MaybeRunCallback` **[1]**, `std::move(callback_).Run(true)` synchronously invokes `OnPasskeysReset` on the owning `AuthenticatorRequestWindow`. That call chain reaches `CloseWindowAndDeleteSelf()` **[3]**, which executes `delete this` on `AuthenticatorRequestWindow`, destroying the `passkey_reset_observer_` `unique_ptr` member **[4]** and freeing the `PasskeyResetWebContentsObserver` (i.e., `this` inside `MaybeRunCallback`). Control returns to `MaybeRunCallback` and the next line writes `status_ = Status::kNotStarted` **[1]** to the freed object, triggering a **heap-use-after-free WRITE**.

```
  void MaybeRunCallback(const std::string& ref) {
    if (status_ == Status::kStarted || ref.empty()) {
      return;
    }
    if (status_ == Status::kSuccess && ref == "success") {
      std::move(callback_).Run(true);   //@audit: callback synchronously deletes |this|
    } else if (status_ == Status::kFail && ref == "fail") {
      std::move(callback_).Run(false);
    }
    status_ = Status::kNotStarted;     //@audit: |this| has been freed, UAF WRITE occurs
  }

```

The `base::Unretained(this)` comment at the callback binding site **[4]** incorrectly states that the observer's existence guarantees the owner's existence — but `OnPasskeysReset` is exactly the path that deletes the owner:

```
        passkey_reset_observer_ =
            std::make_unique<PasskeyResetWebContentsObserver>(
                web_contents.get(),
                // Unretained: `passkey_reset_observer_` is owned by this
                // object so if it exists, this object also exists.   //@audit: wrong; OnPasskeysReset deletes the owner
                base::BindOnce(&AuthenticatorRequestWindow::OnPasskeysReset,
                               base::Unretained(this)));

```

**Execution Path to Free:**

The destruction path starts from `callback_.Run(true)` in `MaybeRunCallback` **[1]**, which calls `AuthenticatorRequestWindow::OnPasskeysReset` **[2]**, which calls `model_->OnGPMPasskeysReset(true)` **[5]**, which calls `model_->SetStep(kGPMCreatePin)`. `SetStep` synchronously iterates observers and calls `OnStepTransition()` **[3]** on `AuthenticatorRequestWindow`. Since the new step is not `kGPMRecoverSecurityDomain`, `CloseWindowAndDeleteSelf()` is called, executing `delete this` on `AuthenticatorRequestWindow` **[3]**, which destroys the `passkey_reset_observer_` `unique_ptr` **[4]**, freeing `PasskeyResetWebContentsObserver`. Control returns to `MaybeRunCallback` line 157 where `status_ = Status::kNotStarted` writes to freed memory.

```
  void OnPasskeysReset(bool success) {   // [2]
    if (model_) {
      model_->OnGPMPasskeysReset(success);
    }
  }

```
```
  void OnStepTransition() override {   // [3]
    if (model_->step() != step_) {
      CloseWindowAndDeleteSelf();
    }
  }

  void CloseWindowAndDeleteSelf() {   // [3]
    if (web_contents_weak_ptr_) {
      web_contents_weak_ptr_->Close();
    }
    delete this;   //@audit: destroys passkey_reset_observer_, freeing PasskeyResetWebContentsObserver
  }

```
```
  std::unique_ptr<PasskeyResetWebContentsObserver> passkey_reset_observer_;   // [4]

```
```
void GPMEnclaveController::OnGPMPasskeysReset(bool success) {   // [5]
  CHECK(model_->step() == Step::kGPMRecoverSecurityDomain);
  ...
  model_->SetStep(AuthenticatorRequestDialogModel::Step::kGPMCreatePin);
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webauthn/authenticator_request_window.cc;l=148>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webauthn/authenticator_request_window.cc;l=323>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webauthn/authenticator_request_window.cc;l=301>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webauthn/authenticator_request_window.cc;l=221>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/webauthn/gpm_enclave_controller.cc;l=1437>

# Summary

Security: Heap-use-after-free in PasskeyResetWebContentsObserver::MaybeRunCallback

# Custom Questions

#### Type of crash:

browser

#### Crash state:

```
=================================================================
==2852092==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bb8f865af30 at pc 0x55620e06b649 bp 0x7ffdb42babf0 sp 0x7ffdb42babe8
WRITE of size 4 at 0x7bb8f865af30 thread T0 (chrome)
    #0 0x55620e06b648 in (anonymous namespace)::PasskeyResetWebContentsObserver::DidFinishNavigation(content::NavigationHandle*) chrome/browser/ui/webauthn/authenticator_request_window.cc:157:13
    #1 0x7f795f56c314 in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&>(void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&) content/browser/web_contents/web_contents_impl.h:1838:9
    #2 0x7f795f56dbda in content::WebContentsImpl::DidFinishNavigation(content::NavigationHandle*) content/browser/web_contents/web_contents_impl.cc:7645:16
    #3 0x7f795eb4c589 in content::NavigationRequest::~NavigationRequest() content/browser/renderer_host/navigation_request.cc:2424:20
    #4 0x7f795eb53c2d in content::NavigationRequest::~NavigationRequest() content/browser/renderer_host/navigation_request.cc:2301:41
    #5 0x7f795ec1719a in content::Navigator::DidNavigate(content::RenderFrameHostImpl*, content::mojom::DidCommitProvisionalLoadParams const&, std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest>>, bool, bool) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #6 0x7f795eca1e6e in content::RenderFrameHostImpl::DidCommitNavigationInternal(std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest>>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitSameDocumentNavigationParams>, base::TimeTicks const&) content/browser/renderer_host/render_frame_host_impl.cc:16456:58
    #7 0x7f795eca3b76 in content::RenderFrameHostImpl::DidCommitSameDocumentNavigation(mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitSameDocumentNavigationParams>) content/browser/renderer_host/render_frame_host_impl.cc:6604:8
    #8 0x7f795c58a5e2 in content::mojom::FrameHostStubDispatch::Accept(content::mojom::FrameHost*, mojo::Message*) gen/content/common/frame.mojom.cc:5932:13
    #9 0x7f797c394042 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #10 0x7f797c3ab300 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #11 0x7f797c3998f4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #12 0x7f796da28cc7 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ipc/ipc_mojo_bootstrap.cc:1199:24
    #13 0x7f796da2af8d in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #14 0x7f797bbf6209 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #15 0x7f797bc70750 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #16 0x7f797bc6f726 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #17 0x7f797be48449 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #18 0x7f797bc71da3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #19 0x7f797bb61652 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #20 0x7f795d775703 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1103:18
    #21 0x7f795d77d976 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:151:15
    #22 0x7f795d76cbb5 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:32:28
    #23 0x7f7960c17715 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:696:10
    #24 0x7f7960c1ae3d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1320:10
    #25 0x7f7960c1a396 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:12
    #26 0x7f7960c14ab3 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:356:36
    #27 0x7f7960c14e3a in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10
    #28 0x556207fbfb75 in ChromeMain chrome/app/chrome_main.cc:194:12
    #29 0x7f790776c082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x7bb8f865af30 is located 32 bytes inside of 48-byte region [0x7bb8f865af10,0x7bb8f865af40)
freed by thread T0 (chrome) here:
    #0 0x556207fbe822 in operator delete(void*, unsigned long) (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67e9822) (BuildId: 6f42fc6d99176868)
    #1 0x55620e06a134 in (anonymous namespace)::AuthenticatorRequestWindow::~AuthenticatorRequestWindow() gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x55620e06a25d in (anonymous namespace)::AuthenticatorRequestWindow::~AuthenticatorRequestWindow() chrome/browser/ui/webauthn/authenticator_request_window.cc:269:42
    #3 0x55620e06a878 in (anonymous namespace)::AuthenticatorRequestWindow::OnStepTransition() chrome/browser/ui/webauthn/authenticator_request_window.cc:314:5
    #4 0x55621038721a in AuthenticatorRequestDialogModel::SetStep(AuthenticatorRequestDialogModel::Step) chrome/browser/webauthn/authenticator_request_dialog_model.cc:178:14
    #5 0x556210439ffe in GPMEnclaveController::OnGPMPasskeysReset(bool) chrome/browser/webauthn/gpm_enclave_controller.cc:1446:11
    #6 0x5562103997ff in AuthenticatorRequestDialogModel::OnGPMPasskeysReset(bool) chrome/browser/webauthn/authenticator_request_dialog_model.cc:255:1
    #7 0x55620e06b8f6 in base::internal::Invoker<base::internal::FunctorTraits<void ((anonymous namespace)::AuthenticatorRequestWindow::*&&)(bool), (anonymous namespace)::AuthenticatorRequestWindow*>, base::internal::BindState<true, true, false, void ((anonymous namespace)::AuthenticatorRequestWindow::*)(bool), base::internal::UnretainedWrapper<(anonymous namespace)::AuthenticatorRequestWindow, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (bool)>::RunOnce(base::internal::BindStateBase*, bool) base/functional/bind_internal.h:740:12
    #8 0x55620e06b3b5 in (anonymous namespace)::PasskeyResetWebContentsObserver::DidFinishNavigation(content::NavigationHandle*) base/functional/callback.h:155:12
    #9 0x7f795f56c314 in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&>(void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&) content/browser/web_contents/web_contents_impl.h:1838:9
    #10 0x7f795f56dbda in content::WebContentsImpl::DidFinishNavigation(content::NavigationHandle*) content/browser/web_contents/web_contents_impl.cc:7645:16
    #11 0x7f795eb4c589 in content::NavigationRequest::~NavigationRequest() content/browser/renderer_host/navigation_request.cc:2424:20
    #12 0x7f795eb53c2d in content::NavigationRequest::~NavigationRequest() content/browser/renderer_host/navigation_request.cc:2301:41
    #13 0x7f795ec1719a in content::Navigator::DidNavigate(content::RenderFrameHostImpl*, content::mojom::DidCommitProvisionalLoadParams const&, std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest>>, bool, bool) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #14 0x7f795eca1e6e in content::RenderFrameHostImpl::DidCommitNavigationInternal(std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest>>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitSameDocumentNavigationParams>, base::TimeTicks const&) content/browser/renderer_host/render_frame_host_impl.cc:16456:58
    #15 0x7f795eca3b76 in content::RenderFrameHostImpl::DidCommitSameDocumentNavigation(mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitSameDocumentNavigationParams>) content/browser/renderer_host/render_frame_host_impl.cc:6604:8
    #16 0x7f795c58a5e2 in content::mojom::FrameHostStubDispatch::Accept(content::mojom::FrameHost*, mojo::Message*) gen/content/common/frame.mojom.cc:5932:13
    #17 0x7f797c394042 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #18 0x7f797c3ab300 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #19 0x7f797c3998f4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #20 0x7f796da28cc7 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ipc/ipc_mojo_bootstrap.cc:1199:24
    #21 0x7f796da2af8d in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #22 0x7f797bbf6209 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #23 0x7f797bc70750 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #24 0x7f797bc6f726 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #25 0x7f797be48449 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #26 0x7f797bc71da3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #27 0x7f797bb61652 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #28 0x7f795d775703 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1103:18
    #29 0x7f795d77d976 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:151:15

previously allocated by thread T0 (chrome) here:
    #0 0x556207fbdc1d in operator new(unsigned long) (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67e8c1d) (BuildId: 6f42fc6d99176868)
    #1 0x55620e069193 in ShowAuthenticatorRequestWindow(content::WebContents*, AuthenticatorRequestDialogModel*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26
    #2 0x556210386ea0 in AuthenticatorRequestDialogModel::SetStep(AuthenticatorRequestDialogModel::Step) chrome/browser/webauthn/authenticator_request_dialog_model.cc:170:7
    #3 0x5562104356e3 in GPMEnclaveController::OnGPMTrustThisComputer() chrome/browser/webauthn/gpm_enclave_controller.cc:843:3
    #4 0x55621039251c in AuthenticatorRequestDialogModel::OnGPMTrustThisComputer() chrome/browser/webauthn/authenticator_request_dialog_model.cc:255:1
    #5 0x556215ca7951 in AuthenticatorRequestDialogView::Accept() chrome/browser/ui/views/webauthn/authenticator_request_dialog_view.cc:303:20
    #6 0x7f7949df63e8 in views::DialogDelegate::AcceptDialog() ui/views/window/dialog_delegate.cc:576:34
    #7 0x7f7949deeb13 in base::internal::Invoker<base::internal::FunctorTraits<void (views::DialogClientView::* const&)(ui::mojom::DialogButton, ui::Event const&), views::DialogClientView*, ui::mojom::DialogButton const&>, base::internal::BindState<true, true, false, void (views::DialogClientView::*)(ui::mojom::DialogButton, ui::Event const&), base::internal::UnretainedWrapper<views::DialogClientView, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, ui::mojom::DialogButton>, void (ui::Event const&)>::Run(base::internal::BindStateBase*, ui::Event const&) base/functional/bind_internal.h:740:12
    #8 0x7f7949a88d0f in base::RepeatingCallback<void (ui::Event const&)>::Run(ui::Event const&) const & base/functional/callback.h:346:12
    #9 0x7f7949a84196 in views::Button::NotifyClick(ui::Event const&) gen/third_party/libc++/src/include/variant:501:12
    #10 0x7f7949a8c2dd in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button_controller.cc
    #11 0x7f79767acfb4 in ui::ScopedTargetHandler::OnEvent(ui::Event*) ui/events/scoped_target_handler.cc:30:24
    #12 0x7f797679439d in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:189:12
    #13 0x7f7976792f9b in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:138:5
    #14 0x7f7976792704 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:84:14
    #15 0x7f797679223a in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #16 0x7f7949d8a505 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root_view.cc:628:9
    #17 0x7f7949dbcafb in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:2210:20
    #18 0x7f7949e65d0c in views::NativeWidgetAura::OnMouseEvent(ui::MouseEvent*) ui/views/widget/native_widget_aura.cc
    #19 0x7f797679439d in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:189:12
    #20 0x7f7976792f9b in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:138:5
    #21 0x7f7976792704 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:84:14
    #22 0x7f797679223a in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #23 0x7f797679aacf in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:72:19
    #24 0x7f797679e051 in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:119:16
    #25 0x7f797679d9f4 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:134:12
    #26 0x7f79588cc67d in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:300:38
    #27 0x7f7949e94bf8 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:250:29
    #28 0x7f797cb7b527 in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (ui::Event*)>::RunOnce(base::internal::BindStateBase*, ui::Event*) base/functional/bind_internal.h:740:12
    #29 0x7f79767b4c4a in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) base/functional/callback.h:155:12

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/ui/webauthn/authenticator_request_window.cc:157:13 in (anonymous namespace)::PasskeyResetWebContentsObserver::DidFinishNavigation(content::NavigationHandle*)
Shadow bytes around the buggy address:
  0x7bb8f865ac80: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fd
  0x7bb8f865ad00: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x7bb8f865ad80: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fa
  0x7bb8f865ae00: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x7bb8f865ae80: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fd
=>0x7bb8f865af00: f7 fa fd fd fd fd[fd]fd f7 fa fd fd fd fd fd fd
  0x7bb8f865af80: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fd
  0x7bb8f865b000: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fa
  0x7bb8f865b080: f7 fa 00 00 00 00 00 00 f7 fa fd fd fd fd fd fd
  0x7bb8f865b100: f7 fa 00 00 00 00 00 00 f7 fa fd fd fd fd fd fd
  0x7bb8f865b180: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fa
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

==2852092==ADDITIONAL INFO

==2852092==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7f796da1df88 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ipc/ipc_mojo_bootstrap.cc:1138:13
    #1 0x7f797a5ee84a in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13

Command line: `./out/ui/chrome --no-sandbox --gaia-url=http://localhost:8080 --flag-switches-begin --enable-experimental-web-platform-features --flag-switches-end --ozone-platform=x11 http://localhost:8080/`

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==2852092==END OF ADDITIONAL INFO

==2852092==ABORTING


```
#### Reporter credit:

Krace

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.2 KB)
- [change.diff](attachments/change.diff) (text/x-diff, 3.8 KB)
- [server.py](attachments/server.py) (text/x-python, 4.8 KB)

## Timeline

### me...@gmail.com (2026-04-17)

Hello, I have updated the server.py which will not trigger the CHECK in WebContents. All the other patches are made to simulate a PrimaryAccount, could you please re-evaluate this issue? Thanks!

### an...@chromium.org (2026-04-17)

Assigning provisional severity (haven't repro'd myself) of S1 as it is memory corruption in browser process.
derinel@ can you PTAL since your CL was mentioned in the bisect?
CC'd agl as well (owner)

### ch...@google.com (2026-04-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-18)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-20)

Project: chromium/src  

Branch:  main  

Author:  Nina Satragno [nsatragno@chromium.org](mailto:nsatragno@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7778612>

[webauthn] Fix write after free

---


Expand for full commit details
```
     
    Fix a write after free on `PasskeyResetWebContentsObserver`. Tests once 
    I figure out how to test this under ASAN. 
     
    Fixed: 503420438 
    Change-Id: Ib269113d21cd706d1cf4db8d1d554c9a34671d87 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7778612 
    Reviewed-by: Adem Derinel <derinel@google.com> 
    Commit-Queue: Nina Satragno <nsatragno@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1617563}

```

---

Files:

- M `chrome/browser/ui/webauthn/authenticator_request_window.cc`

---

Hash: [51e898b4eda8b25397f0f42aedee4d0f05aabfcd](https://chromiumdash.appspot.com/commit/51e898b4eda8b25397f0f42aedee4d0f05aabfcd)  

Date: Mon Apr 20 16:53:53 2026


---

### ch...@google.com (2026-04-21)

Requesting merge to M147 because latest trunk commit (1617563) appears to be after M147 branch point (1596535).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M148 because latest trunk commit (1617563) appears to be after M148 branch point (1610480).

### ch...@google.com (2026-04-21)

**M147** merge request created. **Please update [crbug/504872874](https://crbug.com/504872874) to have this merge reviewed.**

### ch...@google.com (2026-04-21)

**M148** merge request created. **Please update [crbug/504872981](https://crbug.com/504872981) to have this merge reviewed.**

### ns...@chromium.org (2026-04-21)

(I still need to verify this fix doesn't cause any issues.)

### ns...@chromium.org (2026-04-27)

<https://crrev.com/c/7783616> is a little more complex but it solves this in a more robust way, so we shouldn't merge <https://crrev.com/c/7778612>, and I'm leaning towards not doing any merges.

Exploiting this seems quite tough. It has these preconditions:

- User must have used GPM passkeys on another device.
- User has not yet used GPM passkeys on the local device.
- User goes through the GPM unlock flow (sites can trigger this with a webauthn call).
- User decides they want to reset their passkeys.
- Code sets a single enum value on freed memory.

### dx...@google.com (2026-04-28)

Project: chromium/src  

Branch:  main  

Author:  Nina Satragno [nsatragno@chromium.org](mailto:nsatragno@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7783616>

[webauthn] Test & update authenticator window code

---


Expand for full commit details
```
     
    Update AuthenticatorRequestWindow so it is more amenable for testing and 
    it's more resilient: 
    * Have the Magic Arch base URL be configurable from the command line 
      instead of only the PIN reset URL so we can test other flows. 
    * Post tasks for web content observer events so the web contents can be 
      closed synchronously from AuthenticatorRequestDialogModel step 
      observers. AFAICT, this is something that may happen in production 
      (but we don't seem to run into), but definitely does happen in tests. 
    * Use a scoped observation to observe the model. It's cleaner. 
     
    Then, write tests for paths that were not tested before: 
    * Resetting the security domain and then simulating the user clicking 
      the button acknowledging this. 
    * Resetting the security domain and then simulating the user closing the 
      window. 
     
    Note that this test changes the way we address the UAF from 
    crbug.com/503420438. I wasn't sure that change didn't cause problems and 
    I couldn't test it, so this solution should be considered strictly 
    better until proven otherwise. 
     
    Bug: 503420438 
    Change-Id: Ia36376b33a766f70986275743a023a392c5dcf07 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7783616 
    Commit-Queue: Nina Satragno <nsatragno@chromium.org> 
    Reviewed-by: Adem Derinel <derinel@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1621832}

```

---

Files:

- M `chrome/browser/ui/webauthn/authenticator_dialog_browsertest.cc`
- M `chrome/browser/ui/webauthn/authenticator_request_window.cc`
- M `chrome/browser/webauthn/webauthn_switches.cc`
- M `chrome/browser/webauthn/webauthn_switches.h`

---

Hash: [23d9b63d4ee926648e30dc939c4725af17c60314](https://chromiumdash.appspot.com/commit/23d9b63d4ee926648e30dc939c4725af17c60314)  

Date: Tue Apr 28 16:32:34 2026


---

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
highly mitigated browser memory corruption


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### me...@gmail.com (2026-05-05)

Hello, is this eligible for a bisect bonus?

### aj...@google.com (2026-05-07)

The bisect bonus is included in the reward already, sorry that this wasn't noted in comment 13.

### ch...@google.com (2026-07-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-29)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

## Bounty Award

> highly mitigated browser memory corruption

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503420438)*
