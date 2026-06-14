# Security: Potential Use-After-Free in PasswordGenerationPopupControllerImpl::EditPasswordClicked


| Field | Value |
|-------|-------|
| **Issue ID** | [349253666](https://issues.chromium.org/issues/349253666) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 126.0.6478.114 |
| **Reporter** | kd...@gmail.com |
| **Assignee** | rg...@google.com |
| **Created** | 2024-06-25 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. The bug was found by static analysis, so there is no poc yet. However, the prior fix in 079002c2a37d156e88065bb58cecfad9597d7818 suggests that it might be a UAF. So, I'm asking for your manual intervention. Thanks for the time!

# Problem Description

```
// src/chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc
void PasswordGenerationPopupControllerImpl::PasswordAccepted() {
  // ...
  base::WeakPtr<PasswordGenerationPopupControllerImpl> weak_this = GetWeakPtr();
  if (driver_) {
    // See https://crbug.com/1133635 for when `driver_` might be null due to a
    // compromised renderer.
    driver_->GeneratedPasswordAccepted(form_data_, generation_element_id_,
                                       current_generated_password_);
  }
  // |this| can be destroyed here because GeneratedPasswordAccepted pops up
  // another UI and generates some event to close the dropdown.
  if (weak_this) {
    driver_->FocusNextFieldAfterPasswords();
    weak_this->HideImpl();
  }
}

```

In commit <https://chromium.googlesource.com/chromium/src.git/+/079002c2a37d156e88065bb58cecfad9597d7818>, developer notice that `driver_->GeneratedPasswordAccepted` may cause `PasswordGenerationPopupControllerImpl` being destroyed. Thus results in UAF. However, in the `PasswordGenerationPopupControllerImpl::EditPasswordClicked` which is introduced later, the developer use `PasswordGenerationPopupControllerImpl::Show` directly after calling the `GeneratedPasswordAccepted`, which may involves UAF.

```
void PasswordGenerationPopupControllerImpl::EditPasswordClicked() {
  driver_->GeneratedPasswordAccepted(form_data_, generation_element_id_,
                                     current_generated_password_); // may free |this|
  Show(kEditGeneratedPassword); // PasswordGenerationPopupControllerImpl::Show
}


```

Since this issue is detected by static analysis, I don't have a PoC and cannot ensure the bug existence. But you may want to manually check to be safe.

# Summary

Security: Potential Use-After-Free in PasswordGenerationPopupControllerImpl::EditPasswordClicked

# Custom Questions

#### Reporter credit:

Han Zheng (HexHive)

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Timeline

### el...@chromium.org (2024-06-25)

Thanks for the report. I have reviewed the code in question and agree with your reading. Over to vasilii@ who wrote the original mitigation in 079002c2a37d156e88065bb58cecfad9597d7818.

vasilii@: can you fix this error-prone pattern please? it seems like an easy mistake to make to try using `this` after calling `driver_->GeneratedPasswordAccepted()`.

### va...@chromium.org (2024-06-26)

This code is in the Finch experiment and we are ramping it down in a few days anyway. I suggest that as soon as it unlaunches, @rgod can simply close this bug and delete the code.

### pe...@google.com (2024-06-26)

Setting milestone because of s0/s1 severity.

### th...@chromium.org (2024-07-12)

[secondary shepherd] Hi rgod@ -- can the code be deleted now as the fix to this bug?

### pe...@google.com (2024-07-13)

rgod: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-07-15)

Project: chromium/src
Branch: main

commit 0c83b1d10fe3aca428458db81d4dbc6ed33424b4
Author: rgod <rgod@google.com>
Date:   Mon Jul 15 16:48:26 2024

    [Passwords] Remove edit password experiment
    
    Edit password arm of the generation experiment will not move forward and
    can be cleaned up. Ideally all code would be cleaned up at the same
    time, but other arms are pending HaTS results.
    
    Fixed: 349253666
    Change-Id: Id8801101f9f5fb5784f404c61433092f0253f665
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5705421
    Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
    Commit-Queue: Rafał Godlewski <rgod@google.com>
    Cr-Commit-Position: refs/heads/main@{#1327564}

M       chrome/app/generated_resources.grd
D       chrome/app/generated_resources_grd/IDS_PASSWORD_GENERATION_EDIT_PASSWORD.png.sha1
M       chrome/browser/ui/android/passwords/password_generation_editing_popup_view_android.cc
M       chrome/browser/ui/android/passwords/password_generation_editing_popup_view_android.h
M       chrome/browser/ui/passwords/password_generation_popup_controller.h
M       chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc
M       chrome/browser/ui/passwords/password_generation_popup_controller_impl.h
M       chrome/browser/ui/passwords/password_generation_popup_controller_impl_unittest.cc
M       chrome/browser/ui/passwords/password_generation_popup_view.h
M       chrome/browser/ui/passwords/password_generation_popup_view_browsertest.cc
M       chrome/browser/ui/views/autofill/popup/popup_base_view.cc
M       chrome/browser/ui/views/passwords/password_generation_popup_view_views.cc
M       chrome/browser/ui/views/passwords/password_generation_popup_view_views.h
M       chrome/browser/ui/views/passwords/password_generation_popup_view_views_browsertest.cc

https://chromium-review.googlesource.com/5705421


### pe...@google.com (2024-07-16)

Requesting merge to stable (M126) because latest trunk commit (1327564) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1327564) appears to be after beta branch point (1313161).
Merge review required: a commit with .grd or policy\_templates.json string changes was detected.

Merge review required: a commit with .grd or policy\_templates.json string changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-07-17)

based on c#3, `This code is in the Finch experiment and we are ramping it down in a few days anyway. I suggest that as soon as it unlaunches, @rgod can simply close this bug and delete the code.` I do not believe we need to backmerge this change / code removal since this Finch experiment is being turned down.

### rg...@google.com (2024-07-17)

Agree with [comment#9](https://issues.chromium.org/issues/349253666#comment9), the experiment has already ramped down ([Finch config](https://source.corp.google.com/piper///depot/google3/googledata/googleclient/chrome/finch/gcl_studies/passwords/PasswordGenerationExperiment.gcl;l=78?q=PasswordGenerationExperiment&sq=package:piper%20file:%2F%2Fdepot%2Fgoogle3%20-file:google3%2Fexperimental))

### am...@chromium.org (2024-07-17)

perfect, thank you for confirming (and the link to the finch config!)

### sp...@google.com (2024-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1000 for report of highly mitigated memory corruption bug in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Thank you for the report. Based on this code, exploiting this issue would require a significant amount of user interaction. Since we were able to make a security relevant change based on your report, we have extended the reward consistent with a highly mitigated bug. Thanks again for your efforts and reporting this issue to us.

### qk...@google.com (2024-09-12)

Labeling as LTS-NotApplicable-120 because  comment#9 said that the code was in the Finch experiment and they already were ramping it down.

### qk...@google.com (2024-09-19)

Labeling as LTS-NotApplicable-126 because of the same reason for M120 above.

### pe...@google.com (2024-10-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349253666)*
