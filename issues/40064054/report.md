#  heap-buffer-overflow in SavedTabGroup

| Field | Value |
|-------|-------|
| **Issue ID** | [40064054](https://issues.chromium.org/issues/40064054) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | xp...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2023-04-14 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

Reproducing on CANARY / DEV and slightly below.

Requires flag: Tab Groups Save / chrome://flags/#tab-groups-save

First way:

1. Boot Chrome from shutdown.
2. As soon as Chrome has booted and loaded the UI, drag the saved tab group out.
3. Drag saved tab group back over it's icon on the bookmark bar.
4. Let go of drag group over the saved-group-icon.

Second way:

1. Create a new window.
2. As soon as the new window has loaded it's UI, drag the saved tab group out.
3. Drag saved tab group back over it's icon on the bookmark bar.
4. Let go of drag group over the saved-group-icon.

**Problem Description:**  

Bug is reproducing on Dev Channel more than 7+ days ago.

Regression. Bisect will be added later today.

**Additional Comments:**

\*\*Chrome version: \*\* 114.0.5696.0 \*\*Channel: \*\* Dev

**OS:** Windows

## Attachments

- [reproduction_video_on_new_window.mp4](attachments/reproduction_video_on_new_window.mp4) (video/mp4, 2.5 MB)
- [reproduction_video_on_boot.mp4](attachments/reproduction_video_on_boot.mp4) (video/mp4, 5.7 MB)
- [asan_heap_buff.txt](attachments/asan_heap_buff.txt) (text/plain, 19.9 KB)

## Timeline

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### xp...@gmail.com (2023-04-14)

Forgot to attach ASan log. Attached on this comment.

### jd...@chromium.org (2023-04-14)

dljames@, would you mind taking a look at this one, too? Feel free to pass it off to a better owner if appropriate. Thanks!

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### ad...@google.com (2023-04-15)

(I am a bot: this is an auto-cc on a security bug)

### dp...@chromium.org (2023-04-18)

assigning to dljames@ and ccing tbergquist@ to take a look.

### dl...@chromium.org (2023-04-18)

Hey @tbergquist, when you get a chance can you look into the UAF for the dragging implementation? 

It could be the case that something in the SavedTabGroupModel is not passing data / taking ownership correctly but the drag out of window operations makes me think that it is not. 

### pg...@google.com (2023-05-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6bc26a95b47cc5d24be0949a4e8ca280766a46fb

commit 6bc26a95b47cc5d24be0949a4e8ca280766a46fb
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue May 09 23:34:37 2023

Fix crash in SavedTabGroupBar buttons drag and drop.

The drag & drop session was showing the overflow menu when its button was hovered over, even if it would be empty (and its button was not visible). This caused the drop index calculations to come up with an index that was larger than the number of saved tab groups, index into children() with that index, which would cause the heap buffer overflow in the bug.

Added several checks to prevent this and similar issues:
- don't show the overflow menu when hovering over the invisible button
- don't show the overflow menu if there aren't enough saved groups for it to be non-empty
- CHECK that a calculated drop index is within the valid range
- CHECK that a drop index retrieved from drag_data_ is within the valid range

Also a couple of drive-by const and type fixes.

Bug: 1433304
Change-Id: Idadb403b17b3a8fb332115226a1ed38355ecdd57
Low-Coverage-Reason: Drag & Drop tests blocked on crbug.com/1432770
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4518708
Reviewed-by: Darryl James <dljames@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1141728}

[modify] https://crrev.com/6bc26a95b47cc5d24be0949a4e8ca280766a46fb/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_bar.h
[modify] https://crrev.com/6bc26a95b47cc5d24be0949a4e8ca280766a46fb/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_bar.cc


### xp...@gmail.com (2023-05-15)

Hi, I can confirm that the fix works. Can the bug be closed as fixed? Thank you!

### dl...@chromium.org (2023-05-16)

Was not able to reproduce either. Marking this as fixed. 

Thanks for updating this!

### [Deleted User] (2023-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Congratulations, Sven! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug. Thank you for your efforts and reporting this issue to us!

### xp...@gmail.com (2023-05-26)

Thank you Amy and the team! :)

### am...@google.com (2023-05-27)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-05-31)

cc: xrosado@ who is currently investigating UI bugs

### am...@chromium.org (2023-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-23)

This issue was migrated from crbug.com/chromium/1433304?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1441368]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064054)*
