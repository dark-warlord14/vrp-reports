# Security: UAF in ash::PrintServersProviderImpl::NotifyObservers

| Field | Value |
|-------|-------|
| **Issue ID** | [40060700](https://issues.chromium.org/issues/40060700) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Printing |
| **Platforms** | ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | bm...@chromium.org |
| **Created** | 2022-08-28 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

|PrintServersPolicyProvider::PrintServersPolicyProvider| will add[1] self as observer into user\_policy\_provider\_ and device\_policy\_provider\_, and the observer will not be removed even though the object of PrintServersPolicyProvider is freed. The lifetime of PrintServersPolicyProvider object is bound with its profile, but the device\_policy\_provider\_ is pointer of a member of PrintServersProviderFactory single instance. So, create an incognito window and then close will result in a dangling observer in device\_policy\_provider\_.

1. When |DevicePrintServersExternalDataHandler::OnDeviceExternalDataFetched| [2] is called, it will invoke |PrintServersProvider::SetData| [3]. In this function, the dangling observer will be used, the UAF is triggered.
2. |PrintServersExternalDataHandler::OnExternalDataFetched| [4] is the same behavior.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/printing/print_servers_policy_provider.cc;l=22-29;drc=47a6a146686804985940b83d79c4322fca4a0b7e>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/policy/external_data/handlers/device_print_servers_external_data_handler.cc;l=45-50;drc=2330c1533e39e4f8c195b0a2a05802ea9dee9c85;bpv=1;bpt=1>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/printing/print_servers_provider.cc;l=214-226;drc=2330c1533e39e4f8c195b0a2a05802ea9dee9c85;bpv=1;bpt=1>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/policy/external_data/handlers/print_servers_external_data_handler.cc;l=51-57;drc=2330c1533e39e4f8c195b0a2a05802ea9dee9c85>

Fix suggestion:

```
diff --git a/chrome/browser/ash/printing/print_servers_policy_provider.cc b/chrome/browser/ash/printing/print_servers_policy_provider.cc  
index f563edc597ba4..dc874f63e03e1 100644  
--- a/chrome/browser/ash/printing/print_servers_policy_provider.cc  
+++ b/chrome/browser/ash/printing/print_servers_policy_provider.cc  
@@ -28,7 +28,10 @@ PrintServersPolicyProvider::PrintServersPolicyProvider(  
   device_policy_provider_->AddObserver(this);  
 }  
  
-PrintServersPolicyProvider::~PrintServersPolicyProvider() = default;  
+PrintServersPolicyProvider::~PrintServersPolicyProvider() {  
+  device_policy_provider_->RemoveObserver(this);  
+  user_policy_provider_->RemoveObserver(this);  
+}  
  
 // static  
 std::unique_ptr<PrintServersPolicyProvider> PrintServersPolicyProvider::Create(  

```

\*\*VERSION\*\*

ASAN build of linux-chromeos

\*\*REPRODUCTION CASE\*\*

|DevicePrintServersExternalDataHandler::OnDeviceExternalDataFetched| or |PrintServersExternalDataHandler::OnExternalDataFetched| required the administrator of ChromeOS Enterprise to trigger in admin.google.com. Take a look at the comment in chrome/browser/ash/policy/external\_data/handlers/print\_servers\_external\_data\_handler.h and chrome/browser/ash/policy/external\_data/handlers/device\_print\_servers\_external\_data\_handler.h

Sorry for I didn’t setup a real PoC. However, I create a patch for process simulation.

In the patch I enable the chrome.autotestPrivate and modify refreshEnterprisePolicies function to call ash::PrintServersProviderFactory::Get()->GetForDevice()->SetData().

1. Apply patch and build
2. Run chromeos and login, create an incognito window and close it
3. Load the attached extension
4. UAF

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Chaobin Zhang

## Attachments

- patch.diff (text/plain, 7.8 KB)
- manifest.json (text/plain, 537 B)
- test.js (text/plain, 80 B)
- [asan.txt](attachments/asan.txt) (text/plain, 23.4 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 9.4 MB)

## Timeline

### [Deleted User] (2022-08-28)

[Empty comment from Monorail migration]

### al...@google.com (2022-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2022-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### bm...@chromium.org (2022-09-02)

Thanks for the detailed report.  The specific attack scenario here doesn't seem to be likely in real-world setups because it requires the admin to change external printer resources in coordination with the local attacker.  Nevertheless, I do agree that there's a dangling pointer that needs to be fixed.  I'll send a CL shortly.

### bm...@chromium.org (2022-09-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/de271e2507a16f62ad773f497f298455b41b57c7

commit de271e2507a16f62ad773f497f298455b41b57c7
Author: Benjamin Gordon <bmgordon@chromium.org>
Date: Fri Sep 02 18:08:19 2022

Clean up print policy provider observers on deletion

On creation, PrintServersPolicyProvider adds itself to the observers
lists for the supplied device PrintServersProvider and user
PrintServersProvider.  The lifetime of PrintServersPolicyProvider itself
is bound to the profile, so the device provider may still have
references to the object even after the profile is closed (e.g. an
incognito window).  Remove the observer references in the destructor to
make sure this can't happen.

Bug: 1357397
Change-Id: If4fbca359d6f1a5edbd98774dbb6588c79a2bf5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3869418
Reviewed-by: Piotr Pawliczek <pawliczek@chromium.org>
Commit-Queue: Benjamin Gordon <bmgordon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1042677}

