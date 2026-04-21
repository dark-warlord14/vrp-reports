# Security: UAF in chromeos::multidevice::MultidevicePhoneHubHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40060039](https://issues.chromium.org/issues/40060039) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | ju...@google.com |
| **Created** | 2022-06-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in chromeos::multidevice::MultidevicePhoneHubHandler

**VERSION**  

Chrome Version: [stable, beta, or dev]  

Operating System: Chrome

**REPRODUCTION CASE**

1. Download asan-linux-release-1015312 in <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release-chromeos%2Fasan-linux-release-1015312.zip?generation=1655469268278292&alt=media>
2. run: linux-release-chromeos\_asan-linux-release-1015312/asan-linux-release-1015312/chrome-wrapper --use-system-clipboard --user-data-dir=./chromeos\_vm1

browsing `chrome://multidevice-internals/` and open devtools, execute js in console.

```
chrome.send("setFakePhoneHubManagerEnabled", [true]);  
chrome.send("setFakePhoneHubManagerEnabled", [true]);  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Nan Wang(@eternalsakura13) and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 3.5 MB)
- [asan.txt](attachments/asan.txt) (text/plain, 21.5 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 900 B)

## Timeline

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-06-22)

If we have a uxss to inject js into the webui, combining this vulnerability may achieve RCE :)

### et...@gmail.com (2022-06-22)

[Comment Deleted]

### et...@gmail.com (2022-06-22)

## Root Cause
[0] When we call `chrome.send("setFakePhoneHubManagerEnabled", [true]);` twice, this will call EnableFakePhoneHubManager twice, thus initializing fake_phone_hub_manager_ twice, causing the old fake_phone_hub_manager_ created for the first time to be freed.

[1] But the raw ptr of old fake_phone_hub_manager_ is saved in phone_hub_manager_ of PhoneHubUiController

[2] This will cause the raw ptr of old fake_phone_hub_manager_ to be used again in CleanUpPhoneHubManager, which will trigger UAF.

```
void MultidevicePhoneHubHandler::EnableFakePhoneHubManager() {
  DCHECK(!fake_phone_hub_manager_);
  PA_LOG(VERBOSE) << "Setting fake Phone Hub Manager";
  fake_phone_hub_manager_ = std::make_unique<phonehub::FakePhoneHubManager>(); //--->[0]
  ash::SystemTray::Get()->SetPhoneHubManager(fake_phone_hub_manager_.get()); // ---->[1]
  AddObservers();
}
```

```
void PhoneHubUiController::SetPhoneHubManager(
    phonehub::PhoneHubManager* phone_hub_manager) {
  if (phone_hub_manager == phone_hub_manager_)
    return;

  CleanUpPhoneHubManager();

  phone_hub_manager_ = phone_hub_manager;  // ---->[1]
  if (phone_hub_manager_) {
    phone_hub_manager_->GetFeatureStatusProvider()->AddObserver(this);
    phone_hub_manager_->GetOnboardingUiTracker()->AddObserver(this);
    phone_hub_manager_->GetPhoneModel()->AddObserver(this);
  }

  UpdateUiState(GetUiStateFromPhoneHubManager());
}
```

```
void PhoneHubUiController::CleanUpPhoneHubManager() {
  if (!phone_hub_manager_)
    return;

  phone_hub_manager_->GetFeatureStatusProvider()->RemoveObserver(this); //---->[2]
  phone_hub_manager_->GetOnboardingUiTracker()->RemoveObserver(this);
  phone_hub_manager_->GetPhoneModel()->RemoveObserver(this);
}
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/chromeos/multidevice_internals/multidevice_internals_phone_hub_handler.cc;l=360;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4
[1] https://source.chromium.org/chromium/chromium/src/+/main:ash/system/phonehub/phone_hub_ui_controller.cc;l=92;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4
[2] https://source.chromium.org/chromium/chromium/src/+/main:ash/system/phonehub/phone_hub_ui_controller.cc;l=337;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4

## Patch
The patch for this vulnerability is trivial, just convert DCHECK to CHECK
```
 void MultidevicePhoneHubHandler::EnableFakePhoneHubManager() {
-  DCHECK(!fake_phone_hub_manager_);
+  CHECK(!fake_phone_hub_manager_);
   PA_LOG(VERBOSE) << "Setting fake Phone Hub Manager";
   fake_phone_hub_manager_ = std::make_unique<phonehub::FakePhoneHubManager>();
   ash::SystemTray::Get()->SetPhoneHubManager(fake_phone_hub_manager_.get());
```

