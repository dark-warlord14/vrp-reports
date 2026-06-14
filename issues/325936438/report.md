# UAF in FedCmAccountSelectionView::Show

| Field | Value |
|-------|-------|
| **Issue ID** | [325936438](https://issues.chromium.org/issues/325936438) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2024-02-20 |
| **Bounty** | $6,000.00 |

## Description

VULNERABILITY DETAILS
In function `FedCmAccountSelectionView::Show` if IDP sign-in modal dialog is open, the showing of the accounts dialog would be delayed [1], and once the modal dialog is closed, `show_accounts_dialog_callback_` would be executed to show the accounts dialog [2]. However in this path the code does not check FedCM API settings and if the embargo was triggered, the execution of `show_accounts_dialog_callback_` would destroy the FedCmAccountSelectionView and UAF occurs. Considering the following scenario:
1. website triggers a IDP failure
2. user clicks continue button to sign in, which opens the login page (modal dialog), and the login page triggers a new FedCM UI
3. user dismisses the UI in the login page which triggers embargo
4. The login page can be closed by JS code, and since the modal dialog is closed, `FedCmAccountSelectionView::Show` is called again to show the accounts dialog
5. Since FedCM is embargoed, it goes with `ShowVerifyingSheet -> OnAccountSelected -> CompleteRequestWithError`, which destory the FedCmAccountSelectionView
6. The code will continue access member of FedCmAccountSelectionView which leads to UAF

```c++
void FedCmAccountSelectionView::Show(
    const std::string& top_frame_etld_plus_one,
    const std::optional<std::string>& iframe_etld_plus_one,
    const std::vector<content::IdentityProviderData>&
        identity_provider_data_list,
    Account::SignInMode sign_in_mode,
    blink::mojom::RpMode rp_mode,
    bool show_auto_reauthn_checkbox) {
  if (popup_window_ && (state_ == State::IDP_SIGNIN_STATUS_MISMATCH ||
                        state_ == State::ACCOUNT_PICKER)) {
    popup_window_state_ =
        PopupWindowResult::kAccountsReceivedAndPopupNotClosedByIdp;
    show_accounts_dialog_callback_ =                                            // ==> [1]
        base::BindOnce(&FedCmAccountSelectionView::Show,
                       weak_ptr_factory_.GetWeakPtr(), top_frame_etld_plus_one,
                       iframe_etld_plus_one, identity_provider_data_list,
                       sign_in_mode, rp_mode, show_auto_reauthn_checkbox);
    return;
  }


void FedCmAccountSelectionView::CloseModalDialog() {
  // ...
  if (show_accounts_dialog_callback_) {
    std::move(show_accounts_dialog_callback_).Run();   // ==> [2]
    if (is_web_contents_visible_) {
      input_protector_->VisibilityChanged(true);
      GetDialogWidget()->Show();
    }
```
[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=82;drc=51747de656cd4c61e038b7d82e9b7bf20e6d2bb9
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=615;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090

VERSION
Chrome Version: stable 121.0.6167.185 + dev

REPRODUCTION CASE
Tested on: Chrome 123.0.6307.1 asan build 64-bit on Windows 10
1. Create a web server using node.js
   node ./server.js
2. Launch chrome and navigate to http://localhost:8000/poc.html
   out\Asan\chrome.exe http://localhost:8000/poc.html
3. Click continue button, then dismiss the dialog in the new popup page

Please be noted to create a new web server for each test, and clear browser user data is highly recommended. 

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan.log for details

== Bisection ==
This was initially introduced in https://chromium.googlesource.com/chromium/src/+/f4863c5e182188465f2511083ee130fd9d4fda15

== Additional Information ==
compromised renderer requirement: no
miracle ptr protected: no
user interaction: yes

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 30.8 KB)
- [login.html](attachments/login.html) (text/html, 677 B)
- [poc.html](attachments/poc.html) (text/html, 840 B)
- [server.js](attachments/server.js) (text/javascript, 2.1 KB)
- deleted (application/octet-stream, 0 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.6 MB)

## Timeline

### jt...@gmail.com (2024-02-20)

Also upload a recording of repro :)

### jt...@gmail.com (2024-02-20)

