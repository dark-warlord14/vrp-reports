# Security:  Use After Free in PasswordsPrivateDelegateImpl::OsReauthTimeoutCall,

| Field | Value |
|-------|-------|
| **Issue ID** | [40061558](https://issues.chromium.org/issues/40061558) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Passwords, UI>Settings |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | yq...@gmail.com |
| **Assignee** | de...@google.com |
| **Created** | 2022-11-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

KeyedService\* PasswordsPrivateDelegateFactory::BuildServiceInstanceFor(  

content::BrowserContext\* profile) const {  

return new PasswordsPrivateDelegateImpl(static\_cast<Profile\*>(profile)); //[0]  

}

PasswordsPrivateDelegateImpl::PasswordsPrivateDelegateImpl(Profile\* profile)  

: profile\_(profile),  

saved\_passwords\_presenter\_(  

AffiliationServiceFactory::GetForProfile(profile),  

PasswordStoreFactory::GetForProfile(  

profile,  

ServiceAccessType::EXPLICIT\_ACCESS),  

AccountPasswordStoreFactory::GetForProfile(  

profile,  

ServiceAccessType::EXPLICIT\_ACCESS)),  

password\_manager\_porter\_(std::make\_unique<PasswordManagerPorter>(  

profile,  

&saved\_passwords\_presenter\_,  

base::BindRepeating(  

&PasswordsPrivateDelegateImpl::OnPasswordsExportProgress,  

base::Unretained(this)))),  

password\_access\_authenticator\_(  

base::BindRepeating(&PasswordsPrivateDelegateImpl::OsReauthCall,  

base::Unretained(this)),  

base::BindRepeating(  

&PasswordsPrivateDelegateImpl::OsReauthTimeoutCall,  

base::Unretained(this))), //[1]

void PasswordsPrivateDelegateImpl::OsReauthCall(  

password\_manager::ReauthPurpose purpose,  

password\_manager::PasswordAccessAuthenticator::AuthResultCallback  

callback) {  

#if BUILDFLAG(IS\_WIN)  

AuthenticateWithBiometrics(  

password\_manager\_util\_win::GetMessageForLoginPrompt(purpose),  

std::move(callback));  

#elif BUILDFLAG(IS\_MAC)  

// TODO([crbug.com/1358442](https://crbug.com/1358442)): Remove this check.  

if (GetBiometricAuthenticator(web\_contents\_)  

->CanAuthenticate(  

device\_reauth::BiometricAuthRequester::kPasswordsInSettings) &&  

base::FeatureList::IsEnabled(  

password\_manager::features::kBiometricAuthenticationInSettings)) {  

AuthenticateWithBiometrics(  

password\_manager\_util\_mac::GetMessageForBiometricLoginPrompt(purpose),  

std::move(callback)); //[2]  

} else {  

bool result = password\_manager\_util\_mac::AuthenticateUser(purpose);  

std::move(callback).Run(result);  

}

void PasswordsPrivateDelegateImpl::AuthenticateWithBiometrics(  

const std::u16string& message,  

password\_manager::PasswordAccessAuthenticator::AuthResultCallback  

callback) {  

#if !BUILDFLAG(IS\_MAC) && !BUILDFLAG(IS\_WIN)  

NOTIMPLEMENTED();  

#else  

// Cancel any ongoing authentication attempt.  

if (biometric\_authenticator\_) {  

// TODO([crbug.com/1371026](https://crbug.com/1371026)): Remove Cancel and instead simply destroy  

// |biometric\_authenticator\_|.  

biometric\_authenticator\_->Cancel(  

device\_reauth::BiometricAuthRequester::kPasswordsInSettings);  

}  

biometric\_authenticator\_ = GetBiometricAuthenticator(web\_contents\_);

base::OnceClosure on\_reauth\_completed =  

base::BindOnce(&PasswordsPrivateDelegateImpl::OnReauthCompleted,  

weak\_ptr\_factory\_.GetWeakPtr());

biometric\_authenticator\_->AuthenticateWithMessage(  

device\_reauth::BiometricAuthRequester::kPasswordsInSettings, message,  

std::move(callback).Then(std::move(on\_reauth\_completed))); //[3]  

#endif  

}

void BiometricAuthenticatorWin::AuthenticateWithMessage(  

device\_reauth::BiometricAuthRequester requester,  

const std::u16string& message,  

AuthenticateCallback callback) {  

if (!NeedsToAuthenticate()) {  

base::SequencedTaskRunnerHandle::Get()->PostTask(  

FROM\_HERE, base::BindOnce(std::move(callback), /\*success=\*/true)); //[4]  

return;  

}

authenticator\_->AuthenticateUser(  

message,  

base::BindOnce(&BiometricAuthenticatorWin::RecordAuthenticationResult,  

base::Unretained(this))  

.Then(std::move(callback)));  

}

PasswordsPrivateDelegateImpl [0] is build for service.And the callback [1] post task in [4] is bind as unretaind.So when browser down,the PasswordsPrivateDelegateImpl is destroyed.And UAF occur in PasswordsPrivateDelegateImpl::OsReauthTimeoutCall [1].

PATCH

from base::Unretained(this) to weak pointer

## Timeline

### yq...@gmail.com (2022-11-02)

This vulnerability is in the extension. I estimate that it only needs to install an extension to trigger it, and may not require interaction.

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-11-02)

Thanks for the report. Where possible, we strongly prefer proof of concepts to be provided in order to demonstrate that this is a security issue, which can be difficult to tell from the code.

This does look like a plausible sequence.

mamir@: Can you PTAL? We should avoid use of Unretained pointers in callbacks to KeyedServices in general, so this should be addressed.

Around assessing this as a security bug, is the PasswordsPrivate extension API accessible to installed extensions, or could this bug only be potentially triggered by WebUI?

[Monorail components: UI>Browser>Passwords UI>Settings]

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2022-11-04)

