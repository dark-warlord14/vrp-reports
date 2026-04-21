# Security: UAF in IdentityDialogController::ShowIdProviderWindow

| Field | Value |
|-------|-------|
| **Issue ID** | [40057362](https://issues.chromium.org/issues/40057362) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2021-09-23 |
| **Bounty** | $25,000.00 |

## Description

**VULNERABILITY DETAILS**

If `navigator.id.get()` API is called under the permission-oriented flow, a permission prompt is shown, and when the user accepts it, `FederatedAuthRequestImpl::OnSigninApproved` is called which would send a request to fetch well-known configuration [1]. The permission prompt can be closed (e.g. user closing the dialog manually), which will destroy the corresponding WebIdDialog instance, before network manager gets the fetch result. As a result, the raw pointer `view_` in IdentityDialogController becomes a dangling pointer [2]. UAF would occur if the IdP responded to the token fetch with a signin\_url and the IdentityDialogController tries to show signin page with invalid `view_` pointer [3].

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=260;drc=45523c9180c9526630bb3f660828d0539e9be655>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webid/identity_dialog_controller.h;l=81;drc=45523c9180c9526630bb3f660828d0539e9be655>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webid/identity_dialog_controller.cc;l=49;drc=45523c9180c9526630bb3f660828d0539e9be655>

**REPRODUCTION CASE**

Note that this bug can be triggered without a compromised renderer.  

Steps to reproduce:

1. Setup HTTPServer with nodejs (for supporting webid)  
   
   node ./server.js
2. Run asan build chrome with the following command  
   
   ./chrome --ignore-certificate-errors --enable-features=WebID <http://localhost:8081/poc.html>
3. Click the 'Continue' button in the permission prompt, then close the dialog, the browser will crash in seconds

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

## Attachments

- [server.js](attachments/server.js) (text/plain, 1.3 KB)
- [server.cert](attachments/server.cert) (application/octet-stream, 1.2 KB)
- [server.key](attachments/server.key) (application/octet-stream, 1.7 KB)
- [asan.log](attachments/asan.log) (text/plain, 35.2 KB)
- [ajgo.asan](attachments/ajgo.asan) (text/plain, 25.6 KB)

## Timeline

### [Deleted User] (2021-09-23)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-23)

The best I can do is a CHECK on a refptr:-

[18108:8848:0923/155726.521:FATAL:scoped_refptr.h(235)] Check failed: ptr_.
Backtrace:
        base::debug::CollectStackTrace [0x00007FF9420F9F29+25] (C:\src\chromium\src\base\debug\stack_trace_win.cc:303)
        base::debug::StackTrace::StackTrace [0x00007FF941DE66F1+33] (C:\src\chromium\src\base\debug\stack_trace.cc:197)
        logging::LogMessage::~LogMessage [0x00007FF941E594FC+972] (C:\src\chromium\src\base\logging.cc:590)
        logging::LogMessage::~LogMessage [0x00007FF941E5D667+23] (C:\src\chromium\src\base\logging.cc:584)
        scoped_refptr<base::internal::BindStateBase>::operator-> [0x00007FF931331997+273] (C:\src\chromium\src\base\memory\scoped_refptr.h:235)
        base::OnceCallback<void (content::IdentityRequestDialogController::UserApproval)>::Run [0x00007FF936BAD5BF+257] (C:\src\chromium\src\base\callback.h:98)
        WebIdDialogViews::Accept [0x00007FF94A4282BB+37] (C:\src\chromium\src\chrome\browser\ui\views\webid\webid_dialog_views.cc:164)
        views::DialogDelegate::AcceptDialog [0x00007FF94A09FFE6+926] (C:\src\chromium\src\ui\views\window\dialog_delegate.cc:407)
        views::DialogClientView::ButtonPressed [0x00007FF950355F61+251] (C:\src\chromium\src\ui\views\window\dialog_client_view.cc:299)
        views::Button::NotifyClick [0x00007FF941B6EBF3+991] (C:\src\chromium\src\ui\views\controls\button\button.cc:632)        views::Button::DefaultButtonControllerDelegate::NotifyClick [0x00007FF941B69D10+96] (C:\src\chromium\src\ui\views\controls\button\button.cc:69)
        views::ButtonController::OnMouseReleased [0x00007FF94541B5C9+815] (C:\src\chromium\src\ui\views\controls\button\button_controller.cc:59)
        views::View::ProcessMouseReleased [0x00007FF941BBA51A+608] (C:\src\chromium\src\ui\views\view.cc:3068)
        ui::ScopedTargetHandler::OnEvent [0x00007FF94F639973+333] (C:\src\chromium\src\ui\events\scoped_target_handler.cc:28)
        ui::EventDispatcher::DispatchEvent [0x00007FF9431D192C+248] (C:\src\chromium\src\ui\events\event_dispatcher.cc:192)
        ui::EventDispatcher::ProcessEvent [0x00007FF9431D081F+1057] (C:\src\chromium\src\ui\events\event_dispatcher.cc:140)
        ui::EventDispatcherDelegate::DispatchEventToTarget [0x00007FF9431D013C+394] (C:\src\chromium\src\ui\events\event_dispatcher.cc:84)
        ui::EventDispatcherDelegate::DispatchEvent [0x00007FF9431CFD30+668] (C:\src\chromium\src\ui\events\event_dispatcher.cc:56)
        views::internal::RootView::OnMouseReleased [0x00007FF9454D32F5+507] (C:\src\chromium\src\ui\views\widget\root_view.cc:480)
        views::Widget::OnMouseEvent [0x00007FF941BF19C3+2511] (C:\src\chromium\src\ui\views\widget\widget.cc:1549)
        views::NativeWidgetAura::OnMouseEvent [0x00007FF9454C9BF1+765] (C:\src\chromium\src\ui\views\widget\native_widget_aura.cc:1035)
        ui::EventDispatcher::DispatchEvent [0x00007FF9431D192C+248] (C:\src\chromium\src\ui\events\event_dispatcher.cc:192)
        ui::EventDispatcher::ProcessEvent [0x00007FF9431D081F+1057] (C:\src\chromium\src\ui\events\event_dispatcher.cc:140)
        ui::EventDispatcherDelegate::DispatchEventToTarget [0x00007FF9431D013C+394] (C:\src\chromium\src\ui\events\event_dispatcher.cc:84)
        ui::EventDispatcherDelegate::DispatchEvent [0x00007FF9431CFD30+668] (C:\src\chromium\src\ui\events\event_dispatcher.cc:56)
        ui::EventProcessor::OnEventFromSource [0x00007FF9499333BB+1471] (C:\src\chromium\src\ui\events\event_processor.cc:49)
        ui::EventSource::DeliverEventToSink [0x00007FF9454BFB10+424] (C:\src\chromium\src\ui\events\event_source.cc:113)        ui::EventSource::SendEventToSinkFromRewriter [0x00007FF9454BF666+1750] (C:\src\chromium\src\ui\events\event_source.cc:138)
        ui::EventSource::SendEventToSink [0x00007FF9454BEF86+22] (C:\src\chromium\src\ui\events\event_source.cc:107)
        views::DesktopWindowTreeHostWin::HandleMouseEvent [0x00007FF94992FF2A+1100] (C:\src\chromium\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1004)
        views::HWNDMessageHandler::HandleMouseEventInternal [0x00007FF94F6EA048+2240] (C:\src\chromium\src\ui\views\win\hwnd_message_handler.cc:3146)
        views::HWNDMessageHandler::_ProcessWindowMessage [0x00007FF94F6E0BB5+547] (C:\src\chromium\src\ui\views\win\hwnd_message_handler.h:360)
        views::HWNDMessageHandler::OnWndProc [0x00007FF94F6E0045+859] (C:\src\chromium\src\ui\views\win\hwnd_message_handler.cc:1020)
        gfx::WindowImpl::WndProc [0x00007FF945F9A4BD+643] (C:\src\chromium\src\ui\gfx\win\window_impl.cc:306)
        base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> [0x00007FF945F98A57+15] (C:\src\chromium\src\base\win\wrapped_window_proc.h:77)
        CallWindowProcW [0x00007FF9F573E7E8+1016]
        DispatchMessageW [0x00007FF9F573E229+601]
        base::MessagePumpForUI::ProcessMessageHelper [0x00007FF94211F8D9+2297] (C:\src\chromium\src\base\message_loop\message_pump_win.cc:542)
        base::MessagePumpForUI::ProcessNextWindowsMessage [0x00007FF94211D303+1091] (C:\src\chromium\src\base\message_loop\message_pump_win.cc:504)
        base::MessagePumpForUI::DoRunLoop [0x00007FF94211CBBD+1485] (C:\src\chromium\src\base\message_loop\message_pump_win.cc:215)
        base::MessagePumpWin::Run [0x00007FF942119228+456] (C:\src\chromium\src\base\message_loop\message_pump_win.cc:78)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FF945AD64F5+1893] (C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:462)
        base::RunLoop::Run [0x00007FF941F59182+2370] (C:\src\chromium\src\base\run_loop.cc:136)
        content::BrowserMainLoop::RunMainMessageLoop [0x00007FF9373DD4A4+736] (C:\src\chromium\src\content\browser\browser_main_loop.cc:988)
        content::BrowserMainRunnerImpl::Run [0x00007FF9373E4B23+487] (C:\src\chromium\src\content\browser\browser_main_runner_impl.cc:152)
        content::BrowserMain [0x00007FF9373D4825+1125] (C:\src\chromium\src\content\browser\browser_main.cc:49)
        content::RunBrowserProcessMain [0x00007FF93B52CA3F+571] (C:\src\chromium\src\content\app\content_main_runner_impl.cc:609)
        content::ContentMainRunnerImpl::RunBrowser [0x00007FF93B5304D7+4179] (C:\src\chromium\src\content\app\content_main_runner_impl.cc:1105)
        content::ContentMainRunnerImpl::Run [0x00007FF93B52F2BF+1065] (C:\src\chromium\src\content\app\content_main_runner_impl.cc:972)
        content::RunContentProcess [0x00007FF93B52AA00+1588] (C:\src\chromium\src\content\app\content_main.cc:390)
        content::ContentMain [0x00007FF93B52BDEF+205] (C:\src\chromium\src\content\app\content_main.cc:418)
        ChromeMain [0x00007FF93132159B+983] (C:\src\chromium\src\chrome\app\chrome_main.cc:172)
        MainDllLoader::Launch [0x00007FF689028DFB+1337] (C:\src\chromium\src\chrome\app\main_dll_loader_win.cc:169)
        main [0x00007FF689023C7B+11271] (C:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:382)
        __scrt_common_main_seh [0x00007FF6895CE390+268] (d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        BaseThreadInitThunk [0x00007FF9F5557034+20]
        RtlUserThreadStart [0x00007FF9F7202651+33]

Which version (or commit) of Chrome are you testing on?

### aj...@google.com (2021-09-23)

Oh no right after that I got the UAF :)