Oops.. This is the first time I reported bug via new bug tracker, it seems that access to this issue is not restricted, so I changed the restriction settings to 'Restricted'. Any help to change the visibility would be appreciated.

### cb...@chromium.org (2024-02-20)

For future reference, instructions for reporting security bugs are at https://www.chromium.org/for-testers/faq/#how-do-i-file-a-security-bug

See also https://crbug.com/40279117


### am...@chromium.org (2024-02-21)

Thanks for the report, Rong!
The current security shepherd on duty will triage this tomorrow.
I'm re-uploading demo provided in c#2 since everyone on the eng team may not have the appropriate permissions to review Restricted content.

For future reference, the direct link to the security bug template is: <https://issues.chromium.org/issues/new?noWizard=true&component=1363614&template=1922342>

It's also linked from the Chrome VRP page (<https://g.co/chrome/vrp>) and the Chrome VRP FAQ & News (<https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#news-and-updates>)

### ah...@google.com (2024-02-21)

Thanks for the report!
I was able to reproduce on 122.0.6261.0 on windows. (Setting found in to 122, current extended stable)
Setting severity to High (Memory corruption in the browser process that requires specific user interaction, please correct me if my understanding is wrong)
Assigning to yigu@chromium.org as per owners file: content/browser/webid/OWNERS

### pe...@google.com (2024-02-21)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-02-21)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### yi...@chromium.org (2024-02-21)

Thanks for reporting with poc!

Quick recap:
1. main window calls FedCM and triggers the mismatch UI
2. pop-up window sets the loginstatus such that the API call from main window would fetch accounts, due to the presence of the pop-up window, the accounts UI is hidden
3. the pop-up window calls FedCM separately, user closes the account UI and it will trigger embargo, pop-up window calls IdentityProvder.close() immediately after the promise is rejected
4. when the pop-up window is closed, the accounts UI from step 2 can be displayed
5. because of the IdPExemptionHeuristics, auto re-authn will be triggered because IdP claims that the user is returning
6. OnAccountSelected is invoked which would fail due to the embargo state, this eventually causes the UAF

p.s. the `mediation` bit in poc.html is in a wrong place.

This seems to be the same as crbug.com/40279117. Christian, could you please take a look?

### cb...@chromium.org (2024-02-21)

fix at https://chromium-review.googlesource.com/c/chromium/src/+/5314622, just need to write a test now

### ap...@google.com (2024-02-21)

Project: chromium/src
Branch: main

commit 89a78d70f971afe33954079157bdf226361a22ea
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Wed Feb 21 22:42:45 2024

    [FedCM] Protect from `this` getting deleted
    
    Bug: 325936438, 40279117
    Change-Id: If502ff076d7105791b75f3509cb5aa88ea76aa89
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5314622
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Reviewed-by: Zachary Tan <tanzachary@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1263632}

M       chrome/browser/ui/views/webid/fake_delegate.cc
M       chrome/browser/ui/views/webid/fake_delegate.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5314622


### ap...@google.com (2024-02-22)

Project: chromium/src
Branch: main

commit e91874a35e3e23319382588843e6293cc7fb55e2
Author: luci-bisection@appspot.gserviceaccount.com <luci-bisection@appspot.gserviceaccount.com>
Date:   Thu Feb 22 06:21:24 2024

    Revert "[FedCM] Protect from `this` getting deleted"
    
    This reverts commit 89a78d70f971afe33954079157bdf226361a22ea.
    
    Reason for revert:
    LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5718253215154176
    
    Sample build with failed test: https://ci.chromium.org/b/8755435936526279105
    Affected test(s):
    [ninja://chrome/test:unit_tests/FedCmAccountSelectionViewDesktopTest.IdpSigninStatusMismatchDialogToSigninFlow](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fchrome%2Ftest:unit_tests%2FFedCmAccountSelectionViewDesktopTest.IdpSigninStatusMismatchDialogToSigninFlow?q=VHash%3A3e4bab74bcdc7f95)
    
    If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5718253215154176&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F5314622&type=BUG
    
    Original change's description:
    > [FedCM] Protect from `this` getting deleted
    >
    > Bug: 325936438, 40279117
    > Change-Id: If502ff076d7105791b75f3509cb5aa88ea76aa89
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5314622
    > Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    > Reviewed-by: Zachary Tan <tanzachary@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1263632}
    >
    
    Bug: 325936438, 40279117
    Change-Id: I7da9aab9ff3f67e1bf4aa25b03396a63f17147e4
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5316658
    Owners-Override: Yoshisato Yanagisawa <yyanagisawa@google.com>
    Reviewed-by: Takashi Sakamoto <tasak@google.com>
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@google.com>
    Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1263810}