PasswordsPrivate extension API is *not* accessible to installed extensions.
Switching away from Unretained pointers SGTM

Over to Adem!


### de...@google.com (2022-11-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/90edd38ec8d1ffe6799ad21145b2c0f4afe05710

commit 90edd38ec8d1ffe6799ad21145b2c0f4afe05710
Author: Adem Derinel <derinel@google.com>
Date: Wed Nov 09 12:58:51 2022

Use weak pointer for win biometric authenticator.

This CL needs to update RecordAuthenticationResult because `WeakPtr`s
do not work with non-void return values.

Bug: 1380645
Change-Id: I9bee32cf70105b9cb07f0d1b5ff981763893a39b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4006758
Commit-Queue: Adem Derinel <derinel@google.com>
Reviewed-by: Viktor Semeniuk <vsemeniuk@google.com>
Cr-Commit-Position: refs/heads/main@{#1069102}

[modify] https://crrev.com/90edd38ec8d1ffe6799ad21145b2c0f4afe05710/chrome/browser/device_reauth/android/biometric_authenticator_android.cc
[modify] https://crrev.com/90edd38ec8d1ffe6799ad21145b2c0f4afe05710/chrome/browser/device_reauth/win/biometric_authenticator_win.cc
[modify] https://crrev.com/90edd38ec8d1ffe6799ad21145b2c0f4afe05710/chrome/browser/device_reauth/chrome_biometric_authenticator_common.cc
[modify] https://crrev.com/90edd38ec8d1ffe6799ad21145b2c0f4afe05710/chrome/browser/device_reauth/mac/biometric_authenticator_mac.h
[modify] https://crrev.com/90edd38ec8d1ffe6799ad21145b2c0f4afe05710/chrome/browser/device_reauth/chrome_biometric_authenticator_common.h
[modify] https://crrev.com/90edd38ec8d1ffe6799ad21145b2c0f4afe05710/chrome/browser/device_reauth/chrome_biometric_authenticator_common_unittest.cc
[modify] https://crrev.com/90edd38ec8d1ffe6799ad21145b2c0f4afe05710/chrome/browser/device_reauth/mac/biometric_authenticator_mac.mm
[modify] https://crrev.com/90edd38ec8d1ffe6799ad21145b2c0f4afe05710/chrome/browser/device_reauth/win/biometric_authenticator_win.h


### de...@google.com (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

Requesting merge to beta M108 because latest trunk commit (1069102) appears to be after beta branch point (1058933).

Not requesting merge to dev (M109) because latest trunk commit (1069102) appears to be prior to dev branch point (1070088). If this is incorrect, please replace the Merge-NA-109 label with Merge-Request-109. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-15)

Merge review required: M108 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### de...@google.com (2022-11-16)

1. Why does your merge fit within the merge criteria for these milestones?
- Security severity is medium
2. What changes specifically would you like to merge? Please link to Gerrit.
- https://crrev.com/c/4006758
3. Have the changes been released and tested on canary?
- The changes are already in canary
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No

### am...@chromium.org (2022-11-18)

M108 merge approved, please merge this fix to branch 5359 at your earliest convenience. Thank you! 

### am...@chromium.org (2022-11-21)