### aj...@google.com (2021-09-23)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-23)

Interestingly this is in a DCHECK:

WebIdDialog& IdentityDialogController::GetOrCreateView(
    content::WebContents* rp_web_contents) {
  if (!view_)
    view_ = WebIdDialog::Create(rp_web_contents);

  // It is expected that we use the same rp_web_contents during the lifetime
  // of this controller.
  DCHECK_EQ(view_->rp_web_contents(), rp_web_contents);  <<<---- here

  return *view_;
}

However, the original reporter's report is not:-

void IdentityDialogController::ShowIdProviderWindow(
    content::WebContents* rp_web_contents,
    content::WebContents* idp_web_contents,
    const GURL& idp_signin_url,
    IdProviderWindowClosedCallback callback) {
  GetOrCreateView(rp_web_contents)
      .ShowSigninPage(idp_web_contents, idp_signin_url, std::move(callback)); <<-----
}

So this is very likely a real problem.

Repro notes:

Copy files attached above to a directory
cd to the directory
C:\src\chromium\src\third_party\node\win\node.exe .\server.js

elsewhere:
cd src\chromium\src
.\out\Asan\Chrome.exe --ignore-certificate-errors --enable-features=WebID --enable-blink-features=WebID http://localhost:8081/poc.html

Setting severity Critical as this is a web-browser uaf that is relatively easy to trigger. Setting Impact=None as the WebID flag is disabled - please let me know if this is shipping to any users (e.g. via Finch or an OT).

