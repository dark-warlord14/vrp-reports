# Security: UAF in PasswordAutofillManager::OnBiometricReauthCompleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40061475](https://issues.chromium.org/issues/40061475) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Windows |
| **Reporter** | jt...@gmail.com |
| **Assignee** | vs...@google.com |
| **Created** | 2022-10-26 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chromium allows biometric authentication before form filling. If user accepts the autofill password suggestion, it calls `PasswordAutofillManager::DidAcceptSuggestion` and use `authenticator_` to do biometric auth [1].

On windows platform, it then calls `BiometricAuthenticatorWin::AuthenticateWithMessage` which posts the AuthenticateCallback to current SequencedTaskRunner [2]. The task has a bound raw pointer to PasswordAutofillManager [3]. The PasswordAutofillManager instance might get destroyed before the scheduled task is executed, for example, if the webcontents get destroyed. As a result, `PasswordAutofillManager::OnBiometricReauthCompleted` would access freed memory at line [4].

```
void PasswordAutofillManager::DidAcceptSuggestion(  
    const autofill::Suggestion& suggestion,  
    int position) {  
  // ...  
  auto on_reath_complete =  
    base::BindOnce(&PasswordAutofillManager::OnBiometricReauthCompleted,  
                    base::Unretained(this),        // ======> [3]  
                    suggestion.main_text.value,   
                    suggestion.frontend_id);  
  
  authenticator_->AuthenticateWithMessage(        // ======> [1]  
      device_reauth::BiometricAuthRequester::kAutofillSuggestion,  
      l10n_util::GetStringFUTF16(IDS_PASSWORD_MANAGER_FILLING_REAUTH,  
                                  origin),  
      metrics_util::TimeCallback(  
          std::move(on_reath_complete),  
          "PasswordManager.PasswordFilling.AuthenticationTime"));  
}  
  
void BiometricAuthenticatorWin::AuthenticateWithMessage(  
    device_reauth::BiometricAuthRequester requester,  
    const std::u16string& message,  
    AuthenticateCallback callback) {  
  // ...  
  base::SequencedTaskRunnerHandle::Get()->PostTask(        // ======> [2]  
      FROM_HERE,  
      base::BindOnce(std::move(callback),  
                     RecordAuthenticationResult(  
                         authenticator_->AuthenticateUser(message))));  
}  
  
void PasswordAutofillManager::OnBiometricReauthCompleted(  
    const std::u16string& value,  
    int frontend_id,  
    bool auth_succeeded) {  
  authenticator_.reset();        // ======> [4]  
  // ...  
}  
  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/password_autofill_manager.cc;l=547;drc=e2403606fdfdc27d6e273477f059bae2791e9a06>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/device_reauth/win/biometric_authenticator_win.cc;l=65;drc=e2403606fdfdc27d6e273477f059bae2791e9a06>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/password_autofill_manager.cc;l=542;drc=e2403606fdfdc27d6e273477f059bae2791e9a06>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/password_autofill_manager.cc;l=967;drc=e2403606fdfdc27d6e273477f059bae2791e9a06>

**VERSION**  

Chrome Version: dev  

Operating System: Windows

**REPRODUCTION CASE**  

To simulate a normal user filling out a form using biometric authentication in a simple way:

1. Apply the attached patch. It forces PasswordAutofillManager to use biometric auth, and avoids a UAF bug which occurs at an earlier time (see <https://crbug.com/chromium/1378456> for more details).
2. Save one password on localhost domain, you may use new\_password\_helper.html for convenience, e.g., host it at localhost, submit any password, and choose to save it

To reproduce:

1. Host poc.html at localhost  
   
   python3 -m http.server 8000
2. out\asan\chrome.exe --enable-features=Portals,BiometricAuthenticationForFilling <http://localhost:8000/poc.html>
3. Use autofilling to fill the password field, the UAF will occur after closing the Windows credential UI prompt

Note that this bug can be triggered without a compromised renderer.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log for details

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 1.6 KB)
- [new_password_helper.html](attachments/new_password_helper.html) (text/plain, 347 B)
- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 16.2 KB)

## Timeline

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### jt...@gmail.com (2022-10-26)

[Comment Deleted]

### me...@chromium.org (2022-10-26)

kolos, this is similar to https://crbug.com/chromium/1378456, could you PTAL? Thanks.

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-27)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@chromium.org (2022-10-28)

[Empty comment from Monorail migration]

### ko...@chromium.org (2022-11-02)

vsemeniuk@: Could you please take a look? IIUC it was introduced in crrev.com/c/3985747

### vs...@google.com (2022-11-02)

Yes, using base::Unretained isn't safe there. I created a CL [1] to use weak_ptr instead.  

[1]https://chromium-review.googlesource.com/c/chromium/src/+/3998772

### gi...@appspot.gserviceaccount.com (2022-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e0ca2d3a9e278e1ae20a4b70a32f44cd8401ed6

commit 4e0ca2d3a9e278e1ae20a4b70a32f44cd8401ed6
Author: Viktor Semeniuk <vsemeniuk@google.com>
Date: Thu Nov 03 13:40:23 2022

Using weak_ptr instead of base::Unretained in PasswordAutofillManager

Bug: 1378457
Change-Id: If0441d7dd29584fa906ffca9e3c8876ded6680e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3998772
Reviewed-by: Maxim Kolosovskiy <kolos@chromium.org>
Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com>
Cr-Commit-Position: refs/heads/main@{#1066965}

[modify] https://crrev.com/4e0ca2d3a9e278e1ae20a4b70a32f44cd8401ed6/components/password_manager/core/browser/password_autofill_manager.cc


### vs...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### vs...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, Rong Jian! The VPR Panel has decided to award you $7,000 for this report of a mildly mitigated security bug. Thank you for your efforts in discovering and reporting this issue to us!  

### am...@chromium.org (2022-11-11)

Also while I am here, this issue is mildly mitigated by standard user gesture for this feature and closing a prompt. 
Severity == High rather than Critical 

### [Deleted User] (2022-11-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-12)

Not requesting merge to dev (M109) because latest trunk commit (1066965) appears to be prior to dev branch point (1070088). If this is incorrect, please replace the Merge-NA-109 label with Merge-Request-109. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1378457?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061475)*
