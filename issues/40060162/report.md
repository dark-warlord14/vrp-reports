# Security: use after free in IPH DemoMode NeverAvailabilityModel

| Field | Value |
|-------|-------|
| **Issue ID** | [40060162](https://issues.chromium.org/issues/40060162) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>FeatureEngagement |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | sh...@chromium.org |
| **Created** | 2022-07-05 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**  

windows

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 26.9 KB)
- [0001-trigger-uaf.patch](attachments/0001-trigger-uaf.patch) (text/plain, 2.2 KB)
- [0001-fix-uaf.patch](attachments/0001-fix-uaf.patch) (text/plain, 1.9 KB)

## Timeline

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-07-05)

https://source.chromium.org/chromium/chromium/src/+/main:components/feature_engagement/internal/never_availability_model.cc;l=25
```c++
void NeverAvailabilityModel::Initialize(OnInitializedCallback callback,
                                        uint32_t current_day) {
  base::ThreadTaskRunnerHandle::Get()->PostTask(
      FROM_HERE,
      base::BindOnce(&NeverAvailabilityModel::ForwardedOnInitializedCallback,
                     base::Unretained(this), std::move(callback)));  //passs base::unretain(this)
}
```
NeverAvailabilityModel will enter into 
https://source.chromium.org/chromium/chromium/src/+/main:components/feature_engagement/internal/tracker_impl.cc;l=100

```
Tracker* Tracker::Create(
    const base::FilePath& storage_dir,
    const scoped_refptr<base::SequencedTaskRunner>& background_task_runner,
    leveldb_proto::ProtoDatabaseProvider* db_provider) {
  DVLOG(2) << "Creating Tracker";
  if (base::FeatureList::IsEnabled(kIPHDemoMode))
    return CreateDemoModeTracker().release();
```

and Tracker will be a keyedservice. It will be destoryed when the profile destory. 
so if the tracker destoryed, the base::unretain(this) is unsafe, will cause uaf,
use my patch to win race condition.

my chromium commit is 5ded7754374000596f5484290519d8e7ee52c943









### wx...@gmail.com (2022-07-05)

after my patch, my command line is 
```
out\libfuzz\chrome.exe --no-sandbox
```

If  you have any questions, please tell me, thanks.


### da...@chromium.org (2022-07-05)

This is behind the IPH_DemoMode feature, which is disabled.

Unclear, given the name "Demo mode" if this is meant to ship in the future.

=> owners can you comment on if this code is going to ship? I see it was introduced 5 years ago. Should we remove it if not?

[Monorail components: Internals>FeatureEngagement]

### da...@chromium.org (2022-07-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2022-07-06)

IPH_DemoMode is still required. This is not meant to be removed, as it helps in manual validation of the IPH UI without needing an extensive finch setup while developing features.

If we change the NeverAvailabilityModel to use a weak ptr instead of using base::Unretained, that should fix the issue I suppose?

### wx...@gmail.com (2022-07-06)

yes, use https://bugs.chromium.org/p/chromium/issues/detail?id=1341887#c3 the patch is ok.

### gi...@appspot.gserviceaccount.com (2022-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/92593207a5a2903eb86ea108f657cf30c57a7547

commit 92593207a5a2903eb86ea108f657cf30c57a7547
Author: Shakti Sahu <shaktisahu@chromium.org>
Date: Wed Jul 06 19:48:18 2022

Fixed UAF for NeverAvailabilityModel

This CL fixes UAF for NeverAvailabilityModel by converting it to use a
weak ptr instead of base::Unretained.

Bug: 1341887
Change-Id: I1cb50c580315398461a36bc4b6d8a02bc28f7096
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3747490
Commit-Queue: Shakti Sahu <shaktisahu@chromium.org>
Reviewed-by: danakj <danakj@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1021320}

[modify] https://crrev.com/92593207a5a2903eb86ea108f657cf30c57a7547/components/feature_engagement/internal/never_availability_model_unittest.cc
[modify] https://crrev.com/92593207a5a2903eb86ea108f657cf30c57a7547/components/feature_engagement/internal/never_availability_model.h
[modify] https://crrev.com/92593207a5a2903eb86ea108f657cf30c57a7547/components/feature_engagement/internal/never_availability_model.cc


### sh...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2022-07-08)

Technically this is a UaF in the browser process, but it requires user interaction to destroy the profile, so I am going to reduce this to High. Introduced in https://source.chromium.org/chromium/chromium/src/+/9c02705b00898f8dd026c3ad9af909d0607526de, which predates the current extended stable, so marking as M102.

(I'm not convinced we should merge a fix for this, but shrug)

### sh...@chromium.org (2022-07-08)

Requesting merge to M104, and M103 (if possible)

### [Deleted User] (2022-07-08)

Merge rejected: M104 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-08)

Merge rejected: M103 is already shipping to stable and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2022-07-09)

Re-requesting merge to M104 as it has high impact as mentioned in https://crbug.com/chromium/1341887#c13

### [Deleted User] (2022-07-09)

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

### wx...@gmail.com (2022-07-10)

I don't think it needs to be merged as this bug need enable a feature.

### dc...@chromium.org (2022-07-10)

+1 it shouldn't be necessary to merge

(sheriffbot will usually automatically make merge requests if necessary; since this bug is tagged with Security_Impact-None, sheriffbot shouldn't request a merge for this)

### sh...@chromium.org (2022-07-10)

Thanks for chiming in. Yea, the bug needs to enable a  feature. Removing merge request.

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided upon due to this issue being quite mitigated by the race condition and user interaction. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-15)

This issue was migrated from crbug.com/chromium/1341887?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060162)*
