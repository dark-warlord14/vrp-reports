# Security: Use-after-Free in InstallUpdateCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40059589](https://issues.chromium.org/issues/40059589) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | db...@chromium.org |
| **Created** | 2022-05-07 |
| **Bounty** | $1,000.00 |

## Description


Chrome version: 101.0.4951

[0] The `browser_context_` is posted to a separate sequence in function `UpdateDataProvider::RunInstallCallback`

https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/updater/update_data_provider.cc;drc=06b7fdb48dea3de43ab2b3fc996bdc3e09abbd9a;l=144
```
void UpdateDataProvider::RunInstallCallback(
    const std::string& extension_id,
    const std::string& public_key,
    const base::FilePath& unpacked_dir,
    bool install_immediately,
    UpdateClientCallback update_client_callback) {
  VLOG(3) << "UpdateDataProvider::RunInstallCallback " << extension_id << " "
          << public_key;

  if (!browser_context_) {
    base::ThreadPool::PostTask(
        FROM_HERE, {base::TaskPriority::BEST_EFFORT, base::MayBlock()},
        base::GetDeletePathRecursivelyCallback(unpacked_dir));
    content::GetUIThreadTaskRunner({})->PostTask(
        FROM_HERE,
        base::BindOnce(std::move(update_client_callback),
                       update_client::CrxInstaller::Result(
                           update_client::InstallError::GENERIC_ERROR)));
    return;
  }

  content::GetUIThreadTaskRunner({})->PostTask(
      FROM_HERE,
      base::BindOnce(InstallUpdateCallback, browser_context_, extension_id,		// `browser_context_` can be freed before task is runned
                     public_key, unpacked_dir, install_immediately,
                     std::move(update_client_callback)));
}
```


[1] `browser_context_` may be destroyed in UI by the time the it runs, causing a UAF in InstallUpdateCallback callback.

https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/updater/update_data_provider.cc;drc=3810f9d8c604ed06d6c14df979e940eabcc8c897;l=38
```
void InstallUpdateCallback(content::BrowserContext* context,
                           const std::string& extension_id,
                           const std::string& public_key,
                           const base::FilePath& unpacked_dir,
                           bool install_immediately,
                           UpdateClientCallback update_client_callback) {
  // Note that error codes are converted into custom error codes, which are all
  // based on a constant (see ToInstallerResult). This means that custom codes
  // from different embedders may collide. However, for any given extension ID,
  // there should be only one embedder, so this should be OK from Omaha.
  ExtensionSystem::Get(context)->InstallUpdate(
      extension_id, public_key, unpacked_dir, install_immediately,
      base::BindOnce(
          [](UpdateClientCallback callback,
             const absl::optional<CrxInstallError>& error) {
            DCHECK_CURRENTLY_ON(content::BrowserThread::UI);
            update_client::CrxInstaller::Result result(0);
            if (error.has_value()) {
              int detail =
                  error->type() ==
                          CrxInstallErrorType::SANDBOXED_UNPACKER_FAILURE
                      ? static_cast<int>(error->sandbox_failure_detail())
                      : static_cast<int>(error->detail());
              result = update_client::ToInstallerResult(error->type(), detail);
            }
            std::move(callback).Run(result);
          },
          std::move(update_client_callback)));
}
```

[2] To trigger this vulnerability, we can use developerPrivate.autoUpdate function, which can be used from the chrome extension. The path leads to buggy function `UpdateDataProvider::RunInstallCallback` is

UpdateDataProvider::RunInstallCallback
 UpdateDataProvider::GetData
  UpdateService::StartUpdateCheck
   ExtensionUpdater::CheckNow
    DeveloperPrivateAutoUpdateFunction::Run


[3] In addition, due to conditional competition with the UI thread. The browser_context_ used by InstallUpdateCallback is destructed first in UI, so it's maybe hard to trigger the crash. I am working on trying to build a poc. 

I don't have a poc, just code inspection. I'll upload poc as soon as i can trigger crash.



## Timeline

### [Deleted User] (2022-05-07)

[Empty comment from Monorail migration]