In my initial review of this issue for merge review, I missed https://crbug.com/chromium/1380645#c6; it appears that PasswordsPrivate extension API is *not* accessible to installed extensions and this may not be a security issue, making this fix a functional one and not requiring merge. 
Since this issue may be reachable via the webui only via user interaction, leaving as security issue and merge approval as-is. 
Please let me know derinel@ and mamir@ if there are any issues or concerns with this. 

### de...@google.com (2022-11-22)

You are right, this extension API is only accessible to WebUI. If there are no other concerns I'd rather not merge.

### [Deleted User] (2022-11-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-11-22)

amyressler@ is there urgency to include this in M108 recut?

### am...@chromium.org (2022-11-22)

yes, I'm realizing from https://crbug.com/chromium/1380645#c17 that my message in https://crbug.com/chromium/1380645#c16 may have been a bit convolutely articulated. 
If this bug was not reachable via WebUI, it would not be a security issue. 
Since it is and it would seemingly result in a browser process UAF via WebUI interactions, this is a medium severity bug and should be backmerged to M108, which will soon be promoted to stable (and stable RC is being recut today due to an emergency/Pri-0 fix). 

derinel@ unless there are stability or compatibility concerns with backmerging (and if so, please let me know), can you please backmerge this fix to 108/branch 5359 at soonest. Thank you. 

### de...@google.com (2022-11-23)

Even though I built it locally and tested some of the code paths, the merge is not straightforward to M108 and we have some concerns with backmerging.

Adding Ioana as the code owner for help.

### va...@chromium.org (2022-11-23)

BiometricAuthenticatorWin should not execute callbacks when it's destroyed. Thus, [4] should also use the weak ptr.

### de...@google.com (2022-11-23)

Reopening the bug as it it is not fully fixed. 

### sr...@google.com (2022-11-23)

Removing merge-approved label as it is not ready yet. please add merge-request once it is ready

### gi...@appspot.gserviceaccount.com (2022-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/44ff733979350646c3bfd52b7a4d7090758aab2d

commit 44ff733979350646c3bfd52b7a4d7090758aab2d
Author: Adem Derinel <derinel@google.com>
Date: Thu Nov 24 20:54:08 2022

Use weak pointer for the Authenticator in PasswordsPrivateDelegate

Bug: 1380645
Change-Id: I3a9527e56162924a89d605bb0f9068fe27d638ba
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4051191
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Adem Derinel <derinel@google.com>
Cr-Commit-Position: refs/heads/main@{#1075621}

[modify] https://crrev.com/44ff733979350646c3bfd52b7a4d7090758aab2d/components/password_manager/core/browser/password_access_authenticator.cc
[modify] https://crrev.com/44ff733979350646c3bfd52b7a4d7090758aab2d/chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl.cc
[modify] https://crrev.com/44ff733979350646c3bfd52b7a4d7090758aab2d/components/password_manager/core/browser/password_access_authenticator.h


### de...@google.com (2022-11-24)

Requesting merge for  https://chromium-review.googlesource.com/c/chromium/src/+/4051191

### [Deleted User] (2022-11-25)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-25)

Merge review required: M108 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/396aeea6701eb5b9dc213bdb079966479ec38b73

commit 396aeea6701eb5b9dc213bdb079966479ec38b73
Author: Adem Derinel <derinel@google.com>
Date: Mon Nov 28 09:55:50 2022

[Merge M109] Use weak pointer for the Authenticator in PasswordsPrivateDelegate

(cherry picked from commit 44ff733979350646c3bfd52b7a4d7090758aab2d)

Bug: 1380645
Change-Id: I3a9527e56162924a89d605bb0f9068fe27d638ba
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4051191
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Adem Derinel <derinel@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1075621}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4061226
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#245}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/396aeea6701eb5b9dc213bdb079966479ec38b73/components/password_manager/core/browser/password_access_authenticator.cc
[modify] https://crrev.com/396aeea6701eb5b9dc213bdb079966479ec38b73/chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl.cc
[modify] https://crrev.com/396aeea6701eb5b9dc213bdb079966479ec38b73/components/password_manager/core/browser/password_access_authenticator.h


### de...@google.com (2022-11-28)

Answers for https://crbug.com/chromium/1380645#c28:

1. Why does your merge fit within the merge criteria for these milestones?
- It is a medium severity security bug.
2. What changes specifically would you like to merge? Please link to Gerrit.
- https://chromium-review.googlesource.com/c/chromium/src/+/4051191
3. Have the changes been released and tested on canary?
Yes.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No.

