# [ozone/wayland]use-after-free in WaylandWindow

| Field | Value |
|-------|-------|
| **Issue ID** | [40057854](https://issues.chromium.org/issues/40057854) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Ozone, UI>Browser>TopChrome>TabStrip |
| **Platforms** | Linux |
| **Reporter** | ro...@gmail.com |
| **Assignee** | ni...@igalia.com |
| **Created** | 2021-11-08 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36

Steps to reproduce the problem:
[note] first step and the flag in second step is not need in LaCros. See crbug.com/1169446. This bug could be triggered without any flag in LaCros.
1、enable wayland in linux
2、out/asan/chrome --enable-features=UseOzonePlatform --ozone-platform=wayland "http://localhost:8000/a.html"
3、open incognito window
4、drag the a.html tab and wait for the crash.

What is the expected behavior?

What went wrong?
WaylandWindowDragController::Drag[1] will call RunLoop[2] and Runloop will run a nested message loop in [3].If recent window is closed in the nested message loop. Then HandleDropAndResetState[4] will be called and UAF will be triggered in [5] 

bool WaylandWindowDragController::Drag(WaylandToplevelWindow* window,
                                       const gfx::Vector2d& offset) -----[1]{
  DCHECK_GE(state_, State::kAttached);
  DCHECK(window);

  SetDraggedWindow(window, offset);
  state_ = State::kDetached;
  RunLoop(); ------[2]
  SetDraggedWindow(nullptr, {});

  DCHECK(state_ == State::kAttaching || state_ == State::kDropped);
  if (state_ == State::kAttaching) {
    state_ = State::kAttached;
    return false;
  }

  HandleDropAndResetState();  ----------[4]
  return true;
}

https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_window_drag_controller.cc;l=465;drc=62a5d7e08ae7c4e1010b9abe091b967e16a7e259 [3]
https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_window.cc;l=179?q=ui::WaylandWindow::SetPointerFocus&ss=chromium%2Fchromium%2Fsrc [5]

Did this work before? N/A 

Chrome version: 95.0.4638.69  Channel: stable
OS Version:

## Attachments

- [a.html](attachments/a.html) (text/plain, 67 B)
- [asan.log](attachments/asan.log) (text/plain, 13.4 KB)
- [a1.mp4](attachments/a1.mp4) (video/mp4, 733.8 KB)

## Timeline

### [Deleted User] (2021-11-08)

[Empty comment from Monorail migration]

### ro...@gmail.com (2021-11-08)

[Comment Deleted]

### ts...@chromium.org (2021-11-09)

tbergquist - ptal as you've fixed similar bugs in the past, or re-assign as appropriate.
Setting severity high as it is mitigate by gestures.

[Monorail components: UI>Browser>TopChrome>TabStrip]

### [Deleted User] (2021-11-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ro...@gmail.com (2021-11-16)

Friendly ping. Is there any update? Thanks.

### [Deleted User] (2021-11-22)

tbergquist: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-11-23)

nickdiego: Can you please take a look at this?

### ni...@igalia.com (2021-11-24)

On it.
Thanks

[Monorail components: Internals>Ozone]

### ni...@igalia.com (2021-11-24)

WIP CL at https://chromium-review.googlesource.com/c/chromium/src/+/3300755

Interestingly, it does not repro on devel builds, unless I do some tweaks in drag_controller code. Anyways the above patch should fix it. Will do a few more tests before landing it. thanks

### ro...@gmail.com (2021-11-25)

[Comment Deleted]

### ro...@gmail.com (2021-11-25)

https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_window_drag_controller.cc;l=431;drc=de68be3f18ba99cc01d75903e167ca09bade253c?q=wayland_window_drag [1]


### ni...@igalia.com (2021-11-25)

> But in debug build it will hit a DCHECK in [1].

Do you mean it fails to "DCHECK(drag_source_)" ? That's what in that line with my patch applied IIUC.

> No structs has been sprayed to the heap's freed zone when the uaf write happens and the uaf write bug don't destroy the heap flags) but attacker could spray some structs to use this bug to modify the structs field like size for furture exploit.

Ack, thanks for the explanation.

### ro...@gmail.com (2021-11-25)

Oh, I’m sorry for not patch it patiently in my local build. Now in my test it works well. Thank you!

### ni...@igalia.com (2021-11-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7280aa30a74b434c714190479cd02c31a064c4e5

commit 7280aa30a74b434c714190479cd02c31a064c4e5
Author: Nick Diego Yamane <nickdiego@igalia.com>
Date: Thu Nov 25 17:00:28 2021

wayland: tabdrag: fix UAF when the dragged window is destroyed

While in a tab drag session, in detached mode, the browser window being
dragged may get suddenly destroyed, eg: programmatically via JS, which
currently may lead to use-after-free issues, such as the one described
in the linked issue. This fixes it by properly handling the dragged
window destruction after quitting the drag loop.

R=msisov@igalia.com

