# Security: UAF in OnAccessTokenRefreshFailed

| Field | Value |
|-------|-------|
| **Issue ID** | [40060220](https://issues.chromium.org/issues/40060220) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | iOS |
| **Reporter** | ya...@gmail.com |
| **Assignee** | jl...@google.com |
| **Created** | 2022-07-09 |
| **Bounty** | $3,000.00 |

## Description

  std::unique_ptr<KeyedService> BuildAuthenticationService(
    web::BrowserState* context) {
  ChromeBrowserState* browser_state =
      ChromeBrowserState::FromBrowserState(context);
  return std::make_unique<AuthenticationService>(   //[0]
      browser_state->GetPrefs(),
      SyncSetupServiceFactory::GetForBrowserState(browser_state),
      ChromeAccountManagerServiceFactory::GetForBrowserState(browser_state),
      IdentityManagerFactory::GetForBrowserState(browser_state),
      SyncServiceFactory::GetForBrowserState(browser_state));
}


void AuthenticationService::OnAccessTokenRefreshFailed(
    ChromeIdentity* identity,
    NSDictionary* user_info) {
  if (HandleMDMNotification(identity, user_info)) {
    return;
  }

  ios::ChromeIdentityService* identity_service =
      ios::GetChromeBrowserProvider().GetChromeIdentityService();
  if (!identity_service->IsInvalidGrantError(user_info)) {

  // If the failure is not due to an invalid grant, the identity is not
    // invalid and there is nothing to do.
    return;
  }

  // Handle the failure of access token refresh on the next message loop cycle.
  // |identity| is now invalid and the authentication service might need to
  // react to this loss of identity.
  // Note that no reload of the credentials is necessary here, as |identity|
  // might still be accessible in SSO, and |OnIdentityListChanged| will handle
  // this when |identity| will actually disappear from SSO.
  base::ThreadTaskRunnerHandle::Get()->PostTask(
      FROM_HERE,
      base::BindOnce(&AuthenticationService::HandleForgottenIdentity,    //[1] 
                     base::Unretained(this), identity, /*should_prompt=*/true,   
                     /*device_restore=*/false));
}




This is same as https://crbug.com/chromium/1341907.AuthenticationService[0] Object will be created as a service. When the browser is closed, the service will also be down, the object will be destroyed, and HandleForgottenIdentity is bound to the callback function as base::Unretained,will continue to execute in the child thread, causing UAF.

Note:I don't have an ios device, so no PoC.


Patch

Use weakptr


## Timeline

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-10)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-10)

[Empty comment from Monorail migration]

### ya...@gmail.com (2022-07-12)

Please assign to the owner.Thanks!

### dc...@chromium.org (2022-07-14)

Talked with the iOS team. In iOS, KeyedService lifetime is tied to BrowserState, which is destroyed when the last incognito window is destroyed, or the browser is shutdown.

Medium; despite the fact that this is a use-after-free in the browser process, this doesn't seem like something that's easily exploitable.

Also marking this as blocking 1342236; since we've received many of these reports lately, we've started tracking some efforts to broadly mitigate these bugs rather than address them one at a time.

[Monorail components: Services>SignIn]

### dc...@chromium.org (2022-07-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-14)

[Empty comment from Monorail migration]

### jl...@chromium.org (2022-07-22)

[Empty comment from Monorail migration]

### jl...@chromium.org (2022-07-22)

[Empty comment from Monorail migration]

### jl...@chromium.org (2022-07-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/18a29d6b6d83a1739196bc784f311c2c79e224dc

commit 18a29d6b6d83a1739196bc784f311c2c79e224dc
Author: Jérôme Lebel <jlebel@chromium.org>
Date: Fri Jul 22 14:42:20 2022

[iOS] Use weak ptr to post task in AuthenticationService

Need to use weak ptr to post a task since during the shutdown
AuthenticationService might disappear before the task is call.
That should be a very rare case.

Fixed: 1343141
Change-Id: Ice842018b4ba3c7d1c84bc6a44636e7ab6529f2e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3779890
Auto-Submit: Jérôme Lebel <jlebel@chromium.org>
Commit-Queue: Boris Sazonov <bsazonov@chromium.org>
Reviewed-by: Boris Sazonov <bsazonov@chromium.org>
Commit-Queue: Jérôme Lebel <jlebel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1027224}

[modify] https://crrev.com/18a29d6b6d83a1739196bc784f311c2c79e224dc/ios/chrome/browser/signin/authentication_service.mm


### [Deleted User] (2022-07-22)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jl...@chromium.org (2022-07-22)

[Comment Deleted]

### jl...@chromium.org (2022-07-22)

