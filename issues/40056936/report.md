# Security: Page can use space key input to cause autofill prompt to render under cursor, bypasses mouse movement/designated keyboard input requirements for autofill

| Field | Value |
|-------|-------|
| **Issue ID** | [40056936](https://issues.chromium.org/issues/40056936) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | sc...@google.com |
| **Created** | 2021-08-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A page can make a user select an autofill item if they hold the space key and make 2-3 consecutive clicks (depending on user's clicking speed), without moving their mouse over an autofill item or pressing designated keyboard input sequences after the autofill prompt appears.

Normally Chrome requires an intentional selection by the user, either by moving the mouse over an autofill item or using the designated keyboard input sequences (space/up/down, then enter) to select an autofill item.

The page uses space keypresses by the user to trigger the autofill prompt with the first item selected. An input field with one space character typed into it will trigger the autofill prompt with the first item highlighted. To achieve this easily, the page limits the input value to a single space, despite the user holding down the space key. After an item is highlighted, only a single click on the item is required to send the data to the page.

To trick the user into clicking on the highlighted autofill item, the page disables autofill on the input field until the user has made the first click in an instructed sequence of clicks. Immediately after the first click, the page repositions the input field above the cursor (so autofill prompt renders at the cursor position) and then allows the user to trigger the autofill prompt. (To allow the user to trigger the autofill prompt, the page focuses another input field, then refocuses the main input field, then clears the main input field value to allow a new space keypress.)

By the time the user makes the second or third click (depending on user's clicking speed) in the sequence of clicks, the autofill prompt has rendered and the user is likely to accidentally click on the item. In a sequence of clicks, it's difficult for most users to notice the autofill prompt appear moments before they continue the clicking sequence.

ADDITIONAL CONTEXT  

The process above isn't that different from asking a user to press space and then enter sequentially, which is a designated keyboard input sequence. However, that is more difficult to achieve because 1) the user is more likely to notice the autofill prompt after pressing space but before pressing enter; 2) the user might already know the keyboard sequence will result in autofill data being sent to the page

The single space input value is required because subsequent spaces will not hide the autofill prompt but will unhighlight the item. If the item is not highlighted, one click or mouse movement would be required to highlight, and another click required to select the item. This eliminates the element of surprise and makes the attack unlikely to succeed.

This technique almost works with arrow up/down key input to trigger the autofill prompt. However, this is visually more obvious due to the highlighted item visually changing rapidly, and also requires two clicks to select item, so the attack is unlikely to succeed.

This is distict from <https://crbug.com/chromium/1240472> because it does not depend on mousedown to render autofill prompt in an unsafe location. A fix for that issue probably won't resolve this issue.

I've tested this with addresses (which includes name + email) and credit cards. For sample input, see the video recording.

**VERSION**  

Chrome Version: 92.0.4515.131 (Official Build) (64-bit) (cohort: Stable), 95.0.4612.2 Canary  

Operating System: Windows 10 OS Version 2009 (Build 19042.1110)

**REPRODUCTION CASE**  

PoC for address:  

Prerequisite: Have at least one address in chrome://settings/addresses

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-spacebar-clicks.html>
2. Press and hold space key in keyboard.
3. Click the same place 2-3 times in a row, anywhere in the page.

PoC for credit card:  

Prerequisite: Have at least one credit card in chrome://settings/payments

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-spacebar-clicks.html?creditcard>  
   
   Steps 2-3: Same as prior PoC.

For all PoCs:  

Observed: Autofilled data is provided to page, because page can cause user to select an autofill item without any mouse movement or designated keyboard input.  

Expected: Autofilled data is \*not\* provided to page, because page cannot cause user to select an autofill item without user intentionally moving mouse or using keyboard to select item.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [autofill-spacebar-clicks.mp4](attachments/autofill-spacebar-clicks.mp4) (video/mp4, 1.1 MB)
- [autofill-spacebar-clicks.html](attachments/autofill-spacebar-clicks.html) (text/plain, 5.4 KB)

## Timeline

### [Deleted User] (2021-08-19)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-08-19)

Since surprising the user with the autofill prompt is a common theme with some of my recent reports, I'll offer a solution that might work to mitigate them:
Requiring the autofill prompt to be visible for a minimum amount of time before a user can click to select an item (or use the enter key to select an item). This might cause usability issues, and for a few users the delay might be too short to mitigate, so I'm not certain how feasible it is to mitigate this way.

### al...@alesandroortiz.com (2021-08-19)

The video in the report shows 2-click repros the first few times (click speed probably closer to average user), and then shows 3-click repros when I start clicking at my usual speed. In theory a really fast clicker might require four or more clicks.

### pa...@chromium.org (2021-08-20)

My own long-standing :) view is that the control to perform autofill should not be in the content area, but in chrome. But, I leave it to the experts to decide.

This bug seems to require even less-likely interaction from the person before it would work than does https://bugs.chromium.org/p/chromium/issues/detail?id=1240472; it seems like realistically an attacker would need to build it into a compelling video game or something?

I am inclined to call it Security_Severity-Low, but could be convinced to bump it to Medium like the other bug. Or to bump the other bug down. Again, let's hear from autofill, privacy, and secure UX experts.

Limiting the platforms potentially affected due to the combination space bar + pointer requirement.

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-21)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2021-11-12)

Friendly ping: Has this been triaged further since I submitted report in mid-August?

### ma...@chromium.org (2021-11-12)

Handing over to Chris!

### sc...@google.com (2021-11-29)

CC dfried for context for review.

### gi...@appspot.gserviceaccount.com (2021-12-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/43d9f115a8264e6a95840a233a6b971d9ad6d46f

