# Security: HeapOverflow in TabStripModel

| Field | Value |
|-------|-------|
| **Issue ID** | [40054381](https://issues.chromium.org/issues/40054381) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2021-01-07 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

Each tab\_strip has a |contents\_data\_|[1] vector to store the WebContentsData of each tab.  

We now have 6 tabs from 0 to 5 and group them:  

Group\_A : 0,1  

Group\_B : 2,3,4,5

The |contents\_data\_| is as follows:  

contents\_data\_[0]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  

contents\_data\_[1]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  

contents\_data\_[2]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

contents\_data\_[3]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

contents\_data\_[4]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

contents\_data\_[5]->groupId = B004FCD893432A3D4B1EFA56C875ABFC

Then we select 1, 2, 3, 5 and move them. |MoveSelectedTabsTo()|[2] will renumber them as 2, 3, 4, 5 and exchange their WebContentsData.

Now the |contents\_data\_| is as follows:  

contents\_data\_[0]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  

contents\_data\_[1]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

contents\_data\_[2]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  

contents\_data\_[3]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

contents\_data\_[4]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

contents\_data\_[5]->groupId = B004FCD893432A3D4B1EFA56C875ABFC

Then these four tabs will be regrouped by |UpdateGroupForDraggedTabs()|[3]. And first, they will be ungrouped[4]. |RemoveFromGroup()| will ungroup and move tabs by the group[5]. In each group, the tab will also be moved to the left or right of the group according to its position in the group. So now we have:

Group\_A  

to\_left\_of\_group : 2

Group\_B  

to\_left\_of\_group : 3  

to\_right\_of\_group : 4, 5

The processing order of the group is based on the groupId. So if Group\_B\_Id is greater than Group\_A\_Id, Group\_B will be processed first.

For example, the tab with index 3 will be processed as follows:  

TabStripModel::MoveAndSetGroup[6] index : 3 new\_index : 1

```
1. Ungroup(3) =>  
	contents_data_[0]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  
	contents_data_[1]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  
	contents_data_[2]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  
	contents_data_[3]->groupId = null  
	contents_data_[4]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  
	contents_data_[5]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

2. if (index != new_index) => |MoveWebContentsAtImpl()| => |contents_data_[3]| will be inserted[7] before |contents_data_[1]| =>  
	contents_data_[0]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  
	contents_data_[1]->groupId = null  
	contents_data_[2]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  
	contents_data_[3]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  
	contents_data_[4]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  
	contents_data_[5]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

```

4,5 as follows:  

TabStripModel::MoveAndSetGroup index : 5 new\_index : 5  

TabStripModel::MoveAndSetGroup index : 4 new\_index : 4  

=>  

contents\_data\_[0]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  

contents\_data\_[1]->groupId = null  

contents\_data\_[2]->groupId = B004FCD893432A3D4B1EFA56C875ABFC  

contents\_data\_[3]->groupId = D03012E9FB65AC8D2ED44972B7A2110C  

contents\_data\_[4]->groupId = null  

contents\_data\_[5]->groupId = null

Then process Group\_A:  

TabStripModel::MoveAndSetGroup index : 2 new\_index : 0

```
Ungroup(2) (\*\*\*Wrong!!\*\*\* |contents_data_[2]| has become |contents_data_[3]|)  

The |tab_count_| of the group whose groupId is B004FCD893432A3D4B1EFA56C875ABFC has been reduced to 0. This group will be erased[8] from groups_.  

```

Then |MoveTabsAndSetGroup()|[9] will access |updated\_group|(B004FCD893432A3D4B1EFA56C875ABFC) through |GetTabGroup()|[10].

=> groups\_.find(id)->second => groups\_.end()->second => OOB!

A very clever bug :P

Asan may throw it out as UAF.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/tab_strip_model.h;l=766;drc=9b9dd00a6e792b0ac4dd671f0353472140be9398>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.cc;l=1034;drc=709f0a2016e693f06dea4a935684fe9d78277d7c>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.cc;l=1039;drc=709f0a2016e693f06dea4a935684fe9d78277d7c>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.cc;l=2177;drc=709f0a2016e693f06dea4a935684fe9d78277d7c>  

[5]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/tab_strip_model.cc;l=1121;drc=709f0a2016e693f06dea4a935684fe9d78277d7c>

[6]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/tab_strip_model.cc;l=2107;drc=709f0a2016e693f06dea4a935684fe9d78277d7c>  

[7]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/tab_strip_model.cc;l=1953;drc=709f0a2016e693f06dea4a935684fe9d78277d7c>  

[8]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/tab_strip_model.cc;l=2156;drc=709f0a2016e693f06dea4a935684fe9d78277d7c>

[9].<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.cc;l=2185;drc=709f0a2016e693f06dea4a935684fe9d78277d7c>  

[10]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/tab_group_model.cc;l=42;drc=cfa76e5827628eb2104df0e0b55d5d89f4a93eaf>

**VERSION**  

Chrome Version: stable  

Operating System: Win, Linux, ChromeOS, Mac

**REPRODUCTION CASE**

1. load the extension.
2. drag the tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 21.2 KB)
- [extension_group.zip](attachments/extension_group.zip) (application/octet-stream, 1.7 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.3 MB)

## Timeline

### [Deleted User] (2021-01-07)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-01-07)

Marking this as medium severity and impact stable, feel free to correct. 
@cyan can you take a look at this or reassign to another?