Assigning to yigu based on recent history. Please investigate and fix this security issue.

[Monorail components: Blink>Identity>WebID]

### aj...@google.com (2021-09-23)

(confirmed with Ken that this is behind an unshipped flag so None is appropriate)

### aj...@google.com (2021-09-23)

[Empty comment from Monorail migration]

### yi...@chromium.org (2021-09-24)

Hi Ken,
Have you and Majid had a follow up discussion on this TODO?
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webid/identity_dialog_controller.cc;l=63

### gi...@appspot.gserviceaccount.com (2021-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/69d46add8011be2183bc7abeca8560c3e58f031f

commit 69d46add8011be2183bc7abeca8560c3e58f031f
Author: Ken Buchanan <kenrb@chromium.org>
Date: Wed Sep 29 15:42:21 2021

[WebID] Clear dialog view on window closure

Currently when IdentityProviderController::ShowIdProviderWindow is
called, it takes a callback that is invoked when the user explicitly
closes the dialog window. However, the dismissal can happen before the
method is called, since it is still up from the initial permission
request. In that case no notification of the dialog closure is
sent to FederatedAuthRequestImpl, leading to a crash.

This change plumbs the closure callback on creation of the WebIdDialog.

Bug: 1252354
Change-Id: I4b353dd2a9f6a3050427c2505ddcd46befbc6e0a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188813
Reviewed-by: Yi Gu <yigu@chromium.org>
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#926277}

