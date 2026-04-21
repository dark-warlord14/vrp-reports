# Security: use-after-free in WindowTreeHostPlatform::OnBoundsChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40055088](https://issues.chromium.org/issues/40055088) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Aura |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | ev...@foutras.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2021-03-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

I originally reported this as <https://crbug.com/chromium/1184628>, after observing several crashes of my custom-built Chromium (linked to system libstdc++). The crash occurs while dragging a tab around, detaching and reattaching repeatedly. The `--start-maximized` flag makes it quite easy to reproduce. Further investigation with an ASan-enabled build reveals a use-after-free bug in WindowTreeHostPlatform::OnBoundsChanged.

The same ASan report is reproducible with libc++ (which is what Chrome uses), even though a crash isn't readily observed. This might be due to differences in how libc++ and libstdc++ handle object destruction or memory allocation. Based on the reproducibility of the ASan report with libc++, I decided to follow up my original normal issue with this security one.

**VERSION**  

Chrome Version: 89.0.4389.82 stable  

Operating System: Arch Linux (rolling) with Xfce 4.16 and display compositing disabled

**REPRODUCTION CASE**

1. Build Chrome with "is\_asan=true is\_debug=false" and start it with --start-maximized
2. Drag a tab around, repeatedly detaching and reattaching (as shown in the attached video)
3. ASan should abort with a heap-use-after-free in WindowTreeHostPlatform::OnBoundsChanged

If it proves difficult to reproduce, the ASan report might provide enough context to spot the cause.

Type of crash: browser  

Crash State: see attached ASan report (libcxx-tab-drag-heap-use-after-free.txt)

**CREDIT INFORMATION**  

Reporter credit: Evangelos Foutras [evangelos@foutrelis.com](mailto:evangelos@foutrelis.com)

## Attachments

- [libcxx-tab-drag-heap-use-after-free.txt](attachments/libcxx-tab-drag-heap-use-after-free.txt) (text/plain, 10.9 KB)
- [tab-move-crash.mp4](attachments/tab-move-crash.mp4) (video/mp4, 1.7 MB)

## Timeline

### [Deleted User] (2021-03-06)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-03-08)

Thanks for the report. Should we merge https://crbug.com/chromium/1184628 into here?

+ui/aura owners: can you investigate this issue?

[Monorail components: UI>Aura]

### ev...@foutras.com (2021-03-08)

Merging https://crbug.com/chromium/1184628 into this seems good.

### [Deleted User] (2021-03-08)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### th...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5e3a738b1204941aab9f15c0eb3d06e20fefd96e

commit 5e3a738b1204941aab9f15c0eb3d06e20fefd96e
Author: Scott Violet <sky@chromium.org>
Date: Mon Mar 08 21:07:39 2021

x11/ozone: fix two edge cases

WindowTreeHost::OnHostMovedInPixels() may trigger a nested message
loop (tab dragging), which when the stack unravels means this may
be deleted. This adds an early out if this happens.

X11WholeScreenMoveLoop has a similar issue, in so far as notifying
the delegate may delete this.

BUG=1185482
TEST=WindowTreeHostPlatform.DeleteHostFromOnHostMovedInPixels

