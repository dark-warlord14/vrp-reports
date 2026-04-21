# Security: Chrome Browser Policy Bypass "Allow invocation of file selection dialogs"

| Field | Value |
|-------|-------|
| **Issue ID** | [40053555](https://issues.chromium.org/issues/40053555) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | be...@gmail.com |
| **Assignee** | yd...@chromium.org |
| **Created** | 2020-10-12 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

I was working on a "Kiosk Mode Breakout" type of assessment where the only available application to the user is a current Google Chrome installation, heavily restricted by Chrome Browser Policies (<https://support.google.com/chrome/a/answer/187202>) when I found a way to bypass the "Allow invocation of file selection dialogs" policy with Chrome internals.  

At chrome://webrtc-internals the two checkboxes "Enable diagnostic audio recordings" and "Enable diagnostic packet and event recording" in the "Create Dump" subsection open a (unrestricted by filetype) file selection dialog even if the Chrome Browser Policy "AllowFileSelectionDialogs" is set.

**VERSION**  

Chrome Version: 86.0.4240.75 (Official Build) (64-bit)  

Operating System: Windows 10 64bit Version 2004 (OS Build 19041.546)

**REPRODUCTION CASE**

- Set "AllowFileSelectionDialogs" policy to "Disabled" through GPO
- Navigate to chrome://webrtc-internals
- Click on either of the two checkboxes in the "Create Dump" subsection
- Outcome: a file selection dialog opens
- Expected outcome: file dialog does not open and Chrome reports "Access to local files on your machine is disabled by your administrator"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

no crashes triggered

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: vvmute (Benjamin Petermaier)

## Timeline

### me...@chromium.org (2020-10-12)

Thanks for the report. This is similar to https://crbug.com/chromium/1054966 which was treated as a security bug, so triaging similarly.

ydago: PTAL?

[Monorail components: Enterprise]

### [Deleted User] (2020-10-12)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-26)

ydago: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yd...@chromium.org (2020-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0915ac94ccd5d05266009907215e94a8aab1baad

commit 0915ac94ccd5d05266009907215e94a8aab1baad
Author: Yann Dago <ydago@chromium.org>
Date: Thu Nov 05 17:57:31 2020

Enforce AllowFileSelectionDialogs on chrome://webrtc-internals/

Bug: 1137362
Change-Id: I41c4d316f614358ecb53a81f08216e00d0146081
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508229
Reviewed-by: David Roger <droger@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Auto-Submit: Yann Dago <ydago@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#824482}

[modify] https://crrev.com/0915ac94ccd5d05266009907215e94a8aab1baad/content/browser/webrtc/webrtc_internals.cc


### yd...@chromium.org (2020-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-09)

Requesting merge to beta M87 because latest trunk commit (824482) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-09)

This bug requires manual review: We are only 7 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2020-11-09)

ydago@-  please complete the merge questionnaire to consider this merge.

+adetaylor@ for visibility

### yd...@chromium.org (2020-11-09)

1. Yes
2. https://crrev.com/c/2508229
3. Verified on canary
4. No
5. Bug reported by a user
6. No
7. N/A

### la...@google.com (2020-11-09)

merge approved for M87 branch 4280

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/47bb45d3451f2d754ccbfe2538b89de2375a47d0

commit 47bb45d3451f2d754ccbfe2538b89de2375a47d0
Author: Yann Dago <ydago@chromium.org>
Date: Mon Nov 09 22:48:43 2020

Enforce AllowFileSelectionDialogs on chrome://webrtc-internals/

(cherry picked from commit 0915ac94ccd5d05266009907215e94a8aab1baad)

Bug: 1137362
Change-Id: I41c4d316f614358ecb53a81f08216e00d0146081
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508229
Reviewed-by: David Roger <droger@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Auto-Submit: Yann Dago <ydago@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#824482}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2527623
Reviewed-by: Yann Dago <ydago@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1269}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/47bb45d3451f2d754ccbfe2538b89de2375a47d0/content/browser/webrtc/webrtc_internals.cc


### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-18)

The VRP panel has decided to award $500 for this bug. Thanks!

### ad...@google.com (2020-11-19)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fa1e312f96c5d1bf70b6746d248daf8f9a4a3975

commit fa1e312f96c5d1bf70b6746d248daf8f9a4a3975
Author: Yann Dago <ydago@chromium.org>
Date: Wed Dec 16 18:42:09 2020

Enforce AllowFileSelectionDialogs on chrome://webrtc-internals/

(cherry picked from commit 0915ac94ccd5d05266009907215e94a8aab1baad)

Bug: 1137362
Change-Id: I41c4d316f614358ecb53a81f08216e00d0146081
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508229
Reviewed-by: David Roger <droger@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Auto-Submit: Yann Dago <ydago@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#824482}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587031
Reviewed-by: Yann Dago <ydago@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1488}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/fa1e312f96c5d1bf70b6746d248daf8f9a4a3975/content/browser/webrtc/webrtc_internals.cc


### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1137362?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053555)*
