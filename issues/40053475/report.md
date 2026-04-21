# Security: UAF in AutofillPopupControllerImpl::HandleKeyPressEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40053475](https://issues.chromium.org/issues/40053475) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | jd...@chromium.org |
| **Created** | 2020-09-30 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36

Steps to reproduce the problem:
VULNERABILITY DETAILS

When user fill out forms, a popup view will be shown with suggestions saved before.

In function AutofillPopupControllerImpl::Show, a handler is registed to handle key press event with an unretained raw pointer of AutofillPopupControllerImpl [1]. This may cause UAF if we free AutofillPopupControllerImpl and then trigger the event handler.

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/autofill/autofill_popup_controller_impl.cc;l=134;drc=af3f705abb90a12087e6dd49d55f92818a3d5ca7
```
void AutofillPopupControllerImpl::Show(
    const std::vector<Suggestion>& suggestions,
    bool autoselect_first_suggestion,
    PopupType popup_type) {

  // skip ...

  static_cast<ContentAutofillDriver*>(delegate_->GetAutofillDriver())
      ->RegisterKeyPressHandler(
          base::Bind(&AutofillPopupControllerImpl::HandleKeyPressEvent,
                     base::Unretained(this)));  // =====> [1]

  delegate_->OnPopupShown();
}
```

AutofillPopupControllerImpl is deleted in function AutofillPopupControllerImpl::HideViewAndDie, which will be called when AutofillExternalDelegate gets deconstructed [2]. AutofillExternalDelegate is owned by ContentAutofillDriver whose lifetime is bound to RenderFrameHost.

HideViewAndDie dose not remove the key press handler registed before. So if we free RenderFrameHost, which subsequently free AutofillPopupControllerImpl, and then trigger the handler again, an UAF will occur.

https://source.chromium.org/chromium/chromium/src/+/master:components/autofill/core/browser/autofill_external_delegate.cc;l=62;drc=af3f705abb90a12087e6dd49d55f92818a3d5ca7
```
AutofillExternalDelegate::~AutofillExternalDelegate() {
  if (deletion_callback_)
    std::move(deletion_callback_).Run();  // =====> [2]  calls to HideViewAndDie
}
```

VERSION
Chrome Version: 85.0.4183.121 (stable)

REPRODUCTION CASE

This is a bug which is triggered from a compromised renderer to attack the privileged browser process. 
patch.diff is the renderer-side patch that simulates the compromised renderer state.
With a compromised renderer, the only user interaction which is really needed to trigger the bug is a key event registed in HandleKeyPressEvent, such as [Enter], [Key_Up], [Key_Down], [Esc].

Steps to reproduce:

1. Apply the patch.diff

2. Setup a HTTPServer
python -m SimpleHTTPServer

3. Run asan build chrome, and follow the instructions described in the html file.
./chrome http://localhost:8000/poc.html

What is the expected behavior?
Not crash.

What went wrong?
UAF occurred.

Did this work before? N/A 

Chrome version: 85.0.4183.121  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 1.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 30.5 KB)

## Timeline

### do...@chromium.org (2020-09-30)

+autofill folks, can you please take a look. This looks like an inappropriate use of base::Unretained where there is no lifetime guarantee.

Similar to https://crbug.com/chromium/1133635 - High severity UaF in the browser process, mitigated by the need for a compromised renderer and user input to exploit it. The code is present in Stable and has been there for quite some time.

[Monorail components: UI>Browser>Autofill]

### ko...@google.com (2020-09-30)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-09-30)

koerber@, can you triage this? I don't think I am the right owner for this bug.

### ko...@google.com (2020-09-30)

schwering@ started investigating.

### [Deleted User] (2020-09-30)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/192ad9fd016679aa69904c067b9e3951295905f4

commit 192ad9fd016679aa69904c067b9e3951295905f4
Author: Jan Wilken Dörrie <jdoerrie@chromium.org>
Date: Wed Sep 30 18:27:10 2020

[Autofill][Passwords] Fix HandleKeyPressEvent

This change fixes key press event handlers by checking a weak ptr before
invoking them.

Bug: 1133671, 1133688
Change-Id: Id7708653c127a49343edf57de2a6fa4522ca088d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2440620
Reviewed-by: Christoph Schwering <schwering@google.com>
Reviewed-by: Dominic Battré <battre@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Auto-Submit: Jan Wilken Dörrie <jdoerrie@chromium.org>
Commit-Queue: Jan Wilken Dörrie <jdoerrie@chromium.org>
Cr-Commit-Position: refs/heads/master@{#812215}

[modify] https://crrev.com/192ad9fd016679aa69904c067b9e3951295905f4/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/192ad9fd016679aa69904c067b9e3951295905f4/chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc


### jd...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-09-30)

r812215 should fix this particular issue. Security folks, could you comment on to what releases this needs to be merged back, if any?

### [Deleted User] (2020-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-30)

Requesting merge to stable M85 because latest trunk commit (812215) appears to be after stable branch point (782793).

Requesting merge to beta M86 because latest trunk commit (812215) appears to be after beta branch point (800218).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-30)

This bug requires manual review: We are only 5 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-09-30)

+adetaylor@ (Security TPM) for M86 merge review.


Looks like r812215 (landed 1 hr back, not in canary yet)  fixes this issue and other https://crbug.com/chromium/1133688. 

Note: We already cut M86 Stable RC for Android and Desktop. 



### jd...@chromium.org (2020-09-30)

Just in case my input is required on these (I'll gladly refer to adetaylor@ to assess the urgency here):

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Yes, since it's a security bug.

2. Links to the CLs you are requesting to merge.

 r812215

3. Has the change landed and been verified on ToT?

It landed, and I verified it on ToT. It's not in Canary yet, though.

4. Does this change need to be merged into other active release branches (M-1, M+1)?

Probably?

5. Why are these changes required in this milestone after branch?

Security issue only got discovered after.

6. Is this a new feature?

No.

7. If it is a new feature, is it behind a flag using finch?

No.

### ad...@chromium.org (2020-09-30)

Approving merge to M86, branch 4240, but please wait for a day of Canary first. This may or may not get into the first M86 stable release depending on if we recut the RC, but if not, it will go out in our first stable refresh.

No further M85 releases planned, so zapping that merge label.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b53f6b91380f19ae4be2b33f46f46fc59e4405e2

commit b53f6b91380f19ae4be2b33f46f46fc59e4405e2
Author: Jan Wilken Dörrie <jdoerrie@chromium.org>
Date: Fri Oct 02 12:56:36 2020

[Autofill][Passwords] Fix HandleKeyPressEvent

This change fixes key press event handlers by checking a weak ptr before
invoking them.

(cherry picked from commit 192ad9fd016679aa69904c067b9e3951295905f4)

Bug: 1133671, 1133688
Change-Id: Id7708653c127a49343edf57de2a6fa4522ca088d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2440620
Reviewed-by: Christoph Schwering <schwering@google.com>
Reviewed-by: Dominic Battré <battre@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Auto-Submit: Jan Wilken Dörrie <jdoerrie@chromium.org>
Commit-Queue: Jan Wilken Dörrie <jdoerrie@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#812215}
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2445150
Reviewed-by: Jan Wilken Dörrie <jdoerrie@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1120}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/b53f6b91380f19ae4be2b33f46f46fc59e4405e2/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/b53f6b91380f19ae4be2b33f46f46fc59e4405e2/chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc


### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-07)

.... and the VRP panel has decided to award $20,000 for this bug as well.

### jt...@gmail.com (2020-10-08)

Thanks for the quick fix and reward, cheers !

### ad...@google.com (2020-10-08)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1133671?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053475)*
