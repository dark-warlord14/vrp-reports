# Security: Heap-use-after-free in ManagePasswordsUIController::SavePassword

| Field | Value |
|-------|-------|
| **Issue ID** | [40060559](https://issues.chromium.org/issues/40060559) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Passwords |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2022-08-11 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**  

commit d5e65e8f5f8f26bea38c82c2ee72f11e1af5b6f4

1. apply the change.txt and compile chrome with ASAN
2. `python copy_mojo_js_bindings.py path/to/ASAN/gen/` and copy poc.html to the same folder
3. start a server at poc.html's folder : python -m SimpleHTTPServer 8605
4. ASAN/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/noexist <http://127.0.0.1:8605/poc.html>
5. click submit button and save the password, then close the popup
6. input any text, submit and then save the password again
7. if this doesn't crash the browser, repeat setp6 again

**Problem Description:**  

This is found by fuzzing, I'm not familiar with this code, and don't figure out the root cause of this problem. So the analysis maybe not right :P  

The patch is used to simulate the leak of passwords.

When we save a leaked password, it will be stored in `std::vector<const PasswordForm\*> insecure_credentials_` of class `FormFetcherImpl`[1].  

The Mojo `credential.store` will call `client_->NotifyStorePasswordCalled` [2], which will reset the `FormManager` and destruct the `FormFetcherImpl`, and the `PasswordForm` strore in `FomFetcherImpl` will also be reset.

```
void CredentialManagerImpl::Store(const CredentialInfo& credential,  
                                  StoreCallback callback) {  
  const url::Origin origin = GetOrigin();  
  if (password_manager_util::IsLoggingActive(client_)) {  
    CredentialManagerLogger(client_->GetLogManager())  
        .LogStoreCredential(origin, credential.type);  
  }  
  
  // Send acknowledge response back.  
  std::move(callback).Run();  
  
  if (credential.type == CredentialType::CREDENTIAL_TYPE_EMPTY ||  
      !client_->IsSavingAndFillingEnabled(origin.GetURL()))  
    return;  
  
  client_->NotifyStorePasswordCalled(); // [2]  
  
  std::unique_ptr<PasswordForm> form(  
      CreatePasswordFormFromCredentialInfo(credential, origin));  
  
  // Check whether a stored password credential was leaked.  
  if (credential.type == CredentialType::CREDENTIAL_TYPE_PASSWORD) {  
    leak_delegate_.StartLeakCheck(  
        \*form, /\*submitted_form_was_likely_signup_form=\*/false);  
  }  
  
  std::string signon_realm = origin.GetURL().spec();  
  PasswordFormDigest observed_digest(PasswordForm::Scheme::kHtml, signon_realm,  
                                     origin.GetURL());  
  
  // Create a custom form fetcher without HTTP->HTTPS migration as the API is  
  // only available on HTTPS origins.  
  auto form_fetcher = std::make_unique<FormFetcherImpl>(  
      observed_digest, client_, /\*should_migrate_http_passwords=\*/false);  
  form_manager_ = std::make_unique<CredentialManagerPasswordFormManager>(  
      client_, std::move(form), this, nullptr, std::move(form_fetcher));  
}  

```

After that when we click save button, `SavePassword` will use the freed `PasswordForm`[3].

```
void ManagePasswordsUIController::SavePassword(const std::u16string& username,  
                                               const std::u16string& password) {  
  UpdatePasswordFormUsernameAndPassword(username, password,  
                                        passwords_data_.form_manager());  
  
  if (auto\* sentiment_service =  
          TrustSafetySentimentServiceFactory::GetForProfile(  
              Profile::FromBrowserContext(  
                  web_contents()->GetBrowserContext()))) {  
    sentiment_service->SavedPassword();  
  }  
  
  if (GetPasswordFormMetricsRecorder() && BubbleIsManualFallbackForSaving()) {  
    GetPasswordFormMetricsRecorder()->RecordDetailedUserAction(  
        password_manager::PasswordFormMetricsRecorder::DetailedUserAction::  
            kTriggeredManualFallbackForSaving);  
  }  
  save_fallback_timer_.Stop();  
  passwords_data_.form_manager()->Save();  
  
  // If we just saved a password to the account store, notify the IPH tracker  
  // about it (so it can decide not to show the IPH again).  
  if (GetPasswordFeatureManager()->GetDefaultPasswordStore() ==  
      password_manager::PasswordForm::Store::kAccountStore) {  
    feature_engagement::TrackerFactory::GetForBrowserContext(  
        Profile::FromBrowserContext(web_contents()->GetBrowserContext()))  
        ->NotifyEvent("passwords_account_storage_used");  
  }  
  
  post_save_compromised_helper_ =  
      std::make_unique<password_manager::PostSaveCompromisedHelper>(  
          passwords_data_.form_manager()->GetInsecureCredentials(), username); //[3]  
[...]  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/form_fetcher_impl.h;drc=06106fa71f3ed1044028f77ccf4d5b9de7028b8b;bpv=1;bpt=1;l=94>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/credential_manager_impl.cc;l=50;drc=06106fa71f3ed1044028f77ccf4d5b9de7028b8b>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/passwords/manage_passwords_ui_controller.cc;l=546;drc=bead2b4d2553e57229747b48b3dceaadbb8972bf>

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 44.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.4 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 1.7 MB)
- [change.txt](attachments/change.txt) (text/plain, 4.3 KB)

## Timeline

### [Deleted User] (2022-08-11)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-08-11)

[Comment Deleted]

### me...@gmail.com (2022-08-11)

After some debug, I think I have found the root cause of this issue.

`FormFetcherImpl::Clone()` will copy `FormFetcherImpl` to make a new unique_ptr[1]. The copy of unique_ptr is implemented by `MakeCopies`[2], it will create a new unique_ptr use the origin unique_ptr's raw ptr. This is OK, but the raw_ptr is copied directly, which should be the new unique_ptr's raw ptr, rather than the origin raw ptr.

```[1]
std::unique_ptr<FormFetcher> FormFetcherImpl::Clone() {
  // Create the copy without the "HTTPS migration" activated. If it was needed,
  // then it was done by |this| already.
  auto result = std::make_unique<FormFetcherImpl>(form_digest_, client_, false);

  if (state_ != State::NOT_WAITING) {
    // There are no store results to copy, trigger a Fetch on the clone instead.
    result->Fetch();
    return result;
  }

  result->non_federated_ = MakeCopies(non_federated_);
  result->federated_ = MakeCopies(federated_);
  result->is_blocklisted_in_account_store_ = is_blocklisted_in_account_store_;
  result->is_blocklisted_in_profile_store_ = is_blocklisted_in_profile_store_;
  password_manager_util::FindBestMatches(
      MakeWeakCopies(result->non_federated_), form_digest_.scheme,
      &result->non_federated_same_scheme_, &result->best_matches_,
      &result->preferred_match_);

  result->interactions_stats_ = interactions_stats_;
  result->insecure_credentials_ = insecure_credentials_;
  result->state_ = state_;
  result->need_to_refetch_ = need_to_refetch_;

  return result;
}
```

```[2]
std::vector<std::unique_ptr<PasswordForm>> MakeCopies(
    const std::vector<std::unique_ptr<PasswordForm>>& source) {
  std::vector<std::unique_ptr<PasswordForm>> result(source.size());
  std::transform(source.begin(), source.end(), result.begin(),
                 [](const std::unique_ptr<PasswordForm>& ptr) {
                   return std::make_unique<PasswordForm>(*ptr);
                 });
  return result;
}
```

Therefore we can patch this issue by assigning the right value to raw ptr `insecure_credentials_`.

example patch:
```
diff --git a/components/password_manager/core/browser/form_fetcher_impl.cc b/components/password_manager/core/browser/form_fetcher_impl.cc
index 2a5e507b6366..19d396124485 100644
--- a/components/password_manager/core/browser/form_fetcher_impl.cc
+++ b/components/password_manager/core/browser/form_fetcher_impl.cc
@@ -230,7 +230,15 @@ std::unique_ptr<FormFetcher> FormFetcherImpl::Clone() {
       &result->preferred_match_);
 
   result->interactions_stats_ = interactions_stats_;
-  result->insecure_credentials_ = insecure_credentials_;
+  //result->insecure_credentials_ = insecure_credentials_;
+  for (auto& form : result->federated_) {
+    if (!form->password_issues.empty())
+        result->insecure_credentials_.push_back(form.get());
+  }
+  for (auto& form : result->non_federated_) {
+    if (!form->password_issues.empty())
+        result->insecure_credentials_.push_back(form.get());
+  }
   result->state_ = state_;
   result->need_to_refetch_ = need_to_refetch_;

```

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/form_fetcher_impl.cc;l=223;drc=06106fa71f3ed1044028f77ccf4d5b9de7028b8b;bpv=1;bpt=1
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/form_fetcher_impl.cc;l=49;drc=06106fa71f3ed1044028f77ccf4d5b9de7028b8b


### th...@chromium.org (2022-08-12)

I can reproduce if I include the patch. It seems like a reasonable shortcut to trigger the "password leaked" behavior, but vasilii@ if this would not be possible to hit without the patch please say so. Also assigning you generally as you're listed as an owner for this code.

Assigning medium severity because it's memory corruption in the browser process, but requires a compromised renderer and several user gestures.

### [Deleted User] (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-12)

[Empty comment from Monorail migration]

### va...@chromium.org (2022-08-12)

r983316 is the culprit. We should not copy the raw ptrs.

[Monorail components: UI>Browser>Passwords]

### jk...@google.com (2022-08-15)

Unfortunately, that's correct.

Thank you for the report and Vasilii, thank you for analyzing it. It have created https://chromium-review.googlesource.com/c/chromium/src/+/3826135.

### va...@chromium.org (2022-08-16)

Thanks. BTW, 15.08 was a public holiday ;)

### gi...@appspot.gserviceaccount.com (2022-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64

commit 4d8d3d96fddfa5e7b8e2717436699ed7e3745d64
Author: Jan Keitel <jkeitel@google.com>
Date: Tue Aug 16 19:23:11 2022

Create separate copies of PasswordForms instead of keeping raw pointers.

This CL avoids maintaining a set of raw pointers to PasswordForms and instead keeps separate copies. While this may be slightly less
performant, it reduces the risk of those pointers going stale during
future refactorings.

Bug: 1351969
Change-Id: Iabcde87cf022bcb61c2dfcd690e99cd108602571
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3826135
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Cr-Commit-Position: refs/heads/main@{#1035634}

[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/mock_password_form_manager_for_ui.h
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/fake_form_fetcher.cc
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/fake_form_fetcher.h
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/form_fetcher.h
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/password_generation_manager.cc
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/password_form_manager_for_ui.h
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/form_fetcher_impl.h
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/form_fetcher_impl_unittest.cc
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/password_form_manager.h
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/chrome/browser/ui/passwords/manage_passwords_ui_controller_unittest.cc
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/form_fetcher_impl.cc
[modify] https://crrev.com/4d8d3d96fddfa5e7b8e2717436699ed7e3745d64/components/password_manager/core/browser/password_form_manager.cc


### jk...@google.com (2022-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-17)

Requesting merge to beta M105 because latest trunk commit (1035634) appears to be after beta branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-17)

Merge review required: M105 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@google.com (2022-08-18)

1. Why does your merge fit within the merge criteria for these milestones?
Security issue
2. https://chromium-review.googlesource.com/c/chromium/src/+/3826135
3. They were released to Canary - @thefrog, can you also verify that they fix the issue?
4. It is a bug fix and not gated by a flag.
5. N/A
6. N/A

### th...@chromium.org (2022-08-18)

Re 3) in https://crbug.com/chromium/1351969#c18: I can no longer reproduce this on head.

### jk...@google.com (2022-08-18)

Thank you!

### am...@chromium.org (2022-08-22)

m105 merge approved, please merge this fix to branch 5195 asap/ before 12pm PST tomorrow (Tuesday, 23 August) so this fix can be included in m105 stable cut -- thank you!

### gi...@appspot.gserviceaccount.com (2022-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9d3038db8a9ffc1345502f8c770ba82eed442c37

commit 9d3038db8a9ffc1345502f8c770ba82eed442c37
Author: Jan Keitel <jkeitel@google.com>
Date: Tue Aug 23 17:01:40 2022

Create separate copies of PasswordForms instead of keeping raw pointers.

This CL avoids maintaining a set of raw pointers to PasswordForms and instead keeps separate copies. While this may be slightly less
performant, it reduces the risk of those pointers going stale during
future refactorings.

(cherry picked from commit 4d8d3d96fddfa5e7b8e2717436699ed7e3745d64)

Bug: 1351969
Change-Id: Iabcde87cf022bcb61c2dfcd690e99cd108602571
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3826135
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1035634}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3851181
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Jan Keitel <jkeitel@google.com>
Cr-Commit-Position: refs/branch-heads/5195@{#847}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/mock_password_form_manager_for_ui.h
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/fake_form_fetcher.h
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/fake_form_fetcher.cc
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/form_fetcher.h
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/password_form_manager_for_ui.h
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/password_generation_manager.cc
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/form_fetcher_impl.h
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/form_fetcher_impl_unittest.cc
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/password_form_manager.h
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/form_fetcher_impl.cc
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/chrome/browser/ui/passwords/manage_passwords_ui_controller_unittest.cc
[modify] https://crrev.com/9d3038db8a9ffc1345502f8c770ba82eed442c37/components/password_manager/core/browser/password_form_manager.cc


### am...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-30)

Congratulations! The VRP Panel has decided to award you $4,000 for this report of a moderately mitigated [1] security bug. Thank you for your efforts and reporting this issue to us! 

[1] https://g.co/chrome/vrp 

### am...@google.com (2022-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-28)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1351969?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060559)*
