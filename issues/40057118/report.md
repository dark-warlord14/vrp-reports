# heap-use-after-free in OnBrowserSetLastActive

| Field | Value |
|-------|-------|
| **Issue ID** | [40057118](https://issues.chromium.org/issues/40057118) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2021-09-01 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36

Steps to reproduce the problem:
I don’t know how to trigger the function OnBrowserSetLastActive[1]. It seems chromium disable signin and it’s only used in chrome. But I think it’s the real bug because profile will be destroyed when browser is closed. 
If we know how to trigger the function OnBrowserSetLastActive[1].We can use an extension to close all the tab to destroyed the profile and triggered the UAF or
 use a tab run with settimeout(function(){window.close()},n) to close themselves so close the browser with a delay. 

What is the expected behavior?

What went wrong?
1、OnBrowserSetLastActive[1] will call chrome::ShowWarningMessageBox[2].
2、chrome::ShowWarningMessageBox[2] will run a nested message loop and if browser is closed while the message loop is running. Profile will be destroyed.
Then UAF will be triggered when accessing profile in profile_->GetPath()[3]

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/signin/signin_util.cc;l=80;drc=b46a82c56ba82d3643803509501c6e236a81fcf0;bpv=1;bpt=1

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/signin/signin_util.cc;l=86;bpv=1;bpt=1?q=signin_util.cc

[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/signin/signin_util.cc;l=96;drc=b46a82c56ba82d3643803509501c6e236a81fcf0;bpv=1;bpt=1

Did this work before? N/A 

Chrome version: 92.0.4515.159  Channel: n/a
OS Version:

## Timeline

### [Deleted User] (2021-09-01)

[Empty comment from Monorail migration]

### ct...@chromium.org (2021-09-02)

Thanks for the report! It seems plausible that a sufficiently wiley attacker could abuse this by spraying similarly sized objects that get allocated into the browser process. This does require browser shutdown (manually by the user or through a second vector as mentioned in the report), which mitigates this a little (so Severity-Hight). This appears to only affect Desktop platforms (#if defined(CAN_DELETE_PROFILE), which is W/M/L/ChromeOS) and might have been around since crrev.com/c/1352360 (so FoundIn-72).

Setting some security labels and passing this to Sign-in folks. msarda@ could you take a look?

[Monorail components: Services>SignIn]

### ct...@chromium.org (2021-09-02)

Also, to the reporter: If you can figure out a PoC, we'd love to see one! We're definitely interested in building up a richer understanding of how attackers can trigger profile/browser shutdown bugs :-)

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### ro...@gmail.com (2021-09-03)

Very sorry. After my deep analysis. I find it seems this function can only be triggered when there's a primary account exist in the browser which disallow primary account. It seems an attacker should let user add a primary account at first but I can't find a way to reach this. 

### ct...@chromium.org (2021-09-03)

No worries -- we should still fix this as we've seen a few similar bugs and an attacker might be able to come up with a way to exploit this. Thanks again for your report and for taking the time to help analyze this case!

### [Deleted User] (2021-09-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-15)

msarda: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2021-09-15)

When OnBrowserSetLastActive(Browser* browser) is called, |browser| is the new active browser window. The profile of this browser window exists (browser object keeps its profile alive). 

chrome::ShowWarningMessageBox shows a dialog that is blocking on this last browser window. It spins the run loop waiting for the browser to close. What you are saying is that it is possible for the browser and the profile objects to be destroyed while the run loop spins. That is an interesting case, not sure if it can be reproduced though.

In any case, avoiding accessing the profile after ShowWarningMessageBox does not cost us much, so I could prepare a CL that does that.



### ms...@chromium.org (2021-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-31)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c5e30ea5d1bcd339715df71b364b8b6243c36f2c

commit c5e30ea5d1bcd339715df71b364b8b6243c36f2c
Author: Mihai Sardarescu <msarda@chromium.org>
Date: Thu Nov 18 13:01:38 2021

Use profile path instead of profile in profile will be deleted dialog

This CL uses the profile path instead of the profile while presenting
the profile will be deleted dialog to avoid any UAF in case the profile
object is destroyed while this dialog is presented.

Fixed: 1245629
Change-Id: Id0c38c2e19acfb37feae5693b511c4d8a2a35b7e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3268757
Commit-Queue: Mihai Sardarescu <msarda@chromium.org>
Auto-Submit: Mihai Sardarescu <msarda@chromium.org>
Reviewed-by: Alex Ilin <alexilin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#943046}

[modify] https://crrev.com/c5e30ea5d1bcd339715df71b364b8b6243c36f2c/chrome/browser/signin/signin_util.cc


### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-18)

Requesting merge to stable M96 because latest trunk commit (943046) appears to be after stable branch point (929512).

Requesting merge to dev M97 because latest trunk commit (943046) appears to be after dev branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-19)