This bug exists at least since 2016 (probably before). I don't think this crash can be exploited since it can only occur during shutdown. I'm tempted to remove Security_Severity, but I'm no expert on security.
Let me know how to proceed.


### [Deleted User] (2022-07-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2022-07-26)

Since M103 is the current stable, tagging with FoundIn-103 to indicate it affects all current versions and marking this as fixed again.

A use-after-free is a use-after-free; if this were unreachable (due to being guarded by some flag or another that's off by default), then we could mark it as Security-Impact_None, but that's not the case.

### [Deleted User] (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

Requesting merge to beta M104 because latest trunk commit (1027224) appears to be after beta branch point (1012729).

Requesting merge to dev M105 because latest trunk commit (1027224) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

Merge approved: your change passed merge requirements and is auto-approved for M105. Please go ahead and merge the CL to branch 5195 (refs/branch-heads/5195) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS),  matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

Merge review required: M104 has already been cut for stable release.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bs...@chromium.org (2022-07-27)

Jérôme is OOO, so I'll do the merge to M105.

dcheng@ do you believe this should be merged in M104? This UAF doesn't seem exploitable, so I'm not sure if merging makes sense.

### am...@chromium.org (2022-07-27)

Because this is a UAF in the browser process, but is mitigated by requiring shutdown, it is a medium severity security and should be backmerged to M104 as this is being cut for stable release soon, and will become Extended Stable once M105 is promoted to stable. 
As long as there are not stability issues and other concerns with the compatibility of this issue being backported to M104, it should be merged to branch 5112 at your earliest availability to do so. 

### am...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/72ad1e1cc9e2d08c20174cb84815cb174a517c48

commit 72ad1e1cc9e2d08c20174cb84815cb174a517c48
Author: Jérôme Lebel <jlebel@chromium.org>
Date: Wed Jul 27 17:43:15 2022

[M104][iOS] Use weak ptr to post task in AuthenticationService

Need to use weak ptr to post a task since during the shutdown
AuthenticationService might disappear before the task is call.
That should be a very rare case.

(cherry picked from commit 18a29d6b6d83a1739196bc784f311c2c79e224dc)

Fixed: 1343141
Change-Id: Ice842018b4ba3c7d1c84bc6a44636e7ab6529f2e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3779890
Auto-Submit: Jérôme Lebel <jlebel@chromium.org>
Commit-Queue: Boris Sazonov <bsazonov@chromium.org>
Reviewed-by: Boris Sazonov <bsazonov@chromium.org>
Commit-Queue: Jérôme Lebel <jlebel@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1027224}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3789333
Reviewed-by: Harry Souders <harrysouders@google.com>
Owners-Override: Harry Souders <harrysouders@google.com>
Auto-Submit: Boris Sazonov <bsazonov@chromium.org>
Commit-Queue: Harry Souders <harrysouders@google.com>
Cr-Commit-Position: refs/branch-heads/5112@{#1238}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/72ad1e1cc9e2d08c20174cb84815cb174a517c48/ios/chrome/browser/signin/authentication_service.mm


### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0868b1c9d798fef60e22e3e3ca24a0e7b23d0b42

commit 0868b1c9d798fef60e22e3e3ca24a0e7b23d0b42
Author: Jérôme Lebel <jlebel@chromium.org>
Date: Thu Jul 28 15:14:17 2022

[M105][iOS] Use weak ptr to post task in AuthenticationService

Need to use weak ptr to post a task since during the shutdown
AuthenticationService might disappear before the task is call.
That should be a very rare case.

(cherry picked from commit 18a29d6b6d83a1739196bc784f311c2c79e224dc)

Fixed: 1343141
Change-Id: Ice842018b4ba3c7d1c84bc6a44636e7ab6529f2e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3779890
Auto-Submit: Jérôme Lebel <jlebel@chromium.org>
Commit-Queue: Boris Sazonov <bsazonov@chromium.org>
Reviewed-by: Boris Sazonov <bsazonov@chromium.org>
Commit-Queue: Jérôme Lebel <jlebel@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1027224}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3783027
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: David Roger <droger@chromium.org>
Auto-Submit: Boris Sazonov <bsazonov@chromium.org>
Cr-Commit-Position: refs/branch-heads/5195@{#91}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/0868b1c9d798fef60e22e3e3ca24a0e7b23d0b42/ios/chrome/browser/signin/authentication_service.mm


### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-04)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided upon based on report quality (no POC or stack trace) and this issue being mitigated by browser shutdown and limited exploitability potential. A member of our finance team will be in touch to arrange payment. Please let us know the name/tag you would like us to use for acknowledging you for this issue. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1343141?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1342236]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060220)*