M       chrome/browser/ui/views/webid/fake_delegate.cc
M       chrome/browser/ui/views/webid/fake_delegate.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5316658


### pe...@google.com (2024-02-22)

Merge review required: a reverted commit was detected after the merge request.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-02-22)

Merge review required: a reverted commit was detected after the merge request.

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
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

### am...@chromium.org (2024-02-22)

reopening this issue since the fix was reverted

### ap...@google.com (2024-02-22)

Project: chromium/src
Branch: main

commit 2cbdbb93bffa23da2ea09a6eb1bc2f3269f37253
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Thu Feb 22 21:57:32 2024

    Reapply "[FedCM] Protect from `this` getting deleted"
    
    This reverts commit e91874a35e3e23319382588843e6293cc7fb55e2.
    
    Now adds initialization of popup_window_state_ to fix MSAN
    errors.
    
    R=npm@chromium.org
    
    Bug: 325936438, 40279117
    Change-Id: Ia99b3c81343bf01a8f37470b46a8d42db303cbaa
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5318014
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1264246}

M       chrome/browser/ui/views/webid/fake_delegate.cc
M       chrome/browser/ui/views/webid/fake_delegate.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5318014


### cb...@chromium.org (2024-02-22)

OK let's try this again. Answers to the merge survey:

1. Fixes a security bug
2. https://chromium-review.googlesource.com/c/chromium/src/+/5318014
3. Yes
4. n/a
5. n/a
6. No

### ap...@google.com (2024-02-23)

Project: chromium/src
Branch: main

commit 1cd94ca747514b2cd3a73956dd591f6d8d576318
Author: Peter Marshall <petermarshall@chromium.org>
Date:   Fri Feb 23 03:19:50 2024

    Revert "Reapply "[FedCM] Protect from `this` getting deleted""
    
    This reverts commit 2cbdbb93bffa23da2ea09a6eb1bc2f3269f37253.
    
    Reason for revert: Failing on ASAN/LSAN:
    https://ci.chromium.org/ui/p/chromium/builders/ci/Linux%20Chromium%20OS%20ASan%20LSan%20Tests%20(1)/56340/overview
    
    Original change's description:
    > Reapply "[FedCM] Protect from `this` getting deleted"
    >
    > This reverts commit e91874a35e3e23319382588843e6293cc7fb55e2.
    >
    > Now adds initialization of popup_window_state_ to fix MSAN
    > errors.
    >
    > R=npm@chromium.org
    >
    > Bug: 325936438, 40279117
    > Change-Id: Ia99b3c81343bf01a8f37470b46a8d42db303cbaa
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5318014
    > Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    > Reviewed-by: Nicolás Peña <npm@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1264246}
    
    Bug: 325936438, 40279117
    Change-Id: If0edbbf8c0a8e67893060e582036c28dc08c5474
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5320170
    Reviewed-by: Peter Marshall <petermarshall@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Owners-Override: Peter Marshall <petermarshall@chromium.org>
    Commit-Queue: Peter Marshall <petermarshall@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1264400}

M       chrome/browser/ui/views/webid/fake_delegate.cc
M       chrome/browser/ui/views/webid/fake_delegate.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5320170


### am...@chromium.org (2024-02-23)

Hi cbiesinger@ sorry, needing to reopen this issue once again, it looks like the fix (<https://crrev.com/c/5318014>) has once again been reverted

### cb...@chromium.org (2024-02-23)

Thanks Amy. Turns out the test I added exposed a pre-existing memory leak, sigh.

### ap...@google.com (2024-02-23)

Project: chromium/src
Branch: main

commit 953d0643b74814941a771bd3d6e9bd52fc2d697e
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Fri Feb 23 19:34:51 2024

    Reapply "Reapply "[FedCM] Protect from `this` getting deleted""
    
    This reverts commit 1cd94ca747514b2cd3a73956dd591f6d8d576318.
    
    Bug: 325936438, 40279117
    Change-Id: Iae4f1ebb8b953577c7118ceec25f05783620800a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5319066
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1264685}

