# Incorrect use of weakptr lead to uaf

| Field | Value |
|-------|-------|
| **Issue ID** | [40060043](https://issues.chromium.org/issues/40060043) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@gmail.com |
| **Assignee** | jg...@google.com |
| **Created** | 2022-06-22 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

1.python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/Asan  

2.apply patch.diff  

3.out/chromiumos/chrome --enable-blink-features=MojoJS '<http://localhost:8000/1.html>'  

4.close the window manually.

**Problem Description:**  

There is a race-condition bug in browser process.

FeatureStatusProviderImpl::OnReady() will post a task to threadpool with a weakptr to guarantee the this of FeatureStatusProviderImpl has not be destroyed when FeatureStatusProviderImpl::RecordFeatureStatusOnLogin being called. If FeatureStatusProviderImpl has been destroyed before FeatureStatusProviderImpl::RecordFeatureStatusOnLogin call on the threadpool. Then the weakptr will guarantee FeatureStatusProviderImpl::RecordFeatureStatusOnLogin will never be called. However if FeatureStatusProviderImpl::RecordFeatureStatusOnLogin is running to [1] in threadpool thread and FeatureStatusProviderImpl has been destroyed in UI thread. Then weakptr can not guard the UAF.And UAF will happen when accessing this in [2].

<https://source.chromium.org/chromium/chromium/src/+/main:ash/components/phonehub/feature_status_provider_impl.cc;l=169;bpv=1;bpt=1?q=eatureStatusProviderImpl::OnReady>

```
void FeatureStatusProviderImpl::OnReady() {  
UpdateStatus();  
// The status may change a few times before initialization is  
// complete. Before the login status is recorded, all asynchronous  
// action should be complete. Note that scheduling  
// RecordFeatureStatusOnLogin() with BEST_EFFORT sooner (e.g in the  
// constructor) may yield an incorrect metric, because there may be many  
// cycles between the constructor being called and |device_sync_client_| being  
// ready, allowing tasks posted even with BEST_EFFORT to succeed before  
// initialization.  
base::ThreadPool::PostTask(  
FROM_HERE, {base::TaskPriority::BEST_EFFORT},  
base::BindOnce(&FeatureStatusProviderImpl::RecordFeatureStatusOnLogin,  
weak_ptr_factory_.GetWeakPtr()));  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/main:ash/components/phonehub/feature_status_provider_impl.cc;l=303;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4;bpv=1;bpt=1>

```
void FeatureStatusProviderImpl::RecordFeatureStatusOnLogin() {  
UMA_HISTOGRAM_ENUMERATION("PhoneHub.Adoption.LoginFeatureStatus",  
-----------------[1]  
GetStatus());  
is_login_status_metric_recorded_ = true; --------[2]  
}  

```

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 20.0 KB)
- [1.html](attachments/1.html) (text/plain, 205 B)
- [sw.js](attachments/sw.js) (text/plain, 438 B)
- [patch.diff](attachments/patch.diff) (text/plain, 617 B)

## Timeline

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### ro...@gmail.com (2022-06-22)

Hear is the patch.diff

### ro...@gmail.com (2022-06-27)

Hello，is there any update？Thanks！

### lz...@google.com (2022-06-28)

[Empty comment from Monorail migration]

### ro...@gmail.com (2022-06-29)

[Comment Deleted]

### ro...@gmail.com (2022-06-29)

[Comment Deleted]

### ro...@gmail.com (2022-07-01)

[Comment Deleted]

### ro...@gmail.com (2022-07-04)

Friendly ping，is there any update？

### jo...@chromium.org (2022-07-08)

I've pinged Ryan offline.

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### ha...@chromium.org (2022-07-08)

Thanks for the report. Will triage shortly.

### ha...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-07-08)

This is still assigned to you though, is there a better owner? Normally just adding folks in CC doesn't really convey ownership.

### [Deleted User] (2022-07-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2022-07-11)

Josh will be authoring the fix to this.

### jg...@google.com (2022-07-11)

[Empty comment from Monorail migration]

### ha...@chromium.org (2022-07-13)

Josh has a fix at crrev.com/c/3758791, but stepping back, the problematic code may actually be unnecessary. We're talking with the owner of the metric that requires this code tomorrow (jonmann@) to understand if we can simply rip out this code path. Will update tomorrow.

### jg...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/23ddf139937c57c7a9528afef1be2ce4f8f5c46f

commit 23ddf139937c57c7a9528afef1be2ce4f8f5c46f
Author: Josh Graydus <jgraydus@google.com>
Date: Mon Jul 18 17:04:55 2022

Remove metric "PhoneHub.Adoption.LoginFeatureStatus".

We decided that this metric is of no value, and by removing the problematic way in which it is recorded we fix the use-after-free bug.

Change-Id: I36961e540233a637eb4fcebc8cd2c9ce86945ba3
Fixed: 1338553
Tested: Deployed to an atlas and verified that logging in works.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758791
Commit-Queue: Josh Graydus <jgraydus@google.com>
Reviewed-by: Juliet Lévesque <julietlevesque@google.com>
Reviewed-by: Crisrael Lucero <crisrael@google.com>
Reviewed-by: Ryan Hansberry <hansberry@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1025283}

[modify] https://crrev.com/23ddf139937c57c7a9528afef1be2ce4f8f5c46f/ash/components/phonehub/feature_status_provider_impl.cc
[modify] https://crrev.com/23ddf139937c57c7a9528afef1be2ce4f8f5c46f/ash/components/phonehub/feature_status_provider_impl.h
[modify] https://crrev.com/23ddf139937c57c7a9528afef1be2ce4f8f5c46f/tools/metrics/histograms/metadata/phonehub/histograms.xml


### [Deleted User] (2022-07-18)

Requesting merge to extended stable M102 because latest trunk commit (1025283) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1025283) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1025283) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-19)

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

### [Deleted User] (2022-07-19)

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

### [Deleted User] (2022-07-19)

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

### ha...@chromium.org (2022-07-19)

Security (jorgelo@) is not requesting 102 merge -- removing that.

Rationale for 103 and 104 merge: 

1. Why does your merge fit within the merge criteria for these milestones?
103 and 104 merges have been requested by Security team.

2. What changes specifically would you like to merge? Please link to Gerrit.
crrev.com/c/3758791

3. Have the changes been released and tested on canary?
*This change is not yet in canary: will fill this out once that's available.*

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, it is a small security fix on an existing feature.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
*Not yet: waiting to test on canary*

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No.

Josh and I will loop back here once canary testing is available and performed.

### ha...@chromium.org (2022-07-19)

[Empty comment from Monorail migration]

### dg...@google.com (2022-07-21)

Approved for M103. Note, we are not targeting releasing another M103 Stable at this point since M104 is going Stable on Aug 4

### [Deleted User] (2022-07-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2022-07-26)

Josh is double-checking on canary and will cherrypick later today.

### ha...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### dh...@chromium.org (2022-07-27)

lgtm

### ha...@chromium.org (2022-07-27)

Also requesting merge to 105.

### ha...@chromium.org (2022-07-27)

Will merge to 103 now and then seek approval for 104 and 105.

### [Deleted User] (2022-07-27)

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

### ha...@chromium.org (2022-07-27)

Rationale for 104 and 105 merge: 

1. Why does your merge fit within the merge criteria for these milestones?
103 and 104 merges have been requested by Security team.

2. What changes specifically would you like to merge? Please link to Gerrit.
crrev.com/c/3758791

3. Have the changes been released and tested on canary?
Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, it is a small security fix on an existing feature.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
Yes.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No.

### ma...@google.com (2022-07-27)

Approved, M-105

### dg...@google.com (2022-07-28)

Approved for M104. Please be sure to merge this change as soon as possible as we are promoting to stable next week.

Merge approved for M103 as well but we are not planning any more M103 Stable releases.

### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/59dd036864f77627f6515937f1b91120bcaaaa32

commit 59dd036864f77627f6515937f1b91120bcaaaa32
Author: Josh Graydus <jgraydus@google.com>
Date: Thu Jul 28 19:23:05 2022

Remove metric "PhoneHub.Adoption.LoginFeatureStatus".

We decided that this metric is of no value, and by removing the problematic way in which it is recorded we fix the use-after-free bug.

(cherry picked from commit 23ddf139937c57c7a9528afef1be2ce4f8f5c46f)

Change-Id: I36961e540233a637eb4fcebc8cd2c9ce86945ba3
Fixed: 1338553
Tested: Deployed to an atlas and verified that logging in works.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758791
Commit-Queue: Josh Graydus <jgraydus@google.com>
Reviewed-by: Juliet Lévesque <julietlevesque@google.com>
Reviewed-by: Crisrael Lucero <crisrael@google.com>
Reviewed-by: Ryan Hansberry <hansberry@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1025283}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3791798
Cr-Commit-Position: refs/branch-heads/5112@{#1267}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/59dd036864f77627f6515937f1b91120bcaaaa32/ash/components/phonehub/feature_status_provider_impl.cc
[modify] https://crrev.com/59dd036864f77627f6515937f1b91120bcaaaa32/ash/components/phonehub/feature_status_provider_impl.h
[modify] https://crrev.com/59dd036864f77627f6515937f1b91120bcaaaa32/tools/metrics/histograms/metadata/phonehub/histograms.xml


### [Deleted User] (2022-07-28)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2022-07-28)

Leaving open until the 105 merge lands.

### ha...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### ha...@chromium.org (2022-07-28)

The fix landed in 105.0.5189.0 -- no need for 105 merge. 

Leaving open for 103 merge.

### rz...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-29)

1. https://crrev.com/c/3790997
2. Low, just a minor data type conflict for a property
3. 103, 104
4. Yes

### [Deleted User] (2022-08-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-08-02)

Not merged to 103. Delaying until 104 goes to stable. Also, rzanoni@ please evaluate for 102.

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7b43bcac6cb43f98332a53b484f096d4b2f622dd

commit 7b43bcac6cb43f98332a53b484f096d4b2f622dd
Author: Josh Graydus <jgraydus@google.com>
Date: Wed Aug 03 22:13:19 2022

Remove metric "PhoneHub.Adoption.LoginFeatureStatus".

We decided that this metric is of no value, and by removing the problematic way in which it is recorded we fix the use-after-free bug.

(cherry picked from commit 23ddf139937c57c7a9528afef1be2ce4f8f5c46f)

Change-Id: I36961e540233a637eb4fcebc8cd2c9ce86945ba3
Fixed: 1338553
Tested: Deployed to an atlas and verified that logging in works.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758791
Commit-Queue: Josh Graydus <jgraydus@google.com>
Reviewed-by: Juliet Lévesque <julietlevesque@google.com>
Reviewed-by: Crisrael Lucero <crisrael@google.com>
Reviewed-by: Ryan Hansberry <hansberry@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1025283}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3791573
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#1320}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/7b43bcac6cb43f98332a53b484f096d4b2f622dd/ash/components/phonehub/feature_status_provider_impl.cc
[modify] https://crrev.com/7b43bcac6cb43f98332a53b484f096d4b2f622dd/ash/components/phonehub/feature_status_provider_impl.h
[modify] https://crrev.com/7b43bcac6cb43f98332a53b484f096d4b2f622dd/tools/metrics/histograms/metadata/phonehub/histograms.xml


### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-08)

Approved for LTS-96, @rzanoni please cherry pick for LTC-102 as well

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

1. Just https://crrev.com/c/3817890
2. Low, no conflicts
3. 103, 104
4. Yes

### gi...@appspot.gserviceaccount.com (2022-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1769f03b84145a37d23e95ec7bc057128821035c

commit 1769f03b84145a37d23e95ec7bc057128821035c
Author: Josh Graydus <jgraydus@google.com>
Date: Tue Aug 09 12:15:42 2022

[M96-LTS] Remove metric "PhoneHub.Adoption.LoginFeatureStatus".

M96 merge issues:
  histograms.xml:
    Conflicting value for expires_after property

We decided that this metric is of no value, and by removing the problematic way in which it is recorded we fix the use-after-free bug.

(cherry picked from commit 23ddf139937c57c7a9528afef1be2ce4f8f5c46f)

Change-Id: I36961e540233a637eb4fcebc8cd2c9ce86945ba3
Fixed: 1338553
Tested: Deployed to an atlas and verified that logging in works.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758791
Commit-Queue: Josh Graydus <jgraydus@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1025283}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3790997
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1671}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/1769f03b84145a37d23e95ec7bc057128821035c/chromeos/components/phonehub/feature_status_provider_impl.cc
[modify] https://crrev.com/1769f03b84145a37d23e95ec7bc057128821035c/tools/metrics/histograms/metadata/phonehub/histograms.xml
[modify] https://crrev.com/1769f03b84145a37d23e95ec7bc057128821035c/chromeos/components/phonehub/feature_status_provider_impl.h


### gm...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. The reward amount was decided upon based on this issue being mitigated by race condition and browser shutdown. Thank you for your efforts in reporting this issue to us and nice work! 

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/76b4def6de82c9434c9bae3d235d886515625b1d

commit 76b4def6de82c9434c9bae3d235d886515625b1d
Author: Josh Graydus <jgraydus@google.com>
Date: Fri Aug 12 09:14:22 2022

[M102-LTS] Remove metric "PhoneHub.Adoption.LoginFeatureStatus".

We decided that this metric is of no value, and by removing the problematic way in which it is recorded we fix the use-after-free bug.

(cherry picked from commit 23ddf139937c57c7a9528afef1be2ce4f8f5c46f)

Change-Id: I36961e540233a637eb4fcebc8cd2c9ce86945ba3
Fixed: 1338553
Tested: Deployed to an atlas and verified that logging in works.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758791
Commit-Queue: Josh Graydus <jgraydus@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1025283}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3817890
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1290}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/76b4def6de82c9434c9bae3d235d886515625b1d/ash/components/phonehub/feature_status_provider_impl.cc
[modify] https://crrev.com/76b4def6de82c9434c9bae3d235d886515625b1d/ash/components/phonehub/feature_status_provider_impl.h
[modify] https://crrev.com/76b4def6de82c9434c9bae3d235d886515625b1d/tools/metrics/histograms/metadata/phonehub/histograms.xml


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### br...@gmail.com (2022-11-11)

Hello,

Is it possible to undelete POC on https://crbug.com/chromium/1338553#c0 for educational purpose?

Thanks

### am...@chromium.org (2022-11-11)

Thanks, looks like they've been undeleted.
OP, for future reference, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. 

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1338553?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060043)*
