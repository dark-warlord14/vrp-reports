# uaf in BookmarkBarView::OnTabGroupButtonPressed

| Field | Value |
|-------|-------|
| **Issue ID** | [40059074](https://issues.chromium.org/issues/40059074) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | dl...@chromium.org |
| **Created** | 2022-03-12 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36

Steps to reproduce the problem:
1.a
2.
3.

What is the expected behavior?

What went wrong?
a

Did this work before? N/A 

Chrome version: 99.0.4844.51  Channel: stable
OS Version: 10.0

## Attachments

- [uaf.txt](attachments/uaf.txt) (text/plain, 21.8 KB)
- [poc1.mp4](attachments/poc1.mp4) (video/mp4, 11.4 MB)
- [uaf.txt](attachments/uaf.txt) (text/plain, 23.4 KB)

## Timeline

### [Deleted User] (2022-03-12)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-03-12)

1. open one tab and save as a tab group
2. open anathor tab and save as anathor tab group
3. you can see two tab group button in your bookmark view bar
4.move one of group to anathor tab group, (just let your chrome has one tab group)
5.click the old one tab group button of bookview bar.
6. uaf occur.

### wx...@gmail.com (2022-03-12)

[Comment Deleted]

### wx...@gmail.com (2022-03-12)

my chromium commit is a20ff7247d590579a7c93cdbb2c577db30b92226

### wx...@gmail.com (2022-03-12)

[Comment Deleted]

### wx...@gmail.com (2022-03-13)

forget to say that you shoule enable "#tab-groups-save"

### bo...@chromium.org (2022-03-14)

I'm not able to reproduce this bug, although I may not be interpreting https://crbug.com/chromium/1305706#c2 correctly, so I'll pass along to the subsystem owner for a second opinion. 

If this is reachable, it would appear to require the user to perform a precise sequence of UI actions to trigger. Therefore, assigning Medium Severity as the highest possible applicable security severity level. 

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2022-03-14)

[Empty comment from Monorail migration]

### sk...@chromium.org (2022-03-15)

[Empty comment from Monorail migration]

### dl...@google.com (2022-03-15)

Thank you for the bug! This issue is currently being worked on. Will add updates here as soon I get them 👍

### dl...@chromium.org (2022-03-15)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-03-15)

wxhusst@gmail.com can you please provide more specific repro for the step
"4.move one of group to anathor tab group, (just let your chrome has one tab group)"

### dl...@chromium.org (2022-03-15)

These are the steps I did to reproduce this bug:

1. Enable the #tab-groups-save feature
2. Create 2 tab groups (Does not matter how many tabs are in them)
3. Save both tab groups 
    > You should see 2 new buttons appear in the bookmarks bar with the names of the saved tab groups.
4. Click on the first tab group that was saved
    > Will be the leftmost tab group button if the default Left to right mode is enabled.
    > Will be the right most tab group button if Right to left mode enabled.

Please let me know if there are any differences between these steps and the ones described above!

### wx...@gmail.com (2022-03-16)

I will upload a video. Sorry for my bad English 

### wx...@gmail.com (2022-03-16)

[Empty comment from Monorail migration]

### dl...@google.com (2022-03-16)

No worries! Thank you for the video, this is perfect! 

### dp...@chromium.org (2022-03-16)

we should probably go back to design and ask what we should do when there isnt any tabs in the tab group (i.e. the last tab is removed from the group, which closes the group)? there might be other issues here but we should either remove the saved tab group when there are no tabs (an invalid state for a group) or keep the last tab and just consider it a "group close" instead of removing the tab.

### [Deleted User] (2022-03-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f2d3c078ac66e0c535c357d8eeccc0d0fb795c4b

commit f2d3c078ac66e0c535c357d8eeccc0d0fb795c4b
Author: dljames <dljames@google.com>
Date: Fri Mar 18 17:27:41 2022

Fixes the use after free bug when creating multiple saved tab group buttons.

In short, we change OnTabGroupButtonPressed to take a const TabGroupID& so that when we use base::BindRepeating in CreateTabGroupButton the value is automagically copied in the call back. This prevents us from losing our saved tab group data and accessing garbage values.

More information for using const& can be found here: https://chromium.googlesource.com/chromium/src.git/+/HEAD/docs/callback.md#binding-const-reference-parameters


Bug: 1305706
Change-Id: I62a9ba403416f964dc48013ea129c44084865ded
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3533522
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Darryl James <dljames@chromium.org>
Cr-Commit-Position: refs/heads/main@{#982768}

[modify] https://crrev.com/f2d3c078ac66e0c535c357d8eeccc0d0fb795c4b/chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc
[modify] https://crrev.com/f2d3c078ac66e0c535c357d8eeccc0d0fb795c4b/chrome/browser/ui/views/bookmarks/bookmark_bar_view.h


### dl...@google.com (2022-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-19)

Requesting merge to beta M100 because latest trunk commit (982768) appears to be after beta branch point (972766).

This is sufficiently serious that it should be merged to dev. I can't currently determine details for that channel, so please assess whether this is already merged.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-21)

Merge review required: M100 is already shipping to beta.

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

### [Deleted User] (2022-03-21)

Merge approved: your change passed merge requirements and is auto-approved for M101. Please go ahead and merge the CL to branch 4951 (refs/branch-heads/4951) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: None (Android), None (iOS), None (ChromeOS), None (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/32b13d19412a9ed44d2c3892d1f75a394b84947e

commit 32b13d19412a9ed44d2c3892d1f75a394b84947e
Author: dljames <dljames@google.com>
Date: Tue Mar 22 00:21:31 2022

Fixes the use after free bug when creating multiple saved tab group buttons.

In short, we change OnTabGroupButtonPressed to take a const TabGroupID& so that when we use base::BindRepeating in CreateTabGroupButton the value is automagically copied in the call back. This prevents us from losing our saved tab group data and accessing garbage values.

More information for using const& can be found here: https://chromium.googlesource.com/chromium/src.git/+/HEAD/docs/callback.md#binding-const-reference-parameters


(cherry picked from commit f2d3c078ac66e0c535c357d8eeccc0d0fb795c4b)

Bug: 1305706
Change-Id: I62a9ba403416f964dc48013ea129c44084865ded
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3533522
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Darryl James <dljames@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#982768}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3540921
Auto-Submit: Darryl James <dljames@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4951@{#29}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/32b13d19412a9ed44d2c3892d1f75a394b84947e/chrome/browser/ui/views/bookmarks/bookmark_bar_view.h
[modify] https://crrev.com/32b13d19412a9ed44d2c3892d1f75a394b84947e/chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc


### am...@chromium.org (2022-04-04)

M100 merge approved, please merge to branch 4896 at your earliest convenience so this fix can be included in the next M100 stable refresh 

### dl...@chromium.org (2022-04-05)

No merge needed, feature was not implemented until m101 dropping merge to m100.

### am...@google.com (2022-04-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-15)

Hello, raven, and thank you for this report. Due to the highly significant amount of user interaction required to trigger this issue, the VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1305706?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059074)*
