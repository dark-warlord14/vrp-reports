# Security: OOB read when attempting to add tab to group after groups have changed

| Field | Value |
|-------|-------|
| **Issue ID** | [40055511](https://issues.chromium.org/issues/40055511) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2021-04-10 |
| **Bounty** | $11,000.00 |

## Description

**VULNERABILITY DETAILS**  

The context menu shown for a tab allows that tab to be added to an existing group. However, if one or more groups were removed in the time since the menu was shown, an out-of-bounds read can occur in the browser process.

**VERSION**  

Chrome Version: Tested on 92.0.4474.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. Once installed, the extension will create a new window with three tabs: two that are in a group and one that's not.
3. Right-click the tab that's not in a group.
4. Five seconds after opening the window, the extension will ungroup the second tab. Once this has happened, select the final entry from the "Add tab to group" submenu. This will cause an out-of-bounds read in the browser process.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_871272.txt](attachments/asan_output_871272.txt) (text/plain, 12.7 KB)
- [background.js](attachments/background.js) (text/plain, 577 B)
- [manifest.json](attachments/manifest.json) (text/plain, 163 B)
- [suggested_patch.patch](attachments/suggested_patch.patch) (text/plain, 865 B)

## Timeline

### de...@gmail.com (2021-04-10)

The issue here is that when a group is selected from the "Add tab to group" submenu, the ExistingTabGroupSubMenuModel::ExecuteExistingCommand method retrieves a list of current groups and attempts to retrieve the selection from that:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc;l=96;drc=3f97e29466e8450418d0897f21706ffc0d1aef20

However, the tab groups may have changed since the menu was first shown. This then means that the command_index value can be out-of-bounds.

A suggested patch is attached, which simply changes the DCHECK in that method to an early return (since it doesn't make sense to continue the method if command_index is out-of-bounds).

### [Deleted User] (2021-04-10)

[Empty comment from Monorail migration]

### ct...@chromium.org (2021-04-12)

Thanks as always for the clear report (and extra for the suggested patch!).

Confirmed repro on r871272 ASAN. I can also repro on r843829 ASAN.

Passing this one to tbergquist@ as well. 


[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2021-04-13)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-04-20)

Thank you for the detailed report and suggested patch. A fix is in progress at https://chromium-review.googlesource.com/c/chromium/src/+/2841823

### gi...@appspot.gserviceaccount.com (2021-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/65b5b467c8a57ece2ec782adda098ae07d48f205

commit 65b5b467c8a57ece2ec782adda098ae07d48f205
Author: Collin Baker <collinbaker@chromium.org>
Date: Tue Apr 27 22:12:56 2021

Handle out-of-bounds group index when adding tab to existing group

Fixed: 1197875
Change-Id: I5b4749e8cec0ec1b00388f81504723acc01e4389
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2841823
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Cr-Commit-Position: refs/heads/master@{#876785}

[modify] https://crrev.com/65b5b467c8a57ece2ec782adda098ae07d48f205/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/65b5b467c8a57ece2ec782adda098ae07d48f205/chrome/browser/ui/tabs/tab_menu_model_unittest.cc


### [Deleted User] (2021-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-29)

Requesting merge to stable M90 because latest trunk commit (876785) appears to be after stable branch point (857950).

Requesting merge to beta M91 because latest trunk commit (876785) appears to be after beta branch point (870763).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-29)

This bug requires manual review: M91's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-05-03)

Approving merge to M91, branch 4472, and M90, branch 4430.

### pb...@google.com (2021-05-04)

[Bulk Edit] Your change has been approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually asap so that it would be part of tomorrow's Beta release.

### [Deleted User] (2021-05-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-05-07)

Please merge your change to M90 branch 4430 ASAP so we can pick it up for next M90 respin. Thank you.

### sr...@google.com (2021-05-07)

Marking as assigned to get attention for the pending merge

### gi...@appspot.gserviceaccount.com (2021-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e8412ccab087da5ccc5ebb8de19071cd810e8460

commit e8412ccab087da5ccc5ebb8de19071cd810e8460
Author: Collin Baker <collinbaker@chromium.org>
Date: Fri May 07 20:25:16 2021