Merge review required: M97 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-19)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-11-22)

Merge approved for M96 and M97; as long as there are not stability or other concerns since this landed on Canary, please merge to branches 4664 and 4692 respectively. Thanks! 

### am...@chromium.org (2021-11-22)

would probably help if I added approval labels :) 

### am...@google.com (2021-11-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-24)

Congratulations, the VRP Panel has decided to award you $5000 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please let us know a name or handle/pseudonym you would like us to use for attribution of this issue in release notes. Thank you for this report and nice work! 

### ro...@gmail.com (2021-11-24)

[Comment Deleted]

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2021-11-29)

I really do not think we need to merge to M96. This is a theoretical bug  that could only affect a very very small number of users (enterprise users that enable restrict accounts to pattern and where the user is already signed in with a non-authorized account). We have no evidence of this UAF in production code. I'll merge to M97.

amyressler@: Please advice if this needs to be merged to M96 stable.

### ms...@chromium.org (2021-11-29)

Merge to M97 CL is here: https://chromium-review.googlesource.com/c/chromium/src/+/3304221

### pb...@google.com (2021-11-29)

Your change has been approved for M97 branch,please go ahead and merge the CL's to M97 branch:4692 manually asap so that they would be part of this week's first M97 Beta release.

### am...@chromium.org (2021-11-29)

msarda@ thank you for the insight about this code; I concur with not merging this to M96, but please proceed with merge to M97 as soon as possible given the note above  -- thank you! 

### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/98d542e27f9c87cf0fce0cbd8615594ca8e4d2b9

commit 98d542e27f9c87cf0fce0cbd8615594ca8e4d2b9
Author: Mihai Sardarescu <msarda@chromium.org>
Date: Tue Nov 30 11:15:00 2021

Use profile path instead of profile in profile will be deleted dialog

This CL uses the profile path instead of the profile while presenting
the profile will be deleted dialog to avoid any UAF in case the profile
object is destroyed while this dialog is presented.

(cherry picked from commit c5e30ea5d1bcd339715df71b364b8b6243c36f2c)

Fixed: 1245629
Change-Id: Id0c38c2e19acfb37feae5693b511c4d8a2a35b7e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3268757
Commit-Queue: Mihai Sardarescu <msarda@chromium.org>
Auto-Submit: Mihai Sardarescu <msarda@chromium.org>
Reviewed-by: Alex Ilin <alexilin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#943046}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3304221
Cr-Commit-Position: refs/branch-heads/4692@{#570}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/98d542e27f9c87cf0fce0cbd8615594ca8e4d2b9/chrome/browser/signin/signin_util.cc


### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### gm...@google.com (2022-01-05)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2022-02-01)

1. Just one https://crrev.com/c/3376822
2. Low - no conflicts
3. Stable - M97, M98
4. Yes

### gm...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-02-02)

We concluded in https://crbug.com/chromium/1245629#c30 above that this does not need to be merged to M96.

### gm...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5440642a53181a716e6018ec6c8b79e4ac8ded77

commit 5440642a53181a716e6018ec6c8b79e4ac8ded77
Author: Mihai Sardarescu <msarda@chromium.org>
Date: Sat Feb 05 13:29:57 2022

[M96-LTS] Use profile path instead of profile in profile will be deleted dialog

This CL uses the profile path instead of the profile while presenting
the profile will be deleted dialog to avoid any UAF in case the profile
object is destroyed while this dialog is presented.

(cherry picked from commit c5e30ea5d1bcd339715df71b364b8b6243c36f2c)

(cherry picked from commit 98d542e27f9c87cf0fce0cbd8615594ca8e4d2b9)

Fixed: 1245629
Change-Id: Id0c38c2e19acfb37feae5693b511c4d8a2a35b7e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3268757
Commit-Queue: Mihai Sardarescu <msarda@chromium.org>
Auto-Submit: Mihai Sardarescu <msarda@chromium.org>
Reviewed-by: Alex Ilin <alexilin@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#943046}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3304221
Cr-Original-Commit-Position: refs/branch-heads/4692@{#570}
Cr-Original-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3376822
Reviewed-by: Mihai Sardarescu <msarda@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1453}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/5440642a53181a716e6018ec6c8b79e4ac8ded77/chrome/browser/signin/signin_util.cc


### vo...@google.com (2022-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1245629?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057118)*