Bug: 1267791
Change-Id: I22c9b2a8fa06d7d5b50cefae72b24dbd4931f60d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3300755
Commit-Queue: Nick Yamane <nickdiego@igalia.com>
Reviewed-by: Alexander Dunaev <adunaev@igalia.com>
Cr-Commit-Position: refs/heads/main@{#945424}

[modify] https://crrev.com/7280aa30a74b434c714190479cd02c31a064c4e5/ui/ozone/platform/wayland/host/wayland_window_drag_controller.h
[modify] https://crrev.com/7280aa30a74b434c714190479cd02c31a064c4e5/ui/ozone/platform/wayland/host/wayland_window_drag_controller.cc
[modify] https://crrev.com/7280aa30a74b434c714190479cd02c31a064c4e5/ui/ozone/platform/wayland/host/wayland_window_drag_controller_unittest.cc


### ni...@igalia.com (2021-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-26)

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

### [Deleted User] (2021-11-26)

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

### [Deleted User] (2021-11-26)

[Empty comment from Monorail migration]

### ni...@igalia.com (2021-11-26)

1. It fixes a security issue (heap use-after-free). Fix is small and self-contained.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3300755
3. Yes. See https://crbug.com/chromium/1267791#c17.
4. No.
6. No.

### am...@chromium.org (2021-11-29)

merge approved to M97; please merge to branch 4692 ASAP so this fix can be included in tomorrow's beta cut 
merge approved to M96, please merge to branch 4664 by EOD Friday so this fix can be included in next week's stable channel refresh - thanks! 

### gi...@appspot.gserviceaccount.com (2021-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0d29c13044025b2a05aa09c67fe847a77899e7c3

commit 0d29c13044025b2a05aa09c67fe847a77899e7c3
Author: Nick Diego Yamane <nickdiego@igalia.com>
Date: Mon Nov 29 22:49:30 2021

[Merge to M97] wayland: tabdrag: fix UAF when the dragged window is destroyed

While in a tab drag session, in detached mode, the browser window being
dragged may get suddenly destroyed, eg: programmatically via JS, which
currently may lead to use-after-free issues, such as the one described
in the linked issue. This fixes it by properly handling the dragged
window destruction after quitting the drag loop.

R=​msisov@igalia.com

(cherry picked from commit 7280aa30a74b434c714190479cd02c31a064c4e5)

Bug: 1267791
Change-Id: I22c9b2a8fa06d7d5b50cefae72b24dbd4931f60d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3300755
Commit-Queue: Nick Yamane <nickdiego@igalia.com>
Reviewed-by: Alexander Dunaev <adunaev@igalia.com>
Cr-Original-Commit-Position: refs/heads/main@{#945424}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3304118
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Nick Yamane <nickdiego@igalia.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4692@{#548}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/0d29c13044025b2a05aa09c67fe847a77899e7c3/ui/ozone/platform/wayland/host/wayland_window_drag_controller.h
[modify] https://crrev.com/0d29c13044025b2a05aa09c67fe847a77899e7c3/ui/ozone/platform/wayland/host/wayland_window_drag_controller.cc
[modify] https://crrev.com/0d29c13044025b2a05aa09c67fe847a77899e7c3/ui/ozone/platform/wayland/host/wayland_window_drag_controller_unittest.cc


### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/94ca87ec7c634157e3e9815ad87d8f5fdd7319bb

commit 94ca87ec7c634157e3e9815ad87d8f5fdd7319bb
Author: Nick Diego Yamane <nickdiego@igalia.com>
Date: Tue Nov 30 00:18:35 2021

[Merge to M96] wayland: tabdrag: fix UAF when the dragged window is destroyed

While in a tab drag session, in detached mode, the browser window being
dragged may get suddenly destroyed, eg: programmatically via JS, which
currently may lead to use-after-free issues, such as the one described
in the linked issue. This fixes it by properly handling the dragged
window destruction after quitting the drag loop.

R=​msisov@igalia.com

(cherry picked from commit 7280aa30a74b434c714190479cd02c31a064c4e5)

Bug: 1267791
Change-Id: I22c9b2a8fa06d7d5b50cefae72b24dbd4931f60d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3300755
Commit-Queue: Nick Yamane <nickdiego@igalia.com>
Reviewed-by: Alexander Dunaev <adunaev@igalia.com>
Cr-Original-Commit-Position: refs/heads/main@{#945424}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3304119
Auto-Submit: Nick Yamane <nickdiego@igalia.com>
Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1179}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/94ca87ec7c634157e3e9815ad87d8f5fdd7319bb/ui/ozone/platform/wayland/host/wayland_window_drag_controller.cc
[modify] https://crrev.com/94ca87ec7c634157e3e9815ad87d8f5fdd7319bb/ui/ozone/platform/wayland/host/wayland_window_drag_controller.h
[modify] https://crrev.com/94ca87ec7c634157e3e9815ad87d8f5fdd7319bb/ui/ozone/platform/wayland/host/wayland_window_drag_controller_unittest.cc


### am...@google.com (2021-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-01)

Congratulations, Rox! The VRP Panel has decided to award you $10,000 for this report. Thank you for efforts and nice work! 

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1267791?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Ozone, UI>Browser>TopChrome>TabStrip]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057854)*