Handle out-of-bounds group index when adding tab to existing group

(cherry picked from commit 65b5b467c8a57ece2ec782adda098ae07d48f205)

Fixed: 1197875
Change-Id: I5b4749e8cec0ec1b00388f81504723acc01e4389
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2841823
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#876785}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2880712
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1426}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/e8412ccab087da5ccc5ebb8de19071cd810e8460/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/e8412ccab087da5ccc5ebb8de19071cd810e8460/chrome/browser/ui/tabs/tab_menu_model_unittest.cc


### am...@chromium.org (2021-05-10)

[Empty comment from Monorail migration]

### vs...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### pb...@google.com (2021-05-10)

[Bulk Edit] Your change has been approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually. asap so that it would be part of this weeks Beta release.

### [Deleted User] (2021-05-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-05-11)

collinbaker@ please get the change merged to M91 Branch asap.

### gi...@appspot.gserviceaccount.com (2021-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/06bd45efd298107d2f53796287b18ae497e31646

commit 06bd45efd298107d2f53796287b18ae497e31646
Author: Collin Baker <collinbaker@chromium.org>
Date: Tue May 11 18:08:59 2021

Handle out-of-bounds group index when adding tab to existing group

(cherry picked from commit 65b5b467c8a57ece2ec782adda098ae07d48f205)

Fixed: 1197875
Change-Id: I5b4749e8cec0ec1b00388f81504723acc01e4389
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2841823
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#876785}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2888185
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Peter Boström <pbos@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#943}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/06bd45efd298107d2f53796287b18ae497e31646/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/06bd45efd298107d2f53796287b18ae497e31646/chrome/browser/ui/tabs/tab_menu_model_unittest.cc


### gi...@google.com (2021-05-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d04816608feca6e7fabea7a469b5f4b480cb354

commit 6d04816608feca6e7fabea7a469b5f4b480cb354
Author: Collin Baker <collinbaker@chromium.org>
Date: Wed May 12 16:47:24 2021

[M86-LTS]: Handle out-of-bounds group index when adding tab to existing group

[M86]: Enabled feature in test.

(cherry picked from commit 65b5b467c8a57ece2ec782adda098ae07d48f205)

(cherry picked from commit e8412ccab087da5ccc5ebb8de19071cd810e8460)

Fixed: 1197875
Change-Id: I5b4749e8cec0ec1b00388f81504723acc01e4389
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2841823
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#876785}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2880712
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4430@{#1426}
Cr-Original-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2883763
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1631}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/6d04816608feca6e7fabea7a469b5f4b480cb354/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/6d04816608feca6e7fabea7a469b5f4b480cb354/chrome/browser/ui/tabs/tab_menu_model_unittest.cc


### am...@google.com (2021-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-12)

Congratulations, David on another one! The VRP Panel has decided to award you $11,000 for this report + a patch bonus. Awesome stuff! 

### am...@google.com (2021-05-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1410f2e6927072f41424a85e64d36755b19d3d39

commit 1410f2e6927072f41424a85e64d36755b19d3d39
Author: Collin Baker <collinbaker@chromium.org>
Date: Thu May 20 10:59:16 2021

Handle out-of-bounds group index when adding tab to existing group

(cherry picked from commit 65b5b467c8a57ece2ec782adda098ae07d48f205)

(cherry picked from commit e8412ccab087da5ccc5ebb8de19071cd810e8460)

Fixed: 1197875
Change-Id: I5b4749e8cec0ec1b00388f81504723acc01e4389
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2841823
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#876785}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2880712
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4430@{#1426}
Cr-Original-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2884106
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430_101@{#53}
Cr-Branched-From: 3e9034a21f4b1f6707146b1309e001c3321ab48a-refs/branch-heads/4430@{#1364}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/1410f2e6927072f41424a85e64d36755b19d3d39/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/1410f2e6927072f41424a85e64d36755b19d3d39/chrome/browser/ui/tabs/tab_menu_model_unittest.cc


### am...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1197875?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055511)*