### me...@google.com (2022-05-09)

Thanks for the report. developerPrivate can't be used by other extensions, but I wonder if requestUpdateCheck() can be used for the same purpose. Assigning high severity because this requires an extension install, but a PoC would also be great.

lazyboy: Could you triage this bug? Thank you.

[Monorail components: Platform>Extensions]

### [Deleted User] (2022-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-21)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ma...@google.com (2022-05-31)

(Pinged extensions team offline for triage.)


### ma...@google.com (2022-06-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2022-06-03)

I didn't pay much attention for lack of PoC, here's my thought:

We can add "is valid browser context" check and bail out if it isn't, like we do here: https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/runtime/runtime_api.cc;drc=8d6a246c9be4f6b731dc7f6e680b7d5e13a512b5;l=116

TL/DR;
void InstallUpdateCallback(content::BrowserContext* context,
   ...) {
  if (!ExtensionsBrowserClient::Get()->IsValidContext(browser_context))
    return;
  ...
}

### db...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

### sr...@google.com (2022-06-15)

Hi, security marshal here.

@dbertoni, have you started looking at this issue? Can we ship the proposed fix from https://crbug.com/chromium/1323449#c10 maybe?

@huyna89: did you make some progress building a repro for this bug?

### db...@chromium.org (2022-06-15)

I have a fix for this:

https://chromium-review.googlesource.com/c/chromium/src/+/3688185

However, it's stuck behind figuring out how to write unit tests to verify it. That's somewhat complicated because of multiple layers of tasks that are posted. I suppose I could commit the fix now and add tests later, but isn't ideal.

The fix proposed in https://crbug.com/chromium/1323449#c10 is incomplete, because other pointers can become invalidated when the BrowserContext is deleted.

I suspect this will be very difficult to trigger in the real world, but it would be great to have a test case that can reproduce it deterministically.

### [Deleted User] (2022-06-30)

dbertoni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2dbb348fdb87962bcb7ad11e59449d4a32d32be7

commit 2dbb348fdb87962bcb7ad11e59449d4a32d32be7
Author: David Bertoni <dbertoni@chromium.org>
Date: Thu Jun 30 17:32:48 2022

[Extensions] Fix potential UAF in UpdateDataProvider.

UpdateDataProvider post a task that can be run after its BrowserContext is destroyed, leading to user-after-free. This CL instead binds the UpdateDataProvider instance to the callback and uses a member function instead of a static function. This ensures the the UpdateDataProvider instance will be alive when the callback is executed.

Bug: 1323449
Change-Id: If617676d2e0e6a31a7936d88c75dd221c69b1057
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688185
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: David Bertoni <dbertoni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1019720}

[modify] https://crrev.com/2dbb348fdb87962bcb7ad11e59449d4a32d32be7/extensions/browser/updater/update_data_provider.cc
[modify] https://crrev.com/2dbb348fdb87962bcb7ad11e59449d4a32d32be7/extensions/browser/updater/update_data_provider.h


### db...@chromium.org (2022-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-30)

Requesting merge to extended stable M102 because latest trunk commit (1019720) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1019720) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1019720) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-01)

Merge review required: M104 is already shipping to beta.

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

### [Deleted User] (2022-07-01)

Merge review required: M103 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-01)

Merge review required: M102 is already shipping to stable.

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

### am...@google.com (2022-07-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-06)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. The reward amount was decided upon based on this issue not having a POC, stack trace, or other artifacts to demonstrate this issue; additionally, this issue is mitigated by an extension, and actual exploitation potential appears to be theoretical to low due to the race with the UI thread. 
If you can produce a POC or other demonstration of this issue, we would be happy to revisit for a reassessment for a potential change in reward amount. 
Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

Based on our assessment above and also there being two severity labels, removing the high severity label to set this at medium. 

### am...@chromium.org (2022-07-08)

Given the above severity assessment + the size of this fix, approving for merge to M104; please merge this fix to branch 5112 at your earliest convenience. 
Suggesting we not merge this back to ES/102 and Stable/103 which are currently shipping as such and this fix can ship in 104/Stable milestone release. Please let me know if there are any issues/concerns with this assessment or plan. 