[Monorail components: UI>Browser>TabStrip>TabGroups]

### le...@gmail.com (2021-01-08)

Thanks for the quick reply, but I think the severity should be high. It is the memory corruption in the browser process and only needs the tabs permission for the extension to assist trigger. Both https://crbug.com/chromium/1092308 and https://crbug.com/chromium/1138911 seem to be recognized as high-severity.

### [Deleted User] (2021-01-08)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-08)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### cy...@chromium.org (2021-01-11)

@connily is this also fixed with your change?

### co...@chromium.org (2021-01-11)

It's not fixed by the change I made, but I can probably make a similar one for the group/ungroup interaction.

Thanks for the report and the detailed repro!

### co...@chromium.org (2021-01-11)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-01-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2a52558f26ed7113bee957a64f6c07a4e9462817

commit 2a52558f26ed7113bee957a64f6c07a4e9462817
Author: Connie Wan <connily@chromium.org>
Date: Wed Jan 13 20:09:48 2021

Simplify group updates during tab dragging

This makes it so that TabDragController::UpdateGroupForDraggedTabs does
only what its name suggests (updates the group membership of the dragged
tabs) without doing anything extra (lots of tab movement).

The assumption is that tabs are moved to their destination before
UpdateGroupForDraggedTabs is called. This assumption is commented here:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.h;l=527
And it still holds because of this call here:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.cc;l=1034

Most of the deleted movements in UpdateGroupForDraggedTabs were added
because functions like RemoveFromGroup() could potentially shift tabs
around. However, by using MoveAndSetGroup instead, the tabs don't
actually move as long as the above assumption holds.

Tested manually and via interactive UI tests:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller_interactive_uitest.cc;l=698

Bug: 1163845
Change-Id: I447c66a10c26a20a10d08979cd47cee4906d9b71
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2622324
Reviewed-by: Charlene Yan <cyan@chromium.org>
Commit-Queue: Connie Wan <connily@chromium.org>
Cr-Commit-Position: refs/heads/master@{#843162}

[modify] https://crrev.com/2a52558f26ed7113bee957a64f6c07a4e9462817/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/2a52558f26ed7113bee957a64f6c07a4e9462817/chrome/browser/ui/tabs/tab_strip_model.h
[modify] https://crrev.com/2a52558f26ed7113bee957a64f6c07a4e9462817/chrome/browser/ui/tabs/tab_strip_model.cc


### co...@chromium.org (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

Requesting merge to beta M88 because latest trunk commit (843162) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-15)

This bug requires manual review: We are only 3 days from stable.
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-01-15)

1. Yes, since this was automatically slated for merge as a security bug.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2622324
3. Yes.
4. No.
5. Since it's a medium-level security issue it was automatically slated for merge.
6. No.
7. No.

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-26)

(Note to self: landed before M89 branch).

### ad...@google.com (2021-01-27)

I think I agree that this is High severity. It's a browser process crash, so by default is Critical. It's mitigated by the need for an extension and for UI gestures, but I still think that mitigates it down to just High.

bdea@ is that OK with you? Or did you have other rationales for your Medium choice?

Approving merge to M88, branch 4324.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/658b2dc6d1998d2656e236680c3af630449c5a53

commit 658b2dc6d1998d2656e236680c3af630449c5a53
Author: Connie Wan <connily@chromium.org>
Date: Wed Jan 27 20:22:48 2021

Simplify group updates during tab dragging (merge)

This makes it so that TabDragController::UpdateGroupForDraggedTabs does
only what its name suggests (updates the group membership of the dragged
tabs) without doing anything extra (lots of tab movement).

The assumption is that tabs are moved to their destination before
UpdateGroupForDraggedTabs is called. This assumption is commented here:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.h;l=527
And it still holds because of this call here:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.cc;l=1034

Most of the deleted movements in UpdateGroupForDraggedTabs were added
because functions like RemoveFromGroup() could potentially shift tabs
around. However, by using MoveAndSetGroup instead, the tabs don't
actually move as long as the above assumption holds.

Tested manually and via interactive UI tests:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller_interactive_uitest.cc;l=698

(cherry picked from commit 2a52558f26ed7113bee957a64f6c07a4e9462817)

Bug: 1163845
Change-Id: I447c66a10c26a20a10d08979cd47cee4906d9b71
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2622324
Reviewed-by: Charlene Yan <cyan@chromium.org>
Commit-Queue: Connie Wan <connily@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#843162}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2653277
Cr-Commit-Position: refs/branch-heads/4324@{#2030}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/658b2dc6d1998d2656e236680c3af630449c5a53/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/658b2dc6d1998d2656e236680c3af630449c5a53/chrome/browser/ui/tabs/tab_strip_model.h
[modify] https://crrev.com/658b2dc6d1998d2656e236680c3af630449c5a53/chrome/browser/ui/tabs/tab_strip_model.cc


### am...@google.com (2021-01-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-28)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to reward you $10,000 for this report. Nice work! 

### am...@google.com (2021-01-28)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-31)

[Empty comment from Monorail migration]

### as...@google.com (2021-02-02)

[Empty comment from Monorail migration]

### as...@google.com (2021-02-02)

Marking as not applicable for LTS since introducing code landed in M88.
connily@ please, confirm.

### co...@chromium.org (2021-02-02)

Yes I believe this should just be targeting M88. Thanks!

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1163845?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054381)*