[modify] https://crrev.com/69d46add8011be2183bc7abeca8560c3e58f031f/chrome/browser/ui/views/webid/webid_dialog_views.h
[modify] https://crrev.com/69d46add8011be2183bc7abeca8560c3e58f031f/chrome/browser/ui/views/webid/webid_dialog_views_unittest.cc
[modify] https://crrev.com/69d46add8011be2183bc7abeca8560c3e58f031f/chrome/browser/ui/android/webid/webid_dialog_android.cc
[modify] https://crrev.com/69d46add8011be2183bc7abeca8560c3e58f031f/chrome/browser/ui/webid/identity_dialog_controller.h
[modify] https://crrev.com/69d46add8011be2183bc7abeca8560c3e58f031f/chrome/browser/ui/webid/webid_dialog.h
[modify] https://crrev.com/69d46add8011be2183bc7abeca8560c3e58f031f/chrome/browser/ui/views/webid/webid_dialog_views.cc
[modify] https://crrev.com/69d46add8011be2183bc7abeca8560c3e58f031f/chrome/browser/ui/webid/identity_dialog_controller.cc


### ke...@chromium.org (2021-09-29)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations - the VRP Panel has decided to award you $25,000 for this report! Not only was it a highly impactful issue, but we your detailed report helped towards quick reproduction and identification of the issue so it could be swiftly resolved by the engineers. Thank you and great work!! 

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### yi...@chromium.org (2021-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-01-05)

This issue was migrated from crbug.com/chromium/1252354?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-25)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057362)*