Change-Id: Ieca1c90b3e4358da50b332abe2941fdbb50c5c25
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2743555
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/master@{#860852}

[modify] https://crrev.com/5e3a738b1204941aab9f15c0eb3d06e20fefd96e/ui/aura/window_tree_host_platform.cc
[modify] https://crrev.com/5e3a738b1204941aab9f15c0eb3d06e20fefd96e/ui/aura/window_tree_host_platform_unittest.cc
[modify] https://crrev.com/5e3a738b1204941aab9f15c0eb3d06e20fefd96e/ui/base/x/x11_whole_screen_move_loop.cc


### sk...@chromium.org (2021-03-08)

As reproducing this requires user interaction, and is not at all straightforward (meaning you have to do work at it) I'm not going to request a merge.

### ev...@foutras.com (2021-03-08)

Thanks for the fix! For what is worth, I briefly mentioned in https://crbug.com/chromium/1184628 (https://crbug.com/chromium/1185482#c1) that the crash occurs during regular use too. It's very infrequent though, possibly requiring `--start-maximized` and/or Chromium built against libstdc++ to manifest. While the ASan report shows it's reproducible with libc++ too, if you haven't seen any crash reports about this then Chrome is probably safe. :)

Also confirming that the fix appears to work for my custom Chromium 89 build; it no longer crashes when moving tabs around.

### ev...@foutras.com (2021-03-09)

I wish to amend my previous statement that "Chrome is probably safe"; I was thinking in terms of crashing, but the use-after-free can very well exist in Chrome too (based on the ASan report with libc++). I don't feel that a use-after-free could be considered safe just because it's not visibly affecting Chrome (and Chromium linked against libc++), when libstdc++ builds infrequently crash during regular use (with the same backtrace).

Anyway, I just wanted to correct my previous comment. I'm sure you can assess the severity and impact of the bug much better than me.

### sk...@chromium.org (2021-03-09)

IMO, a merge to 90 is reasonable. As 89 has already shipped it's a bit risky to attempt a merge to 89.

### sk...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-10)

Your change meets the bar and is auto-approved for M90. Please go ahead and merge the CL to branch 4430 (refs/branch-heads/4430) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e798599632a2e376c405e4488776e637e6de79e3

commit e798599632a2e376c405e4488776e637e6de79e3
Author: Scott Violet <sky@chromium.org>
Date: Wed Mar 10 20:30:16 2021

[M90] x11/ozone: fix two edge cases

WindowTreeHost::OnHostMovedInPixels() may trigger a nested message
loop (tab dragging), which when the stack unravels means this may
be deleted. This adds an early out if this happens.

X11WholeScreenMoveLoop has a similar issue, in so far as notifying
the delegate may delete this.

BUG=1185482
TEST=WindowTreeHostPlatform.DeleteHostFromOnHostMovedInPixels

(cherry picked from commit 5e3a738b1204941aab9f15c0eb3d06e20fefd96e)

Change-Id: Ieca1c90b3e4358da50b332abe2941fdbb50c5c25
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2743555
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#860852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2749355
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#318}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/e798599632a2e376c405e4488776e637e6de79e3/ui/aura/window_tree_host_platform.cc
[modify] https://crrev.com/e798599632a2e376c405e4488776e637e6de79e3/ui/aura/window_tree_host_platform_unittest.cc
[modify] https://crrev.com/e798599632a2e376c405e4488776e637e6de79e3/ui/base/x/x11_whole_screen_move_loop.cc


### ad...@google.com (2021-03-10)

sky@ we normally merge high severity security bug fixes back to stable, because we have adversaries who weaponize our git commits in a small number of days. UaFs in the browser process are critical severity but this is mitigated to High by virtue of the fact it requires user action. In practice I think the level of user interaction is pretty darned high, so I'm not hugely vocal about the need to ship this in an M89 refresh, but that would be our normal practice. Do you have specific stability concerns about this fix? Re-adding Merge-Request-89 for consideration.

### [Deleted User] (2021-03-10)

This bug requires manual review: Request affecting a post-stable build
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-03-17)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-18)

Note for VRP, CVE and release note purposes: https://crbug.com/chromium/1179635 is believed to be an earlier report of the same issue. The duplication has happened in the inverse direction because discussion has already occurred here.

### ev...@foutras.com (2021-03-18)

Is it possible for me to view https://crbug.com/chromium/1179635? (Out of curiosity.)

### [Deleted User] (2021-03-18)

The older reward-topanel https://crbug.com/chromium/1179635 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### [Deleted User] (2021-03-19)

The older reward-topanel https://crbug.com/chromium/1179635 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### am...@chromium.org (2021-03-22)

