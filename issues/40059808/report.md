# Security: UAF in ManagedConfigurationAPI::GetConfigurationOnBackend

| Field | Value |
|-------|-------|
| **Issue ID** | [40059808](https://issues.chromium.org/issues/40059808) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Managed, Enterprise |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | bf...@chromium.org |
| **Created** | 2022-05-31 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

The pattern of this vulnerability is similar to this issue.  

<https://chromium-review.googlesource.com/c/chromium/src/+/3651398>

1. apply patch.diff and build

[0] Since GetOriginPolicyConfiguration will check origin, this requires chrome enterprise version  

(<https://chromeenterprise.google/policies/?policy=ManagedConfigurationPerOrigin>)  

So I patched it to reach the vulnerable code.

```
void ManagedConfigurationAPI::GetOriginPolicyConfiguration(  
    const url::Origin& origin,  
    const std::vector<std::string>& keys,  
    base::OnceCallback<void(std::unique_ptr<base::DictionaryValue>)> callback) {  
  - if (!CanHaveManagedStore(origin)) {  
  -   return std::move(callback).Run(nullptr);  
  - }  
  backend_task_runner_->PostTaskAndReplyWithResult(  
      FROM_HERE,  
      base::BindOnce(&ManagedConfigurationAPI::GetConfigurationOnBackend,  
                     base::Unretained(this), origin, keys),  
      std::move(callback));  
}  

```

[1] Also add sleep here to simulate block

```
std::unique_ptr<base::DictionaryValue>  
ManagedConfigurationAPI::GetConfigurationOnBackend(  
    const url::Origin& origin,  
    const std::vector<std::string>& keys) {  
  // If there was no policy set for this origin, there is no reason to create  
  // or load a store.  
  - if (!base::Contains(store_map_, origin))  
  -   return nullptr;  
  + sleep(1);  
  value_store::LeveldbValueStore::ReadResult result =  
      store_map_[origin]->Get(keys);  
  if (!result.status().ok())  
    return nullptr;  
  
  auto dict = std::make_unique<base::DictionaryValue>();  
  dict->Swap(&result.settings());  
  return dict;  
}  

```

2. Run: out/release/chrome --user-data-dir=/tmp/xxx <http://127.0.0.1:8000/test.html>

**Problem Description:**  

[0] ManagedConfigurationAPI derived from KeyedSerive, and will be release after the browser closed.

[1] backend\_task\_runner\_ is a ThreadPool::SequencedTaskRunner, callbacks posted to it will run on a separate physical thread.

[2] The base::Unretained(this) is posted to backend\_task\_runner\_(a separate sequence)

[3] ManagedConfigurationAPI \*\*\*\*may be destroyed on the UI thread while GetConfigurationBackend is executing，because base::Contains(store map, origin)) will search the map, or due to cpu thread scheduling and other reasons.

[4] Since ManagedConfigurationAPI has been released at this time, accessing store\_map\_ will trigger UAF.

```
class ManagedConfigurationAPI : public KeyedService{ // [0]  
...  
ManagedConfigurationAPI::ManagedConfigurationAPI(Profile\* profile)  
    : profile_(profile),  
      stores_path_(  
          profile->GetPath().AppendASCII(kManagedConfigurationDirectoryName)),  
      backend_task_runner_(base::ThreadPool::CreateSequencedTaskRunner( //[1]  
          {base::MayBlock(), base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN})) {  
 ...  
}  
  
void ManagedConfigurationAPI::GetOriginPolicyConfiguration(  
    const url::Origin& origin,  
    const std::vector<std::string>& keys,  
    base::OnceCallback<void(std::unique_ptr<base::DictionaryValue>)> callback) {  
  if (!CanHaveManagedStore(origin)) {  
    return std::move(callback).Run(nullptr);  
  }  
  backend_task_runner_->PostTaskAndReplyWithResult(  
      FROM_HERE,  
      base::BindOnce(&ManagedConfigurationAPI::GetConfigurationOnBackend,  
                     base::Unretained(this), origin, keys), //[2]  
      std::move(callback));  
}  
  
std::unique_ptr<base::DictionaryValue>  
ManagedConfigurationAPI::GetConfigurationOnBackend(  
    const url::Origin& origin,  
    const std::vector<std::string>& keys) {  
  // If there was no policy set for this origin, there is no reason to create  
  // or load a store.  
  if (!base::Contains(store_map_, origin)) //[3]  
    return nullptr;  
  
  value_store::LeveldbValueStore::ReadResult result =  
      store_map_[origin]->Get(keys); //[4]  
  if (!result.status().ok())  
    return nullptr;  
  
  auto dict = std::make_unique<base::DictionaryValue>();  
  dict->Swap(&result.settings());  
  return dict;  
}  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/device_api/managed_configuration_api.h;drc=8d6a246c9be4f6b731dc7f6e680b7d5e13a512b5;bpv=1;bpt=1;l=28>  

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/device_api/managed_configuration_api.cc;l=119;drc=8d6a246c9be4f6b731dc7f6e680b7d5e13a512b5;bpv=1;bpt=1>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/device_api/managed_configuration_api.cc;l=150;drc=8d6a246c9be4f6b731dc7f6e680b7d5e13a512b5;bpv=1;bpt=1>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/device_api/managed_configuration_api.cc;l=239;drc=8d6a246c9be4f6b731dc7f6e680b7d5e13a512b5;bpv=1;bpt=1>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/device_api/managed_configuration_api.cc;l=243;drc=8d6a246c9be4f6b731dc7f6e680b7d5e13a512b5;bpv=1;bpt=1>

**Additional Comments:**  

The same vulnerability exists in ManagedConfigurationAPI::PostStoreConfiguration and should be fixed together.

\*\*Chrome version: \*\* \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- test.html (text/plain, 182 B)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 2.6 MB)
- [asan.log](attachments/asan.log) (text/plain, 27.1 KB)
- [repro_bug.diff](attachments/repro_bug.diff) (text/plain, 2.4 KB)

## Timeline

### et...@gmail.com (2022-05-31)

Attach a patch to help reproduce the vulnerability


### et...@gmail.com (2022-06-02)

I think this bug existed when this feature was introduced.
Please see this commit: 
https://source.chromium.org/chromium/chromium/src/+/2b4a3bc20e84e652b09b39661706dc97046260af

In addition, this comment may be one of the reasons why this vulnerability has not been discovered for a long time.
```
void ManagedConfigurationAPI::PostStoreConfiguration(
    const url::Origin& origin,
    base::DictionaryValue configuration) {
  // Safe to use unretained here, since we own the task runner. //-----> error
  backend_task_runner_->PostTask(
      FROM_HERE,
      base::BindOnce(&ManagedConfigurationAPI::StoreConfigurationOnBackend,
                     base::Unretained(this), origin, std::move(configuration)));
}
```

And according to this commit, I see that I may have misunderstood this feature, it's widely available for all web apps from March 2021, not just force-installed apps :)
https://source.chromium.org/chromium/chromium/src/+/dbe8904a70924bbaa9e0f0816b25135d00868ba1

### am...@chromium.org (2022-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-02)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-06-06)

Is anyone working on fixing this bug? thanks

### ct...@chromium.org (2022-06-06)

Sorry for the delay on triaging your report -- we'll work on reproducing and assigning this today.

### et...@gmail.com (2022-06-07)

Thanks for your reply, please let me know if you have any problems with the reproduce :)

### ct...@chromium.org (2022-06-07)

Setting up a custom ASAN build with the included patch, I am able to reproduce this. Thank you for the patch and the detailed analysis.

Assigning to chrome/browser/device_api/OWNERS: bfranz@ could you PTAL? Thanks!

CC'ing some folks from crrev.com/c/2577679 (per analysis at https://crbug.com/chromium/1330489#c2) for visibility.

Setting some initial security labels:
  - Security_Severity-High: This is a browser process UAF that is triggerable from web content, but at its most exploitable requires a specific policy be set and a race condition be triggered with what I believe is browser shutdown.
  - FoundIn-102: This appears to also affect Stable channel.
  - OS: All Desktop platforms where this policy is supported.

I did some investigating to see if I could repro this using locally set policy. However, I'm unsure whether the policy didn't work, the race condition failed (without the added sleep() call, or because the window.close() call fails ("Scripts may close only the windows that were opened by them."). I think it would be nice if we could determine if this is reachable (even if flakey/takes a while to repeatedly attempt) against a standard Chromium ASAN instance with a policy set. I just used the sample policy here (https://chromeenterprise.google/policies/?policy=ManagedConfigurationPerOrigin) which I think should work, but I'd need to investigate more to determine what wasn't working:

"ManagedConfigurationPerOrigin": [
 {
  "origin": "https://www.google.com",
  "managed_configuration_url": "https://gstatic.google.com/configuration.json",
  "managed_configuration_hash": "asd891jedasd12ue9h"
 },
 {
  "origin": "https://www.example.com",
  "managed_configuration_url": "https://gstatic.google.com/configuration2.json",
  "managed_configuration_hash": "djio12easd89u12aws"
 }
]

[Monorail components: Blink>Managed Enterprise]

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-06-09)

Is anyone working on fixing this bug? thanks :)

### gl...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-06-09)

[Comment Deleted]

### et...@gmail.com (2022-06-09)

[Comment Deleted]

### [Deleted User] (2022-06-14)

bfranz: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-06-20)

[Empty comment from Monorail migration]

### bf...@chromium.org (2022-06-20)

[Empty comment from Monorail migration]

### bf...@chromium.org (2022-06-20)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-07-05)

Is anyone working on fixing this bug?


### je...@google.com (2022-07-05)

Yes, the CL has been uploaded and is ready to land (https://crrev.com/c/3714249).

### gi...@appspot.gserviceaccount.com (2022-07-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/303793c9100a3bada9b03951382a4d90e51c2a7a

commit 303793c9100a3bada9b03951382a4d90e51c2a7a
Author: Ben Franz <bfranz@google.com>
Date: Tue Jul 05 11:07:19 2022

Fix UAF issue

Make ManagedConfigurationStore a SequenceBound object. This ensures that
we do not read memory after destruction of ManagedConfigurationAPI
object.

Bug: 1330489
Change-Id: I9f4c5da2e0bb5e563881b8d7093973af04537a4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714249
Reviewed-by: Jeroen Dhollander <jeroendh@google.com>
Commit-Queue: Ben Franz <bfranz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1020807}

[modify] https://crrev.com/303793c9100a3bada9b03951382a4d90e51c2a7a/chrome/browser/device_api/managed_configuration_api.cc
[modify] https://crrev.com/303793c9100a3bada9b03951382a4d90e51c2a7a/chrome/browser/device_api/managed_configuration_store.h
[modify] https://crrev.com/303793c9100a3bada9b03951382a4d90e51c2a7a/chrome/browser/device_api/managed_configuration_api.h
[modify] https://crrev.com/303793c9100a3bada9b03951382a4d90e51c2a7a/chrome/browser/device_api/managed_configuration_store.cc


### bf...@chromium.org (2022-07-05)

Who can help me understand the back merge process (if necessary) for this CL?

### rs...@chromium.org (2022-07-05)

Marking it as Fixed will trigger sheriffbot to evaluate for backports.

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

Requesting merge to extended stable M102 because latest trunk commit (1020807) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1020807) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1020807) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-06)

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

### [Deleted User] (2022-07-06)

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

### [Deleted User] (2022-07-06)

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

### am...@chromium.org (2022-07-08)

Since this fix just landed two days ago AND it appears to be fairly mitigated (requires ManagedConfigurationPerOrigin policy to be set, beating race condition, and shutdown) AND is a pretty substantial change, I'm going to let this get some additional bake time in Canary over the weekend. 
We are currently in Chrome release freeze (aside from any potential emergency releases), so there we have even more time than usual to let this bake. 
Please monitor the performance of this fix on Canary and take not of any stability issues or other concerns in the interim.

Additionally, in reviewing this issue in terms of mitigation vs impact vs size/complexity of fix, we may not want to backmerge this fix to ES/102 and Stable/103; however the reason I would backmerge this is that it has a very specific impact on Enterprise configurations of Chrome, so this may be worth backmerging if safe to do so. 
Thus, performance on Canary is especially useful for this decision. 
Please let me know if any issues or concerns in general or with this plan. 

### am...@chromium.org (2022-07-12)

M104 merge approved, please merge this fix to branch 5112 at your earliest convenience 

### gi...@appspot.gserviceaccount.com (2022-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8060ac9b8478060dbcbc2bd60e6a51117132bec9

commit 8060ac9b8478060dbcbc2bd60e6a51117132bec9
Author: Ben Franz <bfranz@google.com>
Date: Wed Jul 13 11:33:06 2022

Fix UAF issue

Make ManagedConfigurationStore a SequenceBound object. This ensures that
we do not read memory after destruction of ManagedConfigurationAPI
object.

(cherry picked from commit 303793c9100a3bada9b03951382a4d90e51c2a7a)

Bug: 1330489
Change-Id: I9f4c5da2e0bb5e563881b8d7093973af04537a4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714249
Reviewed-by: Jeroen Dhollander <jeroendh@google.com>
Commit-Queue: Ben Franz <bfranz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1020807}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758208
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ben Franz <bfranz@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#847}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/8060ac9b8478060dbcbc2bd60e6a51117132bec9/chrome/browser/device_api/managed_configuration_store.h
[modify] https://crrev.com/8060ac9b8478060dbcbc2bd60e6a51117132bec9/chrome/browser/device_api/managed_configuration_api.cc
[modify] https://crrev.com/8060ac9b8478060dbcbc2bd60e6a51117132bec9/chrome/browser/device_api/managed_configuration_api.h
[modify] https://crrev.com/8060ac9b8478060dbcbc2bd60e6a51117132bec9/chrome/browser/device_api/managed_configuration_store.cc


### [Deleted User] (2022-07-13)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations, Nan Wang! The VRP Panel has decided to award you $5,000 for this report. The reward amount is based on this issue being fairly mitigated by race condition and shutdown. Thank you for your efforts and reporting this issue to us. 

### et...@gmail.com (2022-07-13)

[Comment Deleted]

### et...@gmail.com (2022-07-13)

[Comment Deleted]

### et...@gmail.com (2022-07-13)

[Comment Deleted]

### vo...@google.com (2022-07-14)

[Empty comment from Monorail migration]

### vo...@google.com (2022-07-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-14)

With the race condition and the browser shutdown as preconditions, I'm going to remove the merge labels for backmerge to ES and stable and this fix can be shipped in M104 stable which will also become extended stable support when M105 is promoted to stable. 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-15)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-15)

1. https://crrev.com/c/3762673
2. Low, no conflicts
3. 104
4. Yes

### gm...@google.com (2022-07-15)

Delaying on 96 until 104 goes to Stable. We will need to evaluate for LTC-102 once we take over the Chrome branch. @rzanoni

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

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

1. Just https://crrev.com/c/3816812
2. Low, no conflicts
3. 104
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/03fba18dbde5750b96274f934635510f21d71adf

commit 03fba18dbde5750b96274f934635510f21d71adf
Author: Ben Franz <bfranz@google.com>
Date: Fri Aug 12 09:27:29 2022

[M102-LTS] Fix UAF issue

Make ManagedConfigurationStore a SequenceBound object. This ensures that
we do not read memory after destruction of ManagedConfigurationAPI
object.

(cherry picked from commit 303793c9100a3bada9b03951382a4d90e51c2a7a)

Bug: 1330489
Change-Id: I9f4c5da2e0bb5e563881b8d7093973af04537a4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714249
Commit-Queue: Ben Franz <bfranz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1020807}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3816812
Owners-Override: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1291}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/03fba18dbde5750b96274f934635510f21d71adf/chrome/browser/device_api/managed_configuration_api.cc
[modify] https://crrev.com/03fba18dbde5750b96274f934635510f21d71adf/chrome/browser/device_api/managed_configuration_store.h
[modify] https://crrev.com/03fba18dbde5750b96274f934635510f21d71adf/chrome/browser/device_api/managed_configuration_api.h
[modify] https://crrev.com/03fba18dbde5750b96274f934635510f21d71adf/chrome/browser/device_api/managed_configuration_store.cc


### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d596e117c4acaa5038dde5afc11c100c2c5a5efd

commit d596e117c4acaa5038dde5afc11c100c2c5a5efd
Author: Ben Franz <bfranz@google.com>
Date: Fri Aug 12 10:37:27 2022

[M96-LTS] Fix UAF issue

Make ManagedConfigurationStore a SequenceBound object. This ensures that
we do not read memory after destruction of ManagedConfigurationAPI
object.

(cherry picked from commit 303793c9100a3bada9b03951382a4d90e51c2a7a)

Bug: 1330489
Change-Id: I9f4c5da2e0bb5e563881b8d7093973af04537a4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714249
Commit-Queue: Ben Franz <bfranz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1020807}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3762673
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1673}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/d596e117c4acaa5038dde5afc11c100c2c5a5efd/chrome/browser/device_api/managed_configuration_api.cc
[modify] https://crrev.com/d596e117c4acaa5038dde5afc11c100c2c5a5efd/chrome/browser/device_api/managed_configuration_store.h
[modify] https://crrev.com/d596e117c4acaa5038dde5afc11c100c2c5a5efd/chrome/browser/device_api/managed_configuration_api.h
[modify] https://crrev.com/d596e117c4acaa5038dde5afc11c100c2c5a5efd/chrome/browser/device_api/managed_configuration_store.cc


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### bf...@chromium.org (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1330489?no_tracker_redirect=1

[Multiple monorail components: Blink>Managed, Enterprise]
[Monorail mergedwith: crbug.com/chromium/1337671]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059808)*
