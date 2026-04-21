# Incorrect use of weakptr lead to UAF in NearbyShare

| Field | Value |
|-------|-------|
| **Issue ID** | [40060044](https://issues.chromium.org/issues/40060044) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@gmail.com |
| **Assignee** | jg...@google.com |
| **Created** | 2022-06-22 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

This bug is similar to the 1338553.Bug it seems need a real chromebook so I can't trigger it.

**Problem Description:**  

There is two race-condition bug in browser process similar to the previous one <https://bugs.chromium.org/p/chromium/issues/detail?id=1338553>..

ArcNearbyShareBridge::ArcNearbyShareBridge() will post a task to threadpool with a weakptr to guarantee the this of FeatureStatusProviderImpl has not be destroyed when ArcNearbyShareBridge::DeleteShareCacheFilePaths being called.  

If ArcNearbyShareBridge has been destroyed before ArcNearbyShareBridge::DeleteShareCacheFilePaths call on the threadpool. Then the weakptr will guarantee ArcNearbyShareBridge::DeleteShareCacheFilePaths will never be called.  

However if ArcNearbyShareBridge::DeleteShareCacheFilePaths is running to [1] in threadpool thread when ArcNearbyShareBridge has been destroyed in UI thread. Then UAF will happen when accessing this in [2].  

Another uaf is when profile has been destroyed on ui thread when ArcNearbyShareBridge::DeleteShareCacheFilePaths is running to [1]. Then UAF will happen when accessing profile.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.cc;l=68;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4;bpv=0;bpt=1>

```
ArcNearbyShareBridge::ArcNearbyShareBridge(  
content::BrowserContext\* browser_context,  
ArcBridgeService\* bridge_service)  
: arc_bridge_service_(bridge_service),  
profile_(Profile::FromBrowserContext(browser_context)) {  
DCHECK_CURRENTLY_ON(content::BrowserThread::UI);  
arc_bridge_service_->nearby_share()->SetHost(this);  
// On startup, delete the ARC Nearby Share cache path.  
base::ThreadPool::PostTask(  
FROM_HERE, {base::MayBlock()},  
base::BindOnce(&ArcNearbyShareBridge::DeleteShareCacheFilePaths,  
weak_ptr_factory_.GetWeakPtr()));  
}  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.cc;l=89;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4;bpv=1;bpt=1>

```
void ArcNearbyShareBridge::DeleteShareCacheFilePaths() {  
DCHECK(profile_);  
--------------------[1]  
NearbyShareSessionImpl::DeleteShareCacheFilePaths(profile_);-----------------------------[2]  
}  
  

```

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Timeline

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### lz...@google.com (2022-06-28)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-07-08)

Gonna mark it as High for now until we can figure out how trigger-able this is.

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### ha...@chromium.org (2022-07-08)

Thanks for the report. Will triage shortly.

### ha...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-07-08)

Same comment here about making sure the right owner is assigned.

### [Deleted User] (2022-07-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2022-07-11)

Josh will be working on this once he authors a fix for crbug.com/1338553.

### ha...@chromium.org (2022-07-11)

[Empty comment from Monorail migration]

### ha...@chromium.org (2022-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

jgraydus: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2022-07-12)

Sheriffbot missed the update above somehow. Josh will be tackling this shortly after wrapping up crbug.com/1338553 (which he already has a fix in mind for).

### ha...@chromium.org (2022-07-13)

Josh is beginning work on this now.

### jg...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fb18e53c4d26e60d5158ff581709400c83784466

commit fb18e53c4d26e60d5158ff581709400c83784466
Author: Josh Graydus <jgraydus@google.com>
Date: Tue Jul 26 17:00:04 2022

[Nearby Share] remove unsafe reference to object from another thread

ArcNearbyShareBridge wants to do a blocking operation on creation. In order to prevent blocking the ui thread, this operation is posted as a task to a thread pool. As currently implemented, this task is a method call on the ArcNearbyShareBridge object. However, this is problematic because there's no mechanism to guarantee the callee isn't destroyed during the method execution. This would lead to a use-after-free situation.

In order to resolve the issue, I reduced the task to only include the blocking operations. Since those operations only require string arguments which the task can own, there's no longer any risk of use-after-free.


Change-Id: Iff5c75b71d0ac376e31fd7239d75f3b5e538998a
Fixed: 1338560
Tested: deployed to atlas device and manually verified that I can log in
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3763584
Reviewed-by: Michael Hansen <hansenmichael@google.com>
Commit-Queue: Josh Graydus <jgraydus@google.com>
Reviewed-by: Ryan Hansberry <hansberry@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1028320}

[modify] https://crrev.com/fb18e53c4d26e60d5158ff581709400c83784466/chrome/browser/ash/arc/nearby_share/nearby_share_session_impl.cc
[modify] https://crrev.com/fb18e53c4d26e60d5158ff581709400c83784466/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.cc
[modify] https://crrev.com/fb18e53c4d26e60d5158ff581709400c83784466/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.h


### [Deleted User] (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

Requesting merge to extended stable M102 because latest trunk commit (1028320) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1028320) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1028320) appears to be after beta branch point (1012729).

Requesting merge to dev M105 because latest trunk commit (1028320) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-07-27)

Approved for M105, if needed.

### ob...@google.com (2022-07-27)

Please complete the questions below:

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

### [Deleted User] (2022-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-27)

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

### [Deleted User] (2022-07-27)

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

### [Deleted User] (2022-07-27)

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

### ha...@chromium.org (2022-07-27)

Re-opening to ensure we merge to 103, 104, and 105.

Security (jorgelo@) is not requesting 102 merge -- removing that.

Merge review responses:

1. Why does your merge fit within the merge criteria for these milestones?
103 and 104 merges have been requested by Security team.

2. What changes specifically would you like to merge? Please link to Gerrit.
crrev.com/c/3763584

3. Have the changes been released and tested on canary?
Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, it is a small security fix on an existing feature.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
*Confirming with dhaddock@*

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No.

### ha...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### dh...@chromium.org (2022-07-27)

lgtm

### ha...@chromium.org (2022-07-27)

Thanks David. We'll merge to 105 now. Waiting on TPM to confirm 103 and 104 merge.

### ch...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### dg...@google.com (2022-07-28)

Approved for M104. Please be sure to merge this change as soon as possible as we are promoting to stable next week.

I also approved for M103 but we are not planning any more M103 releases.

### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f7d2376407d7d403d0f707cff36e2a830d040f27

commit f7d2376407d7d403d0f707cff36e2a830d040f27
Author: Josh Graydus <jgraydus@google.com>
Date: Thu Jul 28 17:25:17 2022

[Nearby Share] remove unsafe reference to object from another thread

ArcNearbyShareBridge wants to do a blocking operation on creation. In order to prevent blocking the ui thread, this operation is posted as a task to a thread pool. As currently implemented, this task is a method call on the ArcNearbyShareBridge object. However, this is problematic because there's no mechanism to guarantee the callee isn't destroyed during the method execution. This would lead to a use-after-free situation.

In order to resolve the issue, I reduced the task to only include the blocking operations. Since those operations only require string arguments which the task can own, there's no longer any risk of use-after-free.


(cherry picked from commit fb18e53c4d26e60d5158ff581709400c83784466)

Change-Id: Iff5c75b71d0ac376e31fd7239d75f3b5e538998a
Fixed: 1338560
Tested: deployed to atlas device and manually verified that I can log in
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3763584
Reviewed-by: Michael Hansen <hansenmichael@google.com>
Commit-Queue: Josh Graydus <jgraydus@google.com>
Reviewed-by: Ryan Hansberry <hansberry@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028320}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3789914
Cr-Commit-Position: refs/branch-heads/5195@{#97}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/f7d2376407d7d403d0f707cff36e2a830d040f27/chrome/browser/ash/arc/nearby_share/nearby_share_session_impl.cc
[modify] https://crrev.com/f7d2376407d7d403d0f707cff36e2a830d040f27/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.cc
[modify] https://crrev.com/f7d2376407d7d403d0f707cff36e2a830d040f27/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.h


### [Deleted User] (2022-07-28)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/553b7953c3f36db9bbd08db4c7d2a80c96016f7d

commit 553b7953c3f36db9bbd08db4c7d2a80c96016f7d
Author: Josh Graydus <jgraydus@google.com>
Date: Thu Jul 28 17:49:05 2022

[Nearby Share] remove unsafe reference to object from another thread

ArcNearbyShareBridge wants to do a blocking operation on creation. In order to prevent blocking the ui thread, this operation is posted as a task to a thread pool. As currently implemented, this task is a method call on the ArcNearbyShareBridge object. However, this is problematic because there's no mechanism to guarantee the callee isn't destroyed during the method execution. This would lead to a use-after-free situation.

In order to resolve the issue, I reduced the task to only include the blocking operations. Since those operations only require string arguments which the task can own, there's no longer any risk of use-after-free.


(cherry picked from commit fb18e53c4d26e60d5158ff581709400c83784466)

Change-Id: Iff5c75b71d0ac376e31fd7239d75f3b5e538998a
Fixed: 1338560
Tested: deployed to atlas device and manually verified that I can log in
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3763584
Reviewed-by: Michael Hansen <hansenmichael@google.com>
Commit-Queue: Josh Graydus <jgraydus@google.com>
Reviewed-by: Ryan Hansberry <hansberry@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028320}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3791568
Cr-Commit-Position: refs/branch-heads/5112@{#1264}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/553b7953c3f36db9bbd08db4c7d2a80c96016f7d/chrome/browser/ash/arc/nearby_share/nearby_share_session_impl.cc
[modify] https://crrev.com/553b7953c3f36db9bbd08db4c7d2a80c96016f7d/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.cc
[modify] https://crrev.com/553b7953c3f36db9bbd08db4c7d2a80c96016f7d/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.h


### rz...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-29)

Most of the changed code isn't on M96

### [Deleted User] (2022-08-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7cecc42d7e65a0bf9648529435106f9cb5c0d014

commit 7cecc42d7e65a0bf9648529435106f9cb5c0d014
Author: Josh Graydus <jgraydus@google.com>
Date: Mon Aug 01 17:56:56 2022

[Nearby Share] remove unsafe reference to object from another thread

ArcNearbyShareBridge wants to do a blocking operation on creation. In order to prevent blocking the ui thread, this operation is posted as a task to a thread pool. As currently implemented, this task is a method call on the ArcNearbyShareBridge object. However, this is problematic because there's no mechanism to guarantee the callee isn't destroyed during the method execution. This would lead to a use-after-free situation.

In order to resolve the issue, I reduced the task to only include the blocking operations. Since those operations only require string arguments which the task can own, there's no longer any risk of use-after-free.


(cherry picked from commit fb18e53c4d26e60d5158ff581709400c83784466)

Change-Id: Iff5c75b71d0ac376e31fd7239d75f3b5e538998a
Fixed: 1338560
Tested: deployed to atlas device and manually verified that I can log in
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3763584
Reviewed-by: Michael Hansen <hansenmichael@google.com>
Commit-Queue: Josh Graydus <jgraydus@google.com>
Reviewed-by: Ryan Hansberry <hansberry@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028320}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3789830
Reviewed-by: Melissa Zhang <melzhang@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#1312}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/7cecc42d7e65a0bf9648529435106f9cb5c0d014/chrome/browser/ash/arc/nearby_share/nearby_share_session_impl.cc
[modify] https://crrev.com/7cecc42d7e65a0bf9648529435106f9cb5c0d014/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.cc
[modify] https://crrev.com/7cecc42d7e65a0bf9648529435106f9cb5c0d014/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.h


### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-05)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. The reward amount decided upon was based on this issue being mitigated by race condition and profile destruction. Thank you for your efforts and reporting this issue to us! 

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

1. Just https://crrev.com/c/3816904
2. Low, no conflicts
3. 103, 104, 105
4. Yes

### gm...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/516e0f2a032d8476bd7c381a641244c142354140

commit 516e0f2a032d8476bd7c381a641244c142354140
Author: Josh Graydus <jgraydus@google.com>
Date: Fri Aug 12 09:10:32 2022

[M102-LTS][Nearby Share] remove unsafe reference to object from another thread

ArcNearbyShareBridge wants to do a blocking operation on creation. In order to prevent blocking the ui thread, this operation is posted as a task to a thread pool. As currently implemented, this task is a method call on the ArcNearbyShareBridge object. However, this is problematic because there's no mechanism to guarantee the callee isn't destroyed during the method execution. This would lead to a use-after-free situation.

In order to resolve the issue, I reduced the task to only include the blocking operations. Since those operations only require string arguments which the task can own, there's no longer any risk of use-after-free.


(cherry picked from commit fb18e53c4d26e60d5158ff581709400c83784466)

Change-Id: Iff5c75b71d0ac376e31fd7239d75f3b5e538998a
Fixed: 1338560
Tested: deployed to atlas device and manually verified that I can log in
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3763584
Reviewed-by: Michael Hansen <hansenmichael@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1028320}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3816904
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1289}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/516e0f2a032d8476bd7c381a641244c142354140/chrome/browser/ash/arc/nearby_share/nearby_share_session_impl.cc
[modify] https://crrev.com/516e0f2a032d8476bd7c381a641244c142354140/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.cc
[modify] https://crrev.com/516e0f2a032d8476bd7c381a641244c142354140/chrome/browser/ash/arc/nearby_share/arc_nearby_share_bridge.h


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

fix was already released in release-1-m104 

### [Deleted User] (2022-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1338560?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060044)*