commit 43d9f115a8264e6a95840a233a6b971d9ad6d46f
Author: Christoph Schwering <schwering@google.com>
Date: Fri Dec 03 01:20:12 2021

[Autofill] Ignore clicks on initially hovered, unexited suggestion.

This CL ignores clicks on a suggestion if that suggestion was hovered
at the time the popup was shown (to be precise, if it has been hovered
at every OnPaint() since the popup's creation) AND the mouse has not
exited the suggestion yet.

Some consequences:
- Once the mouse has exited the whole popup,
  every suggestion is clickable.
- Once the mouse has exited the originally hovered suggestion,
  every suggestion is clickable.
- Suggestion selection using the keyboard is not affected.

Bug: 1240472, 1241585
Change-Id: I6bef84e60a36e9b14e0c639df3e023d062069b25
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3302104
Reviewed-by: Dana Fried <dfried@chromium.org>
Reviewed-by: Dominic Battré <battre@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#947797}

[modify] https://crrev.com/43d9f115a8264e6a95840a233a6b971d9ad6d46f/chrome/browser/autofill/mock_autofill_popup_controller.h
[modify] https://crrev.com/43d9f115a8264e6a95840a233a6b971d9ad6d46f/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/43d9f115a8264e6a95840a233a6b971d9ad6d46f/chrome/browser/ui/views/autofill/autofill_popup_view_native_views_unittest.cc


### sc...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-12-04)

Verified as fixed in 98.0.4745.0 Canary on Windows 10. Thanks for working on this, schwering!

### al...@alesandroortiz.com (2022-01-14)

For future reference, there's two bypasses to https://crbug.com/chromium/1240472 which *may* also work for the technique used in this report: https://crbug.com/chromium/1279268, https://crbug.com/chromium/1287364.

### gi...@appspot.gserviceaccount.com (2022-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c24bde01e377a8be7742826891857312eec278a6

commit c24bde01e377a8be7742826891857312eec278a6
Author: Christoph Schwering <schwering@google.com>
Date: Tue Jan 18 22:20:27 2022

[Autofill] Ignore clicks on initially hovered, unexited suggestion.

This CL ignores clicks on a suggestion if that suggestion was hovered
at the time the popup was shown (to be precise, if it has been hovered
at every OnPaint() since the popup's creation) AND the mouse has not
exited the suggestion yet.

Some consequences:
- Once the mouse has exited the whole popup,
  every suggestion is clickable.
- Once the mouse has exited the originally hovered suggestion,
  every suggestion is clickable.
- Suggestion selection using the keyboard is not affected.

(cherry picked from commit 43d9f115a8264e6a95840a233a6b971d9ad6d46f)

Bug: 1240472, 1241585
Change-Id: I6bef84e60a36e9b14e0c639df3e023d062069b25
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3302104
Reviewed-by: Dana Fried <dfried@chromium.org>
Reviewed-by: Dominic Battré <battre@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#947797}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3398792
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Reviewed-by: Milica Selakovic <selakovic@google.com>
Cr-Commit-Position: refs/branch-heads/4692@{#1460}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/c24bde01e377a8be7742826891857312eec278a6/chrome/browser/autofill/mock_autofill_popup_controller.h
[modify] https://crrev.com/c24bde01e377a8be7742826891857312eec278a6/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/c24bde01e377a8be7742826891857312eec278a6/chrome/browser/ui/views/autofill/autofill_popup_view_native_views_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f8ad20e36aae6083bfd7c95734313ea3b6d9da8

commit 2f8ad20e36aae6083bfd7c95734313ea3b6d9da8
Author: Christoph Schwering <schwering@google.com>
Date: Tue Jan 18 22:26:58 2022

[Autofill] Ignore clicks on initially hovered, unexited suggestion.

This CL ignores clicks on a suggestion if that suggestion was hovered
at the time the popup was shown (to be precise, if it has been hovered
at every OnPaint() since the popup's creation) AND the mouse has not
exited the suggestion yet.

Some consequences:
- Once the mouse has exited the whole popup,
  every suggestion is clickable.
- Once the mouse has exited the originally hovered suggestion,
  every suggestion is clickable.
- Suggestion selection using the keyboard is not affected.

(cherry picked from commit 43d9f115a8264e6a95840a233a6b971d9ad6d46f)

Bug: 1240472, 1241585
Change-Id: I6bef84e60a36e9b14e0c639df3e023d062069b25
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3302104
Reviewed-by: Dana Fried <dfried@chromium.org>
Reviewed-by: Dominic Battré <battre@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#947797}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3399744
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Reviewed-by: Milica Selakovic <selakovic@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1414}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/2f8ad20e36aae6083bfd7c95734313ea3b6d9da8/chrome/browser/autofill/mock_autofill_popup_controller.h
[modify] https://crrev.com/2f8ad20e36aae6083bfd7c95734313ea3b6d9da8/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/2f8ad20e36aae6083bfd7c95734313ea3b6d9da8/chrome/browser/ui/views/autofill/autofill_popup_view_native_views_unittest.cc


### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Comment Deleted]

### am...@chromium.org (2022-01-19)

This appears to be same root cause as https://crbug.com/chromium/1240472; temporarily removing CVE allocation to do deconfliction; can re-add/update if appropriate 

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Thank you for yet another detailed report, Alesandro! Given that this issue was the overlapping root cause as https://crbug.com/chromium/1240472, which was already rewarded, we wanted to show our appreciation for this detailed report and POCs to help ensure this issue could be fully resolved. We have decided to extend you a $1,000 thank you reward. Thanks again for your efforts and nice work!

### al...@alesandroortiz.com (2022-03-11)

Thanks for the reward! Really appreciate it given the overlapping root cause.

### [Deleted User] (2022-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1241585?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056936)*
