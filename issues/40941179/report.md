# Security: UAF in FedCmAccountSelectionView::Show

| Field | Value |
|-------|-------|
| **Issue ID** | [40941179](https://issues.chromium.org/issues/40941179) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | yi...@chromium.org |
| **Created** | 2023-11-09 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

In function `FedCmAccountSelectionView::Show`, if the auto re-authn flow is triggered, it will call `FedCmAccountSelectionView::ShowVerifyingSheet` to update the FedCM bubble to show the "verifying" sheet [1]. However, ShowVerifyingSheet also calls `AccountSelectionView::Delegate::OnAccountSelected`, which might complete the request with error and destroy the FedCmAccountSelectionView object [2], and a UAF would occur when the function continue to access its class member at line [3].

```
void FedCmAccountSelectionView::Show(  
    const std::string& top_frame_etld_plus_one,  
    const absl::optional<std::string>& iframe_etld_plus_one,  
    const std::vector<content::IdentityProviderData>&  
        identity_provider_data_list,  
    Account::SignInMode sign_in_mode,  
    bool show_auto_reauthn_checkbox) {  
  // ...  
  if (sign_in_mode == Account::SignInMode::kAuto) {  
    state_ = State::AUTO_REAUTHN;  
  
    // When auto re-authn flow is triggered, the parameter  
    // |identity_provider_data_list| would only include the single returning  
    // account and its IDP.  
    DCHECK_EQ(idp_display_data_list_.size(), 1u);  
    DCHECK_EQ(idp_display_data_list_[0].accounts.size(), 1u);  
    ShowVerifyingSheet(idp_display_data_list_[0].accounts[0],  // ===> [1]  
                       idp_display_data_list_[0]);  
  // ...  
  if (create_bubble || is_modal_closed_but_accounts_fetch_pending_) {  
    is_modal_closed_but_accounts_fetch_pending_ = false;       // ===> [3]  
    if (is_web_contents_visible_) {  
      input_protector_->VisibilityChanged(true);  
      bubble_widget_->Show();  
  }  
  
void FederatedAuthRequestImpl::OnAccountSelected(const GURL& idp_config_url,  
                                                 const std::string& account_id,  
                                                 bool is_sign_in) {  
  // ...  
  if (GetApiPermissionStatus(idp_origin) !=  
      FederatedApiPermissionStatus::GRANTED) {  
    CompleteRequestWithError(                                  // ===> [2]  
        FederatedAuthRequestResult::kErrorDisabledInSettings,  
        TokenStatus::kDisabledInSettings,  
        /\*token_error=\*/absl::nullopt,  
        /\*should_delay_callback=\*/true);  
    return;  
  }  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=132;drc=7fa0c25da15ae39bbd2fd720832ec4df4fee705a>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=1773;drc=7fa0c25da15ae39bbd2fd720832ec4df4fee705a>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=146;drc=7fa0c25da15ae39bbd2fd720832ec4df4fee705a>

**VERSION**  

Chrome Version: stable + dev

**REPRODUCTION CASE**

1. Create a web server using node.js  
   
   node ./server.js
2. Launch chrome and navigate to <http://localhost:8000/poc.html>  
   
   out/Asan/chrome <http://localhost:8000/poc.html>
3. Click the 'Sign in with Google' button, then continue sign-in in the new popup window, after sign in completes, close the bubble at the original page

The page is designed to look like phishing to make the user interaction more reasonable. And please make sure to clear browser user data and create a new web server before each testing.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log

== Bisection ==  

This was initially introduced in <https://chromium.googlesource.com/chromium/src/+/456cd26b1a6bc5263d60eca78870832bbc748299> and was refactored in <https://chromium.googlesource.com/chromium/src/+/6294a136491cf20ee370c8c5eb6fd078c2ab1db2>

== Additional Information ==  

compromised renderer requirement: no  

miracle ptr protected: no  

user interaction: yes

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 669 B)
- [child.html](attachments/child.html) (text/plain, 1.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 161.9 KB)
- [server.js](attachments/server.js) (text/plain, 2.6 KB)
- [child.html](attachments/child.html) (text/plain, 1001 B)
- [poc.html](attachments/poc.html) (text/plain, 619 B)
- [server.js](attachments/server.js) (text/plain, 2.6 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-11-09)

[Empty comment from Monorail migration]

### jt...@gmail.com (2023-11-09)

[Comment Deleted]

### es...@chromium.org (2023-11-09)

I wasn't able to reproduce this; the crash didn't happen on a non-ASAN build, and on an ASAN build the sign-in flow doesn't work; the "Sign in with Google" doesn't appear for some reason. Nevertheless I'll send this to the feature team since the report is high quality.

I've downgraded severity to High because of the specific user interaction required.

[Monorail components: Blink>Identity>FedCM]

### [Deleted User] (2023-11-09)

[Empty comment from Monorail migration]

### jt...@gmail.com (2023-11-10)

Re #3
Ah I accidentally include the  `setStatus` call in the poc which may break things, just delete those lines should work. Sorry about that.

### es...@chromium.org (2023-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-23)

yigu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### np...@chromium.org (2023-11-23)

[Empty comment from Monorail migration]

### yi...@chromium.org (2023-11-24)

Hi reporter, could you let us know about the Chrome version? I couldn't reproduce it M121 with an asan build.
Also the recorded video from #3 doesn't seem to have auto re-authn triggered?

### jt...@gmail.com (2023-11-27)

Re #10
> could you let us know about the Chrome version?
The version of Chrome used in the video is 121.0.6110.1 on Ubuntu. I also downloaded and tested asan build 121.0.6151.0 on Windows platform from Google storage bucket [1], as shown in the attached video.
[1] https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1229133.zip?generation=1701053496780064&alt=media
"metadata": {
  "cr-commit-position": "refs/heads/main@{#1229133}",
  "cr-commit-position-number": "1229133",
  "cr-git-commit": "01135652f33f75ad0590f209223392b6252fb849"
}

> Also the recorded video from #3 doesn't seem to have auto re-authn triggered?
This is because the re-authn verifying sheet would not show when the UAF occurs. FedCmAccountSelectionView::Show calls FedCmAccountSelectionView::ShowVerifyingSheet and then calls OnAccountSelected which may destroy the FedCmAccountSelectionView object. If so, FedCmAccountSelectionView::ShowVerifyingSheet would not call AccountSelectionBubbleView::ShowVerifyingSheet because of the invalid state of weak_ptr at line[2].
```
void FedCmAccountSelectionView::ShowVerifyingSheet(
    const Account& account,
    const IdentityProviderDisplayData& idp_display_data) {
  DCHECK(state_ == State::VERIFYING || state_ == State::AUTO_REAUTHN);
  notify_delegate_of_dismiss_ = false;

  base::WeakPtr<FedCmAccountSelectionView> weak_ptr(
      weak_ptr_factory_.GetWeakPtr());
  delegate_->OnAccountSelected(idp_display_data.idp_metadata.config_url,
                               account);
  // AccountSelectionView::Delegate::OnAccountSelected() might delete this.
  // See https://crbug.com/1393650 for details.
  if (!weak_ptr) {   // ===> [2]
    return;
  }
```

Please be noted to clear browser user data and create a new web server instance before EACH testing. Feel free to let me know if the UAF still cannot be reproduced.

### gi...@appspot.gserviceaccount.com (2023-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/98676a2f66c4b4b802316eef70f4aab77e631f85

commit 98676a2f66c4b4b802316eef70f4aab77e631f85
Author: Yi Gu <yigu@chromium.org>
Date: Tue Nov 28 15:51:40 2023

[FedCM] Check API permission before showing accounts UI

The accounts fetch could be delayed for legitimate reasons. A user may be
able to disable FedCM API (e.g. via settings or dismissing another FedCM
UI on the same RP origin) before the browser receives the accounts
response.

This patch checks the API permission before showing the accounts UI.

Change-Id: Idbbe88912941113ec3f54d7f222845cd774dc897
Bug: 1500921
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5064052
Commit-Queue: Yi Gu <yigu@chromium.org>
Reviewed-by: Christian Biesinger <cbiesinger@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1229912}

[modify] https://crrev.com/98676a2f66c4b4b802316eef70f4aab77e631f85/content/browser/webid/federated_auth_request_impl.cc
[modify] https://crrev.com/98676a2f66c4b4b802316eef70f4aab77e631f85/content/browser/webid/federated_auth_request_impl.h
[modify] https://crrev.com/98676a2f66c4b4b802316eef70f4aab77e631f85/content/browser/webid/federated_auth_request_impl_unittest.cc


### yi...@chromium.org (2023-11-28)

Thanks for the report and coming up with the very interesting test case!


### cb...@chromium.org (2023-11-28)

Hmm when I reviewed the CL I didn't realize this was fixing a UAF. I haven't looked in detail but it feels like there's also an ownership issue somewhere that maybe should be addressed more directly?

### yi...@chromium.org (2023-11-28)

Here are what happened in the bug:
1. website triggers TWO FedCM UI (A from rp.com and B from a pop-up window with rp.com/child)
2. user clicks "Continue as" on B, which stores the sharing permission for the RP
3. right after the previous promise is resolved, another FedCM API call is invoked, but this time the IdP server holds the accounts response which leaves the flow in a pending state
4. user dismisses the UI A which triggers embargo
5. since we reject the promise immediately upon dismissal, the JS sends a fetch to the server to unblock the accounts response
6. the browser receives the accounts response from step 3 and triggers auto reauthn (all conditions are met and we don't check FedCM API settings)
7. upon showing the auto reauthn UI, we call OnAccountSelected which checks API permission. Since FedCM is embargoed, we'd go with CompleteWithError directly and destroy the controller.
8. Access to the UI code after step 7 leads to a UAF.

Do you think there's an ownership issue here?

### cb...@chromium.org (2023-11-28)

Well IMO CompleteRequestWithError should not lead to UAF. Is this the same as https://crbug.com/chromium/1473775?

### yi...@chromium.org (2023-11-28)

aha it's exactly like that bug

### cb...@chromium.org (2023-11-28)

OK great, so we can use this bug for the immediate fix & potential branch merge and that bug for a broader fix.

### [Deleted User] (2023-11-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-28)

Requesting merge to extended stable M118 because latest trunk commit (1229912) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1229912) appears to be after stable branch point (1204232).

Requesting merge to beta M120 because latest trunk commit (1229912) appears to be after beta branch point (1217362).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-28)

Last scheduled releases of M119 Stable and M118 Extended Stable were released earlier today, so no merges to 118 and 119 are no longer needed. 
M120 Stable RC is in the process of being cut today. And since this fix was landed just a few hours ago, it needs a bit more bake time on Canary. I'll revisit later this week for merge review for 120 so this fix can be potentially included in the first security update of M120. 

### [Deleted User] (2023-11-29)

Merge review required: M120 has already been cut for stable release.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-11-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-30)

Congratulations R0ng! The Chrome VRP Panel has decided to award you $5,000 for this mildly mitigated (mitigate by sign-in and user interaction) security bug in a non-sandboxed process + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### yi...@chromium.org (2023-11-30)

1. Why does your merge fit within the merge criteria for these milestones?
High severity security bug fix
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/5064052
3. Have the changes been released and tested on canary?
Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
No
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
N/A


### am...@chromium.org (2023-11-30)

M120 merge approved for https://crrev.com/c/5064052; please merge this fix to branch 6099 at your earliest convenience (before EOD next Thursday (12/7) so this fix can be included in the first update of M120 Stable. 

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/998e947b265f6c96346dafdf2fb65b8c07759344

commit 998e947b265f6c96346dafdf2fb65b8c07759344
Author: Yi Gu <yigu@chromium.org>
Date: Fri Dec 01 00:10:37 2023

[FedCM] Check API permission before showing accounts UI

The accounts fetch could be delayed for legitimate reasons. A user may be
able to disable FedCM API (e.g. via settings or dismissing another FedCM
UI on the same RP origin) before the browser receives the accounts
response.

This patch checks the API permission before showing the accounts UI.

(cherry picked from commit 98676a2f66c4b4b802316eef70f4aab77e631f85)

Change-Id: Idbbe88912941113ec3f54d7f222845cd774dc897
Bug: 1500921
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5064052
Commit-Queue: Yi Gu <yigu@chromium.org>
Reviewed-by: Christian Biesinger <cbiesinger@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1229912}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5074630
Auto-Submit: Yi Gu <yigu@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#1255}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/998e947b265f6c96346dafdf2fb65b8c07759344/content/browser/webid/federated_auth_request_impl.cc
[modify] https://crrev.com/998e947b265f6c96346dafdf2fb65b8c07759344/content/browser/webid/federated_auth_request_impl.h
[modify] https://crrev.com/998e947b265f6c96346dafdf2fb65b8c07759344/content/browser/webid/federated_auth_request_impl_unittest.cc


### [Deleted User] (2023-12-01)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-12-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-11)

[Empty comment from Monorail migration]

### rz...@google.com (2023-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-14)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-12-14)

1. Just https://crrev.com/c/5095846
2. Low, just a simple conflict
3. 120
4. Yes

### am...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### na...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### na...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08f72db40703193c5ee5cbc952aced96044f9ee0

commit 08f72db40703193c5ee5cbc952aced96044f9ee0
Author: Yi Gu <yigu@chromium.org>
Date: Fri Jan 12 19:36:01 2024

[M114-LTS][FedCM] Check API permission before showing accounts UI

M114 merge issues:
  content/browser/webid/federated_auth_request_impl.h/cc:
    - The GetApiPermissionStatus() doesn't exist in 114, it uses api_permission_delegate_
    directly.

The accounts fetch could be delayed for legitimate reasons. A user may be
able to disable FedCM API (e.g. via settings or dismissing another FedCM
UI on the same RP origin) before the browser receives the accounts
response.

This patch checks the API permission before showing the accounts UI.

(cherry picked from commit 98676a2f66c4b4b802316eef70f4aab77e631f85)

Change-Id: Idbbe88912941113ec3f54d7f222845cd774dc897
Bug: 1500921
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5064052
Commit-Queue: Yi Gu <yigu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1229912}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5095846
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Christian Biesinger <cbiesinger@chromium.org>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1663}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/08f72db40703193c5ee5cbc952aced96044f9ee0/content/browser/webid/federated_auth_request_impl.cc
[modify] https://crrev.com/08f72db40703193c5ee5cbc952aced96044f9ee0/content/browser/webid/federated_auth_request_impl_unittest.cc


### rz...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-12)

This issue was migrated from crbug.com/chromium/1500921?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pe...@google.com (2024-03-25)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40941179)*