M       chrome/browser/ui/views/webid/fake_delegate.cc
M       chrome/browser/ui/views/webid/fake_delegate.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5319066


### cb...@chromium.org (2024-02-23)

The asan and msan trybots are passing. Let's see what happens over the weekend...

### cb...@chromium.org (2024-02-26)

The bots seem happy but I've been pointed to another crash that this causes.

My plan is:
1) Revert the latest CL, reland https://chromium-review.googlesource.com/c/chromium/src/+/5318014 but without the test -- the test exposes some pre-existing issues unrelated to the security issue
2) Merge that CL to the branch to fix the security issue
3) Figure out how to fix the pre-existing issue on trunk (a memory leak)

### ap...@google.com (2024-02-26)

Project: chromium/src
Branch: main

commit cff7121ecc72c81b6c0c6d91ebbdd3357c2a3810
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Mon Feb 26 17:22:22 2024

    Revert "Reapply "Reapply "[FedCM] Protect from `this` getting deleted"""
    
    This reverts commit 953d0643b74814941a771bd3d6e9bd52fc2d697e.
    
    Reason for revert: Causes a crash in certain circumstances
    
    Original change's description:
    > Reapply "Reapply "[FedCM] Protect from `this` getting deleted""
    >
    > This reverts commit 1cd94ca747514b2cd3a73956dd591f6d8d576318.
    >
    > Bug: 325936438, 40279117
    > Change-Id: Iae4f1ebb8b953577c7118ceec25f05783620800a
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5319066
    > Reviewed-by: Nicolás Peña <npm@chromium.org>
    > Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1264685}
    
    Bug: 325936438, 40279117
    Change-Id: I3c90b2be031b77401af6a936808c6ada6de4c10e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5323342
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1265271}

M       chrome/browser/ui/views/webid/fake_delegate.cc
M       chrome/browser/ui/views/webid/fake_delegate.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5323342


### ap...@google.com (2024-02-26)

Project: chromium/src
Branch: main

commit ffdfc28b03b864bfc013aebb802e3378da475bb2
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Mon Feb 26 19:18:01 2024

    Reapply "Reapply "[FedCM] Protect from `this` getting deleted""
    
    This reverts commit 1cd94ca747514b2cd3a73956dd591f6d8d576318.
    
    Relanding without the test so that this can be merged to the branch.
    
    Bug: 325936438, 40279117
    Change-Id: I54415209c403119e6be0d200b18cd8bf2b8f159f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5324640
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1265348}

M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h

https://chromium-review.googlesource.com/5324640


### cb...@chromium.org (2024-02-26)

OK, that last commit fixes the security bug & should be safe to merge to the branch. Questionnaire:

1. Fixes a security bug
2. https://chromium-review.googlesource.com/c/chromium/src/+/5324640
3. Yes
4. n/a
5. n/a
6. No

### ap...@google.com (2024-02-27)

Project: chromium/src
Branch: main

commit 4abec046ae8d2a5e79e3871320e2def15fb69765
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Tue Feb 27 16:26:09 2024

    [FedCM] Fix memory leak in FedCmAccountSelectionView
    
    If we do not create a dialog widget, nothing deletes the
    FedCmAccountSelectionView. This patch fixes that.
    
    Found with the test I was going to add for bug 325936438. This
    CL adds the test I wanted to add for that bug.
    
    Bug: 325936438, 40279117
    Change-Id: Id1173fd56881a2099d34748835bfb705a46b76f3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5321496
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Reviewed-by: Yi Gu <yigu@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1265834}

M       chrome/browser/ui/views/webid/fake_delegate.cc
M       chrome/browser/ui/views/webid/fake_delegate.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5321496


### pe...@google.com (2024-02-27)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

### cb...@chromium.org (2024-02-27)

Amy/Srinivas, could you help me get the merge approved (comment 26)? Thanks!

### am...@chromium.org (2024-02-27)

Hi Christian, it's in the queue :) Since latest commit just landed yesterday, we'll need it to get a bit more canary bake time before we can approve for Beta or Stable merges.