[modify] https://crrev.com/de271e2507a16f62ad773f497f298455b41b57c7/chrome/browser/ash/printing/print_servers_policy_provider.cc


### bm...@chromium.org (2022-09-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>Printing]

### zh...@gmail.com (2022-09-03)

Thanks @bmgordon. I agree with your comment https://crbug.com/chromium/1357397#c6. In order to trigger the browser UAF, the attacker have to wait for the admin to change the external printer resources. 

### bm...@chromium.org (2022-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-06)

Merge review required: M106 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bm...@chromium.org (2022-09-06)

1. Yes: Fix for potential security issue.
2. crrev.com/c/3869418
3. Yes.
4. No.
5. N/A
6. N/A


### ce...@google.com (2022-09-07)

Merge approved for M106.

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3a456098cf93eff4a17b5d1fe5b1d2ab21560bcd

commit 3a456098cf93eff4a17b5d1fe5b1d2ab21560bcd
Author: Benjamin Gordon <bmgordon@chromium.org>
Date: Thu Sep 08 17:53:04 2022

Clean up print policy provider observers on deletion

On creation, PrintServersPolicyProvider adds itself to the observers
lists for the supplied device PrintServersProvider and user
PrintServersProvider.  The lifetime of PrintServersPolicyProvider itself
is bound to the profile, so the device provider may still have
references to the object even after the profile is closed (e.g. an
incognito window).  Remove the observer references in the destructor to
make sure this can't happen.

(cherry picked from commit de271e2507a16f62ad773f497f298455b41b57c7)

Bug: 1357397
Change-Id: If4fbca359d6f1a5edbd98774dbb6588c79a2bf5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3869418
Reviewed-by: Piotr Pawliczek <pawliczek@chromium.org>
Commit-Queue: Benjamin Gordon <bmgordon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1042677}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3877378
Auto-Submit: Benjamin Gordon <bmgordon@chromium.org>
Commit-Queue: Piotr Pawliczek <pawliczek@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#355}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/3a456098cf93eff4a17b5d1fe5b1d2ab21560bcd/chrome/browser/ash/printing/print_servers_policy_provider.cc


### [Deleted User] (2022-09-08)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bm...@chromium.org (2022-09-08)

1. No.
2. No.

### rz...@google.com (2022-09-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-09-09)

1. Just https://crrev.com/c/3883923
2. Low, no conflicts
3. 106
4. Yes

### rz...@google.com (2022-09-09)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### ch...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@gmail.com (2022-10-01)

Will this issue get a CVE identifier? This bug is NOT a regression AFAIK, and chrome 106 had released according to https://chromiumdash.appspot.com/schedule.




### zh...@gmail.com (2022-10-12)

@amyressler, sorry for disturb.

Could you please do me a favor? I think it should get a CVE identifier and list in: https://chromereleases.googleblog.com/2022/10/stable-channel-update-for-chromeos.html but it was missing out. Thanks in advance.

### am...@chromium.org (2022-10-12)

Hi zhchbin@, at the time this issue was reported, this issue did not appear to impact stable according to the FoundIn-106 label applied in August. As this issue does not appear to impact Stable/Extended Stable based on FoundIn-106 and reporting data, it would not have been eligible for a CVE nor to included in the Stable release notes. 

+ chmiel@ from Chrome OS for confirmation / updating as this is a ash issue impacting Chrome OS 

### zh...@gmail.com (2022-10-13)

[Comment Deleted]

### zh...@gmail.com (2022-10-13)

Hi amyressler@, thanks. 

I should have reported the impact version correctly. After double check the code history, https://source.chromium.org/chromium/chromium/src/+/6f9b377c07083cc3f7d3d8870b8dacdbd607bbd1 , I think this issue maybe exist since 2020-10-30 and it did impact the stable version, and there are also labels: LTS-Merge-Review-102 and LTS-Merge-Delayed-102 can help us figure out whether stable version was effected when I reported  in August.

FYI chmiel@

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations, Chaobin Zhang! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-18)

Removing LTS labels.

### [Deleted User] (2022-10-18)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-10-28)

Not Applicable for LTS merge per new merge guidelines.

### [Deleted User] (2022-12-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1357397?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060700)*
