# Security: Calling ash::DiagnosticsDialog::ShowDialog multiple times can result in an Use-After-Free (UAF) error in ash::diagnostics::NetworkingLog::UpdateNetworkList.

| Field | Value |
|-------|-------|
| **Issue ID** | [40064290](https://issues.chromium.org/issues/40064290) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Call stack:

1. PlayStore app background js: sendNativeMessage('onRunNetworkTestsClicked');
2. arc::ArcSessionManager::OnRunNetworkTestsClicked();
3. ash::DiagnosticsDialog::ShowDialog();
4. ash::diagnostics::DiagnosticsLogController::Get()->ResetAndInitializeLogWriters();

Within the ResetAndInitializeLogWriters function, various member variables such as  

keyboard\_input\_log\_ and networking\_log\_ are freed and subsequently reinitialized.

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:ash/system/diagnostics/diagnostics_log_controller.cc;l=183-193;drc=1be03d635f64b065a567c02c3341fcc839f0e9e5>

```
void DiagnosticsLogController::ResetAndInitializeLogWriters() {  
  // ...  
  keyboard_input_log_ = std::make_unique<KeyboardInputLog>(log_base_path_);  
  networking_log_ = std::make_unique<NetworkingLog>(log_base_path_); // <-- Reinitialized  
  routine_log_ = std::make_unique<RoutineLog>(log_base_path_);  
  telemetry_log_ = std::make_unique<TelemetryLog>();  
}  

```

By examining the call hierarchy of DiagnosticsLogController::GetNetworkingLog(), we can notice  

that a raw pointer to networking\_log\_ is passed and then stored in the instance of  

ash::diagnostics::NetworkHealthProvider.

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:ash/webui/diagnostics_ui/backend/diagnostics_manager.cc;l=30-31;drc=1be03d635f64b065a567c02c3341fcc839f0e9e5>

```
DiagnosticsManager::DiagnosticsManager(SessionLogHandler\* session_log_handler,  
                                       content::WebUI\* webui)  
    : webui_(webui) {  
  // Configure providers with logs from DiagnosticsLogController when flag  
  // enabled.  
  if (features::IsLogControllerForDiagnosticsAppEnabled() &&  
      DiagnosticsLogController::IsInitialized()) {  
    system_data_provider_ = std::make_unique<SystemDataProvider>(  
        DiagnosticsLogController::Get()->GetTelemetryLog());  
    system_routine_controller_ = std::make_unique<SystemRoutineController>(  
        DiagnosticsLogController::Get()->GetRoutineLog());  
    network_health_provider_ = std::make_unique<NetworkHealthProvider>(  
        DiagnosticsLogController::Get()->GetNetworkingLog()); // <--- Raw ptr passed  
  } else {  
    // ......   
  }  
}  

```

Let's move to another call stack:

ash/webui/diagnostics\_ui/resources/network\_list.ts

1. When diagnostics dialog shows, NetworkListElement::constructor()
2. this.observeNetworkList();
3. this.networkHealthProvider.observeNetworkList() mojo call to ash::NetworkHealthProvider::ObserveNetworkList();

ash/webui/diagnostics\_ui/backend/connectivity/network\_health\_provider.cc  

4. ash::NetworkHealthProvider::ObserveNetworkList();  

5. ash::NetworkHealthProvider::NotifyNetworkListObservers();

In the NetworkHealthProvider::NotifyNetworkListObservers function, the networking\_log\_ptr\_  

is utilized to invoke UpdateNetworkList. However, if networking\_log\_ is freed by  

ResetAndInitializeLogWriters before this point, a Use-After-Free (UAF) error may occur.

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:ash/webui/diagnostics_ui/backend/connectivity/network_health_provider.cc;l=641-651;drc=1be03d635f64b065a567c02c3341fcc839f0e9e5>

```
void NetworkHealthProvider::NotifyNetworkListObservers() {  
  std::vector<std::string> observer_guids =  
      GetObserverGuidsAndUpdateActiveGuid();  
  for (auto& observer : network_list_observers_) {  
    observer->OnNetworkListChanged(mojo::Clone(observer_guids), active_guid_);  
  }  
  
  if (IsLoggingEnabled() && !active_guid_.empty()) {  
    networking_log_ptr_->UpdateNetworkList(observer_guids, active_guid_); // <-- UAF if networking_log_ is freed.  
  }  
}  

```

This can be achieved through a background JavaScript call in the PlayStore application.

```
sendNativeMessage('onRunNetworkTestsClicked');  
sendNativeMessage('onRunNetworkTestsClicked');  

```

You may be confused as to how this is possible when reading the source code of  

DiagnosticsDialog::ShowDialog. We would close any existing dialog before reopening via  

MaybeCloseExistingDialog function.

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/webui/ash/diagnostics_dialog.cc;l=43-73;drc=d04c3f5aa44a179ef0c65faae5d94a9451e43f5a>

```
// static  
void DiagnosticsDialog::ShowDialog(DiagnosticsDialog::DiagnosticsPage page,  
                                   gfx::NativeWindow parent) {  
  // Close any instance of Diagnostics opened as an SWA.  
  auto\* profile = ProfileManager::GetActiveUserProfile();  
  auto\* browser =  
      ash::FindSystemWebAppBrowser(profile, ash::SystemWebAppType::DIAGNOSTICS);  
  if (browser) {  
    browser->window()->Close();  
  }  
  
  // Close any existing Diagnostics dialog before reopening.  
  MaybeCloseExistingDialog();  
  
  DiagnosticsDialog\* dialog = new DiagnosticsDialog(page);  
  
  // Ensure log controller configuration matches current session.  
  if (features::IsLogControllerForDiagnosticsAppEnabled()) {  
    diagnostics::DiagnosticsLogController::Get()  
        ->ResetAndInitializeLogWriters();  
  }  
  
  dialog->ShowSystemDialog(parent);  
}  

```

Nonetheless, this approach did not succeed due to an issue with the overridden member  

function Id(), which was removed incorrectly as per <https://chromium-review.googlesource.com/c/chromium/src/+/4076817>.  

As the returned existing\_dialog from SystemWebDialogDelegate::FindInstance(kDiagnosticsDialogId)  

will always be null, the first diagnostics dialog would not be closed.

Even MaybeCloseExistingDialog work as expected, it is still possible for a Use-After-Free (UAF)  

error to occur.

```
void DiagnosticsDialog::MaybeCloseExistingDialog() {  
  SystemWebDialogDelegate\* existing_dialog =  
      SystemWebDialogDelegate::FindInstance(kDiagnosticsDialogId);  
  if (existing_dialog) {  
    existing_dialog->Close();  
  }  
}  

```

Call stack

1. ash::SystemWebDialogDelegate::Close()
2. views::Widget::Close()
3. views::Widget::CloseWithReason()

By examining the CloseWithReason function comment, we can ascertain that the dialog still  

exists until a return to the message loop. Therefore, invoking ResetAndInitializeLogWriters  

after this call is erroneous.

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:ui/views/widget/widget.h;l=688-692;drc=3a06e758a5820009ee0f2590b08a311f00d76163>

```
  // Hides the widget, then closes it after a return to the message loop,  
  // specifying the reason for it having been closed.  
  // Note that while you can pass ClosedReason::kUnspecified, it is highly  
  // discouraged and only supported for backwards-compatibility with Close().  
  void CloseWithReason(ClosedReason closed_reason);  

```

**VERSION**  

Chrome Version: 112.0.5615.134 (Official Build) (64bit) stable  

Bitset: <https://chromium-review.googlesource.com/c/chromium/src/+/3587610>  

Operating System: ChromeOS

**REPRODUCTION CASE**

1. Run PlayStore app
2. Go to chrome://extensions page, load attached extension
3. Wait 15 seconds, UAF occur

Note: Since the system may experience repeated UAF errors upon restarting,  

it is advisable to remove the PoC extension during this extended timeout period.  

If you comprehend this trick, you can reduce the 15 seconds timeout duration  

to expedite the reproduction process.

Poc Video: <https://drive.google.com/file/d/1-Rnpkqxh6idtl7ZuZWGQUgp5tfwUMvNM/view?usp=share_link>

As PlayStore is unavailable in linux-chromeos, I have also created a patch that  

can simulate and replicate the issue.

1. Git Apply testShowDiagnosticsDialog.patch
2. Go to chrome://certificate-manager/ and run following js code in console.

```
chrome.send("testShowDiagnosticsDialog"); chrome.send("testShowDiagnosticsDialog");  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see attached diagnostics\_reset\_uaf.asan

**CREDIT INFORMATION**  

Reporter credit: Chaobin Zhang

## Attachments

- [background.js](attachments/background.js) (text/plain, 720 B)
- [manifest.json](attachments/manifest.json) (text/plain, 1.0 KB)
- [diagnostics_reset_uaf.asan](attachments/diagnostics_reset_uaf.asan) (text/plain, 22.3 KB)
- [testShowDiagnosticsDialog.patch](attachments/testShowDiagnosticsDialog.patch) (text/plain, 2.3 KB)

## Timeline

### [Deleted User] (2023-04-30)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-05-01)

Thanks for the report, and the patch! :)

When you say

> This can be achieved through a background JavaScript call in the PlayStore application.

do you mean a hypothetical malicious Android application, or the malicious Chrome extension you attached? Or does an attack require the target to have both installed?

michaelcheco@ et al., could you please take a look?

### zh...@gmail.com (2023-05-02)

I'm glad to hear that it was helpful!

> When you say
>>  This can be achieved through a background JavaScript call in the PlayStore application.
> do you mean a hypothetical malicious Android application, or the malicious Chrome extension you attached? Or does an attack require the target to have both installed?

The PlayStore application is a platform app built into Chromebook. We can find the source code here: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/chromeos/arc_support/. The JavaScript code sendNativeMessage('onRunNetworkTestsClicked') works in the background.js file of the PlayStore platform app with the app ID "cnbgggchhmkkdmeppjobngjoejnihlei".

The malicious Chrome extension I attached is simplified from `arc_support` directory, and the attack only requires it. The trick used by the extension is that it employs the same "key" as shown in this link: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/chromeos/arc_support/manifest.json;l=10-11.

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

[Monorail blocking: b/280378934]

### ch...@google.com (2023-05-02)

Your report will be worked on in the Buganizer system ( link: https://issuetracker.google.com/issues/280378934 ). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-06-06)

b/280378934 had been marked as fixed. 

### ch...@google.com (2023-06-12)

Project: chromium/src
Branch: refs/branch-heads/5790

commit 68b660642ceb0cc2f18ab5771d0b0c39e5c96086
Author: Gavin Williams <gavinwill@chromium.org>
Date:   Mon Jun 05 19:26:57 2023

    [115] Diagnostics: Change all logs from raw ptrs to references
   
    - Change the log getters to return a reference instead of a
      pointer so consumers know not to store them
    - Allow setting logs directly in DiagnosticsLogController for tests
    - Create a separate FakeDiagnosticsBrowserDelegate to help initialize
      DiagnosticsLogController in tests
   
    (cherry picked from commit 2aa9e64bdd400b1fc392d162428b01fcf58c8b5f)
   
    Bug: b:280378934
    Tests: ash_webui_unittests --gtest_filter=InputDataProviderTest.*, NetworkHealthProviderTest.*, SystemDataProviderTest.*, SystemRoutineControllerTest.*
    Change-Id: I809a28bfe9cca83ac4ac20f35c813244d9724a86
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4545778
    Reviewed-by: Zentaro Kavanagh <zentaro@chromium.org>
    Commit-Queue: Gavin Williams <gavinwill@chromium.org>
    Reviewed-by: Jimmy Gong <jimmyxgong@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1150726}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4585378
    Cr-Commit-Position: refs/branch-heads/5790@{#363}
    Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

M       ash/BUILD.gn
M       ash/system/diagnostics/diagnostics_log_controller.cc
M       ash/system/diagnostics/diagnostics_log_controller.h
M       ash/system/diagnostics/diagnostics_log_controller_unittest.cc
A       ash/system/diagnostics/fake_diagnostics_browser_delegate.cc
A       ash/system/diagnostics/fake_diagnostics_browser_delegate.h
M       ash/webui/diagnostics_ui/backend/connectivity/network_health_provider.cc
M       ash/webui/diagnostics_ui/backend/connectivity/network_health_provider.h
M       ash/webui/diagnostics_ui/backend/connectivity/network_health_provider_unittest.cc
M       ash/webui/diagnostics_ui/backend/diagnostics_manager.cc
M       ash/webui/diagnostics_ui/backend/input/input_data_provider.cc
M       ash/webui/diagnostics_ui/backend/input/input_data_provider.h
M       ash/webui/diagnostics_ui/backend/input/input_data_provider_unittest.cc
M       ash/webui/diagnostics_ui/backend/session_log_handler_unittest.cc
M       ash/webui/diagnostics_ui/backend/system/system_data_provider.cc
M       ash/webui/diagnostics_ui/backend/system/system_data_provider.h
M       ash/webui/diagnostics_ui/backend/system/system_data_provider_unittest.cc
M       ash/webui/diagnostics_ui/backend/system/system_routine_controller.cc
M       ash/webui/diagnostics_ui/backend/system/system_routine_controller.h
M       ash/webui/diagnostics_ui/backend/system/system_routine_controller_unittest.cc
M       chrome/browser/ui/webui/ash/diagnostics_dialog.cc
M       chrome/browser/ui/webui/ash/diagnostics_dialog.h
A       chrome/browser/ui/webui/ash/diagnostics_dialog_unittest.cc
M       chrome/test/BUILD.gn

https://chromium-review.googlesource.com/4585378
21:29
21:29
CLs: Merged:​crrev/c/4545778, crrev/c/4585439      crrev/c/4545778, crrev/c/4585378, crrev/c/4585439
CLs: Pending:​crrev/c/4585378      <none>

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-20)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-20)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-13)

Congratulations, ChaobinZhang! The VRP Panel has decided to award you $1,000 for this report of a security issue in ash that is significantly mitigated by preconditions of a malicious Play store application being installed on the device and extension. Thank you for your efforts in discovering this issue and reporting it to us. 

### zh...@gmail.com (2023-07-13)

Thanks for the reward. But I am a little confused.  The Play store application is built-in officially by default in many real device, and it is not need to be maliciou. Please take a look again.

### zh...@gmail.com (2023-07-13)

[Comment Deleted]

### zh...@gmail.com (2023-07-14)

By the way, I want to correct the reproduce steps in my report. In the first step, the official Play Store application didn't need to be running. It was just required to run once before the victim load the malicious extension, so that ArcSupportHost was initialized and the malicious extension can call |sendNativeMessage('onRunNetworkTestsClicked');|

Sorry for the trouble. Please help me apply for another round reward assessment. 

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-19)

Thanks for the information, Chaobin Zhang. Based on reassessment, the VRP Panel has decided to award you $5,000 for this report of a mildly mitigated security bug with the precondition to install a malicious extension. Thank you for your efforts and and your patience while we reassessed this issue. 

### zh...@gmail.com (2023-07-19)

I sincerely appreciate this, as it enhances my chances of being included among the top Chrome VRP researchers of 2023, which is one of my goals for this year!

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-18)

This issue was migrated from crbug.com/chromium/1441306?no_tracker_redirect=1

[Monorail blocking: b/280378934]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064290)*