### cb...@chromium.org (2024-02-27)

OK thanks!

### am...@google.com (2024-02-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-29)

Congratulations Rong! The Chrome VRP Panel has decided to award you $5,000 for this mildly mitigated memory corruption bug in a non-sandboxed process, mitigated by user interaction consistent with FedCM workflow, + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!

### am...@chromium.org (2024-03-01)

not seeing any issues based on latest canary data related to <https://crrev.com/c/5324640>
merge approves approved for M123 and M122
Please merge this fix to 123 Beta (branch 6312) by EOD Tuesday, 5 March so this fix can be included in the next Beta update; please merge to 122 Stable (branch 6261) by EOD Thursday, 7 March so this fix can be included in the next 122 Stable update -- thank you

### cb...@chromium.org (2024-03-04)

122 merge: https://chromium-review.googlesource.com/c/chromium/src/+/5341312

123 merge: https://chromium-review.googlesource.com/c/chromium/src/+/5340993

### ap...@google.com (2024-03-04)

Project: chromium/src
Branch: refs/branch-heads/6312

commit 53b851fd2d88bcf6f75e3d310d3410a86185ac3a
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Mon Mar 04 18:14:59 2024

    M123: Reapply "Reapply "[FedCM] Protect from `this` getting deleted""
    
    This reverts commit 1cd94ca747514b2cd3a73956dd591f6d8d576318.
    
    Relanding without the test so that this can be merged to the branch.
    
    (cherry picked from commit ffdfc28b03b864bfc013aebb802e3378da475bb2)
    
    Bug: 325936438, 40279117
    Change-Id: I54415209c403119e6be0d200b18cd8bf2b8f159f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5324640
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1265348}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5340993
    Cr-Commit-Position: refs/branch-heads/6312@{#352}
    Cr-Branched-From: 6711dcdae48edaf98cbc6964f90fac85b7d9986e-refs/heads/main@{#1262506}

M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h

https://chromium-review.googlesource.com/5340993


### ap...@google.com (2024-03-04)

Project: chromium/src
Branch: refs/branch-heads/6261

commit 389c3fad9c8e0093d5c3a907a46e791c7c254dc3
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Mon Mar 04 18:44:24 2024

    M122: Reapply "Reapply "[FedCM] Protect from `this` getting deleted""
    
    This reverts commit 1cd94ca747514b2cd3a73956dd591f6d8d576318.
    
    Relanding without the test so that this can be merged to the branch.
    
    (cherry picked from commit ffdfc28b03b864bfc013aebb802e3378da475bb2)
    
    Bug: 325936438, 40279117
    Change-Id: I54415209c403119e6be0d200b18cd8bf2b8f159f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5324640
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1265348}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5341312
    Cr-Commit-Position: refs/branch-heads/6261@{#1007}
    Cr-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}

M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h

https://chromium-review.googlesource.com/5341312


### pe...@google.com (2024-03-05)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### cb...@chromium.org (2024-03-05)

1) No
2) I don't believe so

### pe...@google.com (2024-03-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-03-19)

1. One <https://crrev.com/c/5370050>
2. Low, some small conflicts
3. M122, M123
4. Yes

### ap...@google.com (2024-04-01)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 46505d3383b480e4e527e70a392ced098da19aa8
Author: Zakhar Voit <voit@google.com>
Date:   Mon Apr 01 18:58:29 2024

    [M120-LTS] Reapply "Reapply "[FedCM] Protect from `this` getting deleted""
    
    This reverts commit 1cd94ca747514b2cd3a73956dd591f6d8d576318.
    
    Relanding without the test so that this can be merged to the branch.
    
    (cherry picked from commit ffdfc28b03b864bfc013aebb802e3378da475bb2)
    
    (cherry picked from commit 389c3fad9c8e0093d5c3a907a46e791c7c254dc3)
    
    Bug: 325936438, 40279117
    Change-Id: I54415209c403119e6be0d200b18cd8bf2b8f159f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5324640
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1265348}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5341312
    Cr-Original-Commit-Position: refs/branch-heads/6261@{#1007}
    Cr-Original-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5370050
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
    Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
    Reviewed-by: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1999}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h

https://chromium-review.googlesource.com/5370050


### pe...@google.com (2024-06-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/325936438)*