updating labels so correct bug (https://crbug.com/chromium/1179635) is pulled into this week's VRP panel docket 

### ad...@google.com (2021-03-23)

sky@ ping re https://crbug.com/chromium/1185482#c17. We're starting to get ready for the next round of M89 merges.

### sk...@chromium.org (2021-03-23)

I don't have any specific concerns about merging to 89. I'll request it now.

### ad...@google.com (2021-03-23)

Thanks. In that case, approving merge for M89, branch 4389.

### ad...@google.com (2021-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-23)

The older reward-topanel https://crbug.com/chromium/1179635 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### gi...@appspot.gserviceaccount.com (2021-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ad84a8e7882275fb32f938fd0adc04d1a2a5773

commit 8ad84a8e7882275fb32f938fd0adc04d1a2a5773
Author: Scott Violet <sky@chromium.org>
Date: Tue Mar 23 18:47:22 2021

[M89 merge] x11/ozone: fix two edge cases

WindowTreeHost::OnHostMovedInPixels() may trigger a nested message
loop (tab dragging), which when the stack unravels means this may
be deleted. This adds an early out if this happens.

X11WholeScreenMoveLoop has a similar issue, in so far as notifying
the delegate may delete this.

BUG=1185482
TEST=WindowTreeHostPlatform.DeleteHostFromOnHostMovedInPixels

(cherry picked from commit 5e3a738b1204941aab9f15c0eb3d06e20fefd96e)

Change-Id: Ieca1c90b3e4358da50b332abe2941fdbb50c5c25
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2743555
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#860852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2779886
Cr-Commit-Position: refs/branch-heads/4389@{#1583}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/8ad84a8e7882275fb32f938fd0adc04d1a2a5773/ui/aura/window_tree_host_platform.cc
[modify] https://crrev.com/8ad84a8e7882275fb32f938fd0adc04d1a2a5773/ui/aura/window_tree_host_platform_unittest.cc
[modify] https://crrev.com/8ad84a8e7882275fb32f938fd0adc04d1a2a5773/ui/base/x/x11_whole_screen_move_loop.cc


### ad...@google.com (2021-03-24)

Note for myself and Amy when preparing release notes: consider https://crbug.com/chromium/1179635.

### ad...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-03-29)

[Empty comment from Monorail migration]

### as...@google.com (2021-03-30)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-03-30)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-03-30)

Merge approved for LTS-86

### gi...@appspot.gserviceaccount.com (2021-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8c3eb9d1c4095ff42184f1e5261e6e5e704672dd

commit 8c3eb9d1c4095ff42184f1e5261e6e5e704672dd
Author: Scott Violet <sky@chromium.org>
Date: Wed Mar 31 13:28:05 2021

[M86-LTS merge] x11/ozone: fix two edge cases

WindowTreeHost::OnHostMovedInPixels() may trigger a nested message
loop (tab dragging), which when the stack unravels means this may
be deleted. This adds an early out if this happens.

X11WholeScreenMoveLoop has a similar issue, in so far as notifying
the delegate may delete this.

BUG=1185482
TEST=WindowTreeHostPlatform.DeleteHostFromOnHostMovedInPixels

(cherry picked from commit 5e3a738b1204941aab9f15c0eb3d06e20fefd96e)

(cherry picked from commit 8ad84a8e7882275fb32f938fd0adc04d1a2a5773)

Change-Id: Ieca1c90b3e4358da50b332abe2941fdbb50c5c25
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2743555
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#860852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2779886
Cr-Original-Commit-Position: refs/branch-heads/4389@{#1583}
Cr-Original-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2794391
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1583}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/8c3eb9d1c4095ff42184f1e5261e6e5e704672dd/ui/aura/window_tree_host_platform.cc
[modify] https://crrev.com/8c3eb9d1c4095ff42184f1e5261e6e5e704672dd/ui/aura/window_tree_host_platform_unittest.cc
[modify] https://crrev.com/8c3eb9d1c4095ff42184f1e5261e6e5e704672dd/ui/base/x/x11_whole_screen_move_loop.cc


### as...@google.com (2021-03-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-31)

Congratulations, Evangelos! The VRP Panel has decided to award you $1000 as a thank you for your engagement on this issue and helping test the patch. A member of our finance team will be in touch soon to arrange payment. 

### ev...@foutras.com (2021-04-01)

Hi Amy. I appreciate the gesture and also thanks for mentioning me in the release notes.

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1185482?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1179635, crbug.com/chromium/1184628]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055088)*
