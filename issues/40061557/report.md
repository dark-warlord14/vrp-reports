# Security: heap-use-after-free ui/views/view.cc:1921:7 in views::View::HandleAccessibleAction

| Field | Value |
|-------|-------|
| **Issue ID** | [40061557](https://issues.chromium.org/issues/40061557) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2022-11-02 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. Enable touch screen & chromevox
2. Open NTP
3. alt+tab then double click on views (please refer to screencast)

**Problem Description:**  

Copied from <https://bugs.chromium.org/p/chromium/issues/detail?id=1355560#c25>, the CL in <https://bugs.chromium.org/p/chromium/issues/detail?id=1355560#c11> (<https://chromium-review.googlesource.com/c/chromium/src/+/3868127>) is not complete fix the UaF issue. I had comment two times on issue #1355560 but it seems the thread was not monitored after status set to fixed. So I open new report for security to able track the new issue.

\*It is okay if this issue merge to the old issue #1355560(reopen), since the reward have been given and CVE have been submitted.  

\*I also had reported same pattern for this UaF issue on #1350561 but it seems the owner is not correct and has not been fixed, it's okay if can merge.

**Additional Comments:**

\*\*Chrome version: \*\* 109 \*\*Channel: \*\* Dev

**OS:** Chrome OS

## Attachments

- [screencast_00022.webm](attachments/screencast_00022.webm) (video/webm, 6.9 MB)
- [1355560-M109.log](attachments/1355560-M109.log) (text/plain, 18.8 KB)

## Timeline

### rh...@gmail.com (2022-11-02)

another same pattern UaF goes to issue #1350561

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-11-02)

[Empty comment from Monorail migration]

[Monorail components: UI>Accessibility]

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-03)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-16)

dtseng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2022-11-22)

This looks like a views usage pattern issue.
Namely,

WindowCycleItemView

deletes itself when it gets a mouse press through

    #17 0x560338196de7 in views::View::HandleAccessibleAction(ui::AXActionData const&) ui/views/view.cc:1917:7

(context call stack below)
    #12 0x560333f475e8 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:281:7
    #13 0x560333f475e8 in ash::WindowCycleController::StopCycling() ash/wm/window_cycle/window_cycle_controller.cc:421:22
    #14 0x560333f5944c in ash::WindowCycleItemView::OnMousePressed(ui::MouseEvent const&) ash/wm/window_cycle/window_cycle_item_view.cc:53:44
    #15 0x560338193ae2 in views::View::ProcessMousePressed(ui::MouseEvent const&) ui/views/view.cc:3109:23
    #16 0x56033819362d in views::View::OnMouseEvent(ui::MouseEvent*) ui/views/view.cc:1492:11
    #17 0x560338196de7 in views::View::HandleAccessibleAction(ui::AXActionData const&) ui/views/view.cc:1917:7

Then,

    #0 0x56033819714e in views::View::HandleAccessibleAction(ui::AXActionData const&) ui/views/view.cc:1921:7

UAFs on the deleted view. This line attempts to dispatch a mouse release event on the deleted view.

Ideally, views don't delete themselves when pressed or defer deletion until the next callstack.

Assigning to robliao for his take. Should this be fixed by Ash/WindowCycleItemView owners?

In terms of priority/time/duplication:
Agreed, if this was the *issue* being filed, then the original issue was fixing something else and this or the original could be dupped against one another.
In terms of milestones, this views code is several years old, maybe even a decade, so targeting any particular milestone doesn't make sense.

### gi...@appspot.gserviceaccount.com (2022-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/40f5180b4f560308a22fb5292da280dede1513d2

commit 40f5180b4f560308a22fb5292da280dede1513d2
Author: David Tseng <dtseng@google.com>
Date: Tue Nov 29 03:56:11 2022

views-a11y: workaround self-deleting views on mouse press

In View::HandleAccessibleAction, accessibility sends both a press and
release mouse event to the view instance.

Unfortunately, if the view deletes itself immediately after receiving
the mouse press event, the subsequent mouse release event causes a UAF.

e.g. for illustrative purposes, here's the flow:

bool HandleAccessibleAction(...) {
  view->OnEvent(mouse_press);
  // |view| is now deleted.
  view->OnEvent(mouse_release);
  // UAF.
}

Fix this by overriding HandleAccessibleAction in the self-deleting view.

Notes:
The deletion stack for the WindowCycleItemView is
    #3 0x560338183db8 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49:5
    #4 0x560338183db8 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:281:7
    #5 0x560338183db8 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:247:75
    #6 0x560338183db8 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) ui/views/view.cc:2739:1
    #7 0x560338183fe4 in views::View::RemoveAllChildViews() ui/views/view.cc:341:5
    #8 0x560333f50cbb in ash::WindowCycleView::DestroyContents() ash/wm/window_cycle/window_cycle_view.cc:379:3
    #9 0x560333f4b3e7 in ash::WindowCycleList::~WindowCycleList() ash/wm/window_cycle/window_cycle_list.cc:139:18
    #10 0x560333f4b747 in ash::WindowCycleList::~WindowCycleList() ash/wm/window_cycle/window_cycle_list.cc:117:37
    #11 0x560333f475e8 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49:5
    #12 0x560333f475e8 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:281:7
    #13 0x560333f475e8 in ash::WindowCycleController::StopCycling() ash/wm/window_cycle/window_cycle_controller.cc:421:22
    #14 0x560333f5944c in ash::WindowCycleItemView::OnMousePressed(ui::MouseEvent const&) ash/wm/window_cycle/window_cycle_item_view.cc:53:44
    #15 0x560338193ae2 in views::View::ProcessMousePressed(ui::MouseEvent const&) ui/views/view.cc:3109:23
    #16 0x56033819362d in views::View::OnMouseEvent(ui::MouseEvent*) ui/views/view.cc:1492:11

Bug: 1380602
Change-Id: I2533dc299c0f5f5bb32efa130e6d564cb70d4613
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4046647
Commit-Queue: David Tseng <dtseng@chromium.org>
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1076637}

[modify] https://crrev.com/40f5180b4f560308a22fb5292da280dede1513d2/ash/wm/window_cycle/window_cycle_item_view.cc
[modify] https://crrev.com/40f5180b4f560308a22fb5292da280dede1513d2/ash/wm/window_cycle/window_cycle_item_view.h


### dt...@chromium.org (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

Requesting merge to dev M109 because latest trunk commit (1076637) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

Merge review required: M109 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-11-30)

Approved, M109.

Category: Security fix

### ma...@google.com (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations, Rheza! The VRP Panel has decided to award you $2,000 for this report of this highly mitigated security bug. Thank you for taking the time to test the original fix and reporting that this issue is still reproducible to us -- nice work! 

### rh...@gmail.com (2022-12-09)

Thank you Amy(security team) and developers as well. 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1380602?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ni...@google.com (2024-06-18)

Marking verified per comment 13

### pe...@google.com (2024-10-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061557)*