### aj...@google.com (2022-06-22)

Thanks for the report - sending to ChromeOS for triage.

### lz...@google.com (2022-06-28)

I will let PhoneHub team triage.

### al...@google.com (2022-06-28)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell]

### al...@google.com (2022-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-29)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-07-01)

I think the fix for this bug is simple and have attached a patch, can anyone help with this ：）

### [Deleted User] (2022-07-06)

jessejames: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2022-07-08)

I don't think Jesse (a senior PM) is a good owner here. Assigning to the person who wrote the code.

### jo...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-07-08)

Hsu will be back on Monday.

### kh...@chromium.org (2022-07-11)

hsuregan@ no longer works on Phone Hub; reassigning to jonmann@ and CC'ing a few others who have touched Phone Hub recently.

### [Deleted User] (2022-07-20)

jonmann: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2022-07-20)

Hey Juliet, is there any chance you might have the bandwidth to look into this one?

### ju...@google.com (2022-07-22)

Yep, I have time to address this UAF concern in the second half of next week and verify the fix. 

### gi...@appspot.gserviceaccount.com (2022-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cc950421ca931991f0d39cdc0cabe9c6f2e6e4a3

commit cc950421ca931991f0d39cdc0cabe9c6f2e6e4a3
Author: Juliet Levesque <julietlevesque@google.com>
Date: Wed Jul 27 20:35:23 2022

[Phone Hub] Prevent UAF in chrome://multidevice-internals

Prevents the fakePhoneHubManager from being created twice UAF security
vulnerability by returning early if its already been set.

even if UAF is attempted

Test: Verified on DUT that the fakePhoneHubManager is only created once
Change-Id: Id347e4e17977269be33314e6d90e25533ea646c0
Fixed: 1338412
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788228
Reviewed-by: Jon Mann <jonmann@chromium.org>
Commit-Queue: Juliet Lévesque <julietlevesque@google.com>
Cr-Commit-Position: refs/heads/main@{#1028889}

[modify] https://crrev.com/cc950421ca931991f0d39cdc0cabe9c6f2e6e4a3/chrome/browser/ui/webui/chromeos/multidevice_internals/multidevice_internals_phone_hub_handler.cc


### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

Requesting merge to beta M104 because latest trunk commit (1028889) appears to be after beta branch point (1012729).

Requesting merge to dev M105 because latest trunk commit (1028889) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-28)

Merge review required: M105 is already shipping to stable.

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

### [Deleted User] (2022-07-28)

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

### ma...@google.com (2022-07-29)

Please answer the merge survey above to begin review

### ju...@google.com (2022-07-29)

1. Why does your merge fit within the merge criteria for these milestones? yes, Security fix
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
crrev/c/3788228
3. Have the changes been released and tested on canary? no
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels? no
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents no
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing. no

### ma...@google.com (2022-07-29)

Approved, M104 and M105

### rs...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1800742b0166f9ad1416f0ee86198810138d5aec

commit 1800742b0166f9ad1416f0ee86198810138d5aec
Author: Juliet Levesque <julietlevesque@google.com>
Date: Wed Aug 03 20:49:22 2022

[Phone Hub] Prevent UAF in chrome://multidevice-internals

Prevents the fakePhoneHubManager from being created twice UAF security
vulnerability by returning early if its already been set.

even if UAF is attempted

(cherry picked from commit cc950421ca931991f0d39cdc0cabe9c6f2e6e4a3)