### am...@chromium.org (2022-11-30)

Updating as fixed based on new CLs and merge request in https://crbug.com/chromium/1380645#c26

### am...@chromium.org (2022-11-30)

M108 merge approved, please merge the latest CL (https://ccrev.com/c/4051191) to M108/ branch 5359 at your earliest convenience.

### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4f2b6a7318b3f1e5696f2d56dc6575cc2a2068a0

commit 4f2b6a7318b3f1e5696f2d56dc6575cc2a2068a0
Author: Adem Derinel <derinel@google.com>
Date: Thu Dec 01 12:50:55 2022

[Merge M108] Use weak pointer for the Authenticator in PasswordsPrivateDelegate

(cherry picked from commit 44ff733979350646c3bfd52b7a4d7090758aab2d)

Bug: 1380645
Change-Id: I3a9527e56162924a89d605bb0f9068fe27d638ba
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4051191
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Adem Derinel <derinel@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1075621}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4066048
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1051}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/4f2b6a7318b3f1e5696f2d56dc6575cc2a2068a0/components/password_manager/core/browser/password_access_authenticator.cc
[modify] https://crrev.com/4f2b6a7318b3f1e5696f2d56dc6575cc2a2068a0/chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl.cc
[modify] https://crrev.com/4f2b6a7318b3f1e5696f2d56dc6575cc2a2068a0/components/password_manager/core/browser/password_access_authenticator.h


### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/751db273f09252f9862c541733677b1cab6f4234

commit 751db273f09252f9862c541733677b1cab6f4234
Author: Adem Derinel <derinel@google.com>
Date: Thu Dec 01 14:10:15 2022

Passwords: Add DCHECKs for PasswordAccessAuthenticator

PasswordAccessAuthenticator now requires `Init()` to be called. This CL
adds the required DCHECKs and removes the old constructor.

Bug: 1380645
Change-Id: I4f94a19ad7417f6827cf3eb6d38e6b02f6cab93d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4061235
Commit-Queue: Adem Derinel <derinel@google.com>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1078023}

[modify] https://crrev.com/751db273f09252f9862c541733677b1cab6f4234/components/password_manager/core/browser/password_access_authenticator.cc
[modify] https://crrev.com/751db273f09252f9862c541733677b1cab6f4234/components/password_manager/core/browser/password_access_authenticator_unittest.cc
[modify] https://crrev.com/751db273f09252f9862c541733677b1cab6f4234/components/password_manager/core/browser/password_access_authenticator.h


### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations! The VRP Panel has decided to award you $1,000 fro this report. There was no demonstration or evidence of exploitability or reachability with this issue, since that was mostly determined with engineering input and a fix was able to be landed, the reward amount is for appreciation of your report that allowed us to make a security relevant change. Given this issue is only reachable via the Web UI, it would be considered as mitigated so the reward amount also reflects that as well. Thank you for your efforts in reporting this issue to us. 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-12)

The CL adding the DCHECKs was landed after the merge of the original CL. The newest DCHECKs CL (https://ccrev.com/c/4061235) to M109/branch 5414 at your earliest convenience unless there are stability concerns with doing so.  
The last planned RC for M108 Stable channel release was already cut for respin release tomorrow. M108 will become Extended support when M109 is promoted to Stable on 3 January, so please also backmerge this fix to branch 5359 when you have a chance. 
This will not be considered as resolved in or listed in the security fixes for tomorrow's Stable M108 release given the pending CL merge. 

### pb...@google.com (2022-12-13)

Your merge has been approved for M109, please help complete your merges asap (before 2pm PST) today, so the change can be included in this week's RC build for beta releases.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M109 branch(go/chrome-branches).

### ma...@chromium.org (2022-12-13)

Thank you for your diligence.
The CL that adds the DCHECK https://crrev.com/c/4061235 doesn't contribute to the fix of the UAF issue. 
This is only a code cleanup CL and hence doesn't need to be merged back in M109 .



### [Deleted User] (2022-12-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### de...@google.com (2023-01-03)

Dropping Merge-Approved-108 and Merge-Approved-108 labels as the required CL (https://chromium-review.googlesource.com/c/chromium/src/+/4051191) is both merged to 108 (https://chromiumdash.appspot.com/commit/4f2b6a7318b3f1e5696f2d56dc6575cc2a2068a0) and 109 (https://chromiumdash.appspot.com/commit/396aeea6701eb5b9dc213bdb079966479ec38b73)

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1380645?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Passwords, UI>Settings]
[Monorail blocking: crbug.com/chromium/1342236]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061558)*