### sr...@google.com (2022-07-12)

This CL is approved for Merge to M104, Please help complete all merges before 3pm PST today ( July 12) so that these can be included in this week's beta release going out tomorrow,. I will be cutting RC build today at 3pm PST

### sr...@google.com (2022-07-22)

This bug is approved for merge to M104, Stable RC cut is next tuesday around 2pm PST, so please help get all the merges complete asap so they can be included in the RC build.

### sr...@google.com (2022-07-22)

Looks like the merge is completed here - https://chromium-review.googlesource.com/c/chromium/src/+/3774733

Dropping the merge-approved label

### [Deleted User] (2022-07-25)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-27)

1. https://crrev.com/c/3787841
2. Low, just an include conflict and conflicting PostTask calls
3. 104
4. Yes

### gm...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-10)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-11)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/64e1b8564bd967d652531df287b58277f550d206

commit 64e1b8564bd967d652531df287b58277f550d206
Author: David Bertoni <dbertoni@chromium.org>
Date: Fri Aug 12 14:11:03 2022

[M96-LTS][Extensions] Fix potential UAF in UpdateDataProvider.

M96 merge issues:
  extensions/browser/updater/update_data_provider.h:
    conflicting types for browser_context_
  extensions/browser/updater/update_data_provider.cc:
    Conflict in calls in deleted code:
      main uses base::GetDeletePathRecursivelyCallback(unpacked_dir) as
      3rd argument of PostTask, M96 uses:
      base::BindOnce(base::GetDeletePathRecursivelyCallback(), unpacked_dir)

UpdateDataProvider post a task that can be run after its BrowserContext is destroyed, leading to user-after-free. This CL instead binds the UpdateDataProvider instance to the callback and uses a member function instead of a static function. This ensures the the UpdateDataProvider instance will be alive when the callback is executed.

(cherry picked from commit 2dbb348fdb87962bcb7ad11e59449d4a32d32be7)

Bug: 1323449
Change-Id: If617676d2e0e6a31a7936d88c75dd221c69b1057
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688185
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: David Bertoni <dbertoni@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1019720}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3787841
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1678}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/64e1b8564bd967d652531df287b58277f550d206/extensions/browser/updater/update_data_provider.cc
[modify] https://crrev.com/64e1b8564bd967d652531df287b58277f550d206/extensions/browser/updater/update_data_provider.h


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-12)

1. Just https://crrev.com/c/3822902
2. Low, only conflicts with datatypes in the deleted code
3. 104
4. Yes

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6c1ee1e6d7ef6146cd536a850b4e1f47d72b52bf

commit 6c1ee1e6d7ef6146cd536a850b4e1f47d72b52bf
Author: David Bertoni <dbertoni@chromium.org>
Date: Thu Aug 18 10:11:30 2022

[M102-LTS][Extensions] Fix potential UAF in UpdateDataProvider.

M102 merge issues:
  extensions/browser/updater/update_data_provider.cc:
    Conflicts in deleted code in RunInstallCallback after the browser_context_ check, kept the version from the CL.

UpdateDataProvider post a task that can be run after its BrowserContext is destroyed, leading to user-after-free. This CL instead binds the UpdateDataProvider instance to the callback and uses a member function instead of a static function. This ensures the the UpdateDataProvider instance will be alive when the callback is executed.

(cherry picked from commit 2dbb348fdb87962bcb7ad11e59449d4a32d32be7)

Bug: 1323449
Change-Id: If617676d2e0e6a31a7936d88c75dd221c69b1057
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688185
Commit-Queue: David Bertoni <dbertoni@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1019720}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3822902
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1312}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/6c1ee1e6d7ef6146cd536a850b4e1f47d72b52bf/extensions/browser/updater/update_data_provider.cc
[modify] https://crrev.com/6c1ee1e6d7ef6146cd536a850b4e1f47d72b52bf/extensions/browser/updater/update_data_provider.h


### rz...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1323449?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059589)*