Test: Verified on DUT that the fakePhoneHubManager is only created once
Change-Id: Id347e4e17977269be33314e6d90e25533ea646c0
Fixed: 1338412
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788228
Reviewed-by: Jon Mann <jonmann@chromium.org>
Commit-Queue: Juliet Lévesque <julietlevesque@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1028889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3806147
Cr-Commit-Position: refs/branch-heads/5112@{#1382}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/1800742b0166f9ad1416f0ee86198810138d5aec/chrome/browser/ui/webui/chromeos/multidevice_internals/multidevice_internals_phone_hub_handler.cc


### [Deleted User] (2022-08-03)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08b5eaecf33165cda178517fa4ba070d1f598e16

commit 08b5eaecf33165cda178517fa4ba070d1f598e16
Author: Juliet Levesque <julietlevesque@google.com>
Date: Wed Aug 03 20:57:30 2022

[Phone Hub] Prevent UAF in chrome://multidevice-internals

Prevents the fakePhoneHubManager from being created twice UAF security
vulnerability by returning early if its already been set.

even if UAF is attempted

(cherry picked from commit cc950421ca931991f0d39cdc0cabe9c6f2e6e4a3)

Test: Verified on DUT that the fakePhoneHubManager is only created once
Change-Id: Id347e4e17977269be33314e6d90e25533ea646c0
Fixed: 1338412
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788228
Reviewed-by: Jon Mann <jonmann@chromium.org>
Commit-Queue: Juliet Lévesque <julietlevesque@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1028889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3806035
Cr-Commit-Position: refs/branch-heads/5195@{#192}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/08b5eaecf33165cda178517fa4ba070d1f598e16/chrome/browser/ui/webui/chromeos/multidevice_internals/multidevice_internals_phone_hub_handler.cc


### rz...@google.com (2022-08-04)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-04)

1. Just https://crrev.com/c/3810451
2. Low, no conflicts
3. 104, 105
4. Yes

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-04)

Congratulations Nan Wang! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided upon based on this issue being significantly mitigated by not being remote exploitable and requiring user interaction and accessing dev tools. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-09)

1. Just https://crrev.com/c/3816811
2. Low, no conflicts
3. 104, 105
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-08-17)

re https://crbug.com/chromium/1338412#c48:
https://chromereleases.googleblog.com/2022/08/stable-channel-update-for-desktop_16.html
Hi, I noticed that the credit on the chromerelease is inconsistent with what I wrote in the issue :)

Can I modify my credit from `Nan Wang(@eternalsakura13) and Guang Gong of 360 Alpha Lab` to `Nan Wang(@eternalsakura13) and Guang Gong of 360 Vulnerability Research Institute`? Thanks


### gm...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b16ae025e31795cff0444d1a28fa35ca73fe02cf

commit b16ae025e31795cff0444d1a28fa35ca73fe02cf
Author: Juliet Levesque <julietlevesque@google.com>
Date: Fri Aug 19 09:24:19 2022

[M102-LTS][Phone Hub] Prevent UAF in chrome://multidevice-internals

Prevents the fakePhoneHubManager from being created twice UAF security
vulnerability by returning early if its already been set.

even if UAF is attempted

(cherry picked from commit cc950421ca931991f0d39cdc0cabe9c6f2e6e4a3)

Test: Verified on DUT that the fakePhoneHubManager is only created once
Change-Id: Id347e4e17977269be33314e6d90e25533ea646c0
Fixed: 1338412
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788228
Commit-Queue: Juliet Lévesque <julietlevesque@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1028889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3816811
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1316}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/b16ae025e31795cff0444d1a28fa35ca73fe02cf/chrome/browser/ui/webui/chromeos/multidevice_internals/multidevice_internals_phone_hub_handler.cc


### gi...@appspot.gserviceaccount.com (2022-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e3a9b56f808e92147831992d24544ab1ecd07876

commit e3a9b56f808e92147831992d24544ab1ecd07876
Author: Juliet Levesque <julietlevesque@google.com>
Date: Fri Aug 19 11:09:22 2022

[M96-LTS][Phone Hub] Prevent UAF in chrome://multidevice-internals

Prevents the fakePhoneHubManager from being created twice UAF security
vulnerability by returning early if its already been set.

even if UAF is attempted

(cherry picked from commit cc950421ca931991f0d39cdc0cabe9c6f2e6e4a3)

Test: Verified on DUT that the fakePhoneHubManager is only created once
Change-Id: Id347e4e17977269be33314e6d90e25533ea646c0
Fixed: 1338412
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788228
Commit-Queue: Juliet Lévesque <julietlevesque@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1028889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3810451
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1690}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/e3a9b56f808e92147831992d24544ab1ecd07876/chrome/browser/ui/webui/chromeos/multidevice_internals/multidevice_internals_phone_hub_handler.cc


### rz...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

fix was already released in Release-1-M104 

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1338412?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060039)*
