# Security: Page can cause autofill prompt to render under cursor in order to bypass mouse movement/keyboard input requirements for autofill

| Field | Value |
|-------|-------|
| **Issue ID** | [40056900](https://issues.chromium.org/issues/40056900) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Privacy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | sc...@google.com |
| **Created** | 2021-08-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A page can make a user select an autofill item with two consecutive clicks (three in limited cases), without moving their mouse or pressing keyboard keys after the autofill prompt appears.

Normally Chrome requires an intentional selection by the user, either by moving the mouse over an autofill item or using the keyboard to select an autofill item.

In essence, this is a simpler method to achieve the same outcome as <https://crbug.com/chromium/1239496>.

When a user clicks an input field, the autofill prompt position is calculated a few moments after the mousedown event occurs. However, there is a delay between the mousedown event and when the calculation occurs. If a page moves the input field immediately after the mousedown event, the prompt position is calculated based on the input field's new position.

A page can use this delay to move the input field into a position that results in the autofill prompt rendering at the cursor location.

To make the click on the input field easy (first click), a page can place the input field under the cursor at all times (using mousemove events). Immediately after the first click, the input field is moved to make the autofill prompt render under the cursor. With the cursor over the autofill item, clicking a second time results in the page receiving the autofill data.

If after page load the user does not move the cursor at all, a third click is required since (as far as I know) there is no way to determine cursor position without a mouse movement or click. In this scenario, the first click is used to determine the cursor position and move the input field under the cursor.

I've tested this with addresses (which includes name + email) and credit cards. For sample input, see the video recording.

**VERSION**  

Chrome Version: 92.0.4515.131 (Official Build) (64-bit) (cohort: Stable), 95.0.4609.3 Canary  

Operating System: Windows 10 OS Version 2009 (Build 19042.1110)

**REPRODUCTION CASE**  

PoC for address:  

Prerequisite: Have at least one address in chrome://settings/addresses

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-two-clicks.html>
2. Click the same place twice in a row, anywhere in the page.

PoC for credit card:  

Prerequisite: Have at least one credit card in chrome://settings/payments

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-two-clicks.html?creditcard>
2. (Same as prior PoC, click twice in a row)

For all PoCs:  

Observed: Autofilled data is provided to page, because page can cause user to select an autofill item without any mouse movement or keyboard input.  

Expected: Autofilled data is \*not\* provided to page, because page cannot cause user to select an autofill item without user intentionally moving mouse or using keyboard to select item.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [autofill-two-clicks.mp4](attachments/autofill-two-clicks.mp4) (video/mp4, 596.7 KB)
- deleted (application/octet-stream, 0 B)
- [autofill-two-clicks.html](attachments/autofill-two-clicks.html) (text/plain, 3.0 KB)
- [autofill-window-move.mp4](attachments/autofill-window-move.mp4) (video/mp4, 451.7 KB)
- [autofill-window-move.html](attachments/autofill-window-move.html) (text/plain, 1016 B)
- [autofill-window-move-popup.html](attachments/autofill-window-move-popup.html) (text/plain, 2.2 KB)
- [autofill-move-two-clicks.html](attachments/autofill-move-two-clicks.html) (text/plain, 3.7 KB)
- [autofill-move-two-clicks-canary.mp4](attachments/autofill-move-two-clicks-canary.mp4) (video/mp4, 752.0 KB)
- [autofill-move-two-clicks-stable.mp4](attachments/autofill-move-two-clicks-stable.mp4) (video/mp4, 932.1 KB)

## Timeline

### [Deleted User] (2021-08-17)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-08-17)

Updated PoC source attached (removes unused code).

### pa...@chromium.org (2021-08-17)

Thanks for this report!

I haven't tried this on Android yet, but it might well work there, too.

I almost always have to do 3 clicks, not just 2. Not sure why. Clicking Escape gets me out of the pop-up autofill dialog, naturally.

Still, violates the model. Thanks!

[Monorail components: Privacy UI>Browser>Autofill>UI]

### pa...@chromium.org (2021-08-17)

Oops, battre is out for another week. estade, could you please take a look? Thanks!

### [Deleted User] (2021-08-17)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-08-17)

I don't work on Autofill these days but lately Mohamed has been tackling these sorts of bugs.

### al...@alesandroortiz.com (2021-08-18)

palmer@: Thanks for triage.

mamir@: Thanks for working on all my autofill reports from the past couple of weeks. As a heads up, I may still have at least a couple more reports related to autofill.

I discovered a variation of the original report, which in terms of victim experience works similarly but might not have the same fix as original report. Given similar behavior and potential shared fix, I'm reporting it via this comment. But if the fix turns out to be distinct, I can create a new issue to track and reward separately.

VULNERABILITY DETAILS
In this variation, to take advantage of the delay in autofill prompt position calculation, instead of moving the input field within the same page on mousedown, we move the whole window (popup) on mousedown.

This requires a third click to open the popup compared to the two clicks for the original report, but otherwise works the same in terms of victim experience. (https://crbug.com/chromium/1239496 also requires three clicks due to use of popup.)

REPRODUCTION CASE
PoC for address:
Prerequisite: Have at least one address in chrome://settings/addresses
1. Navigate to https://alesandroortiz.com/security/chromium/autofill-window-move.html
2. Click the same place three times in a row, anywhere in the page.

PoC for credit card:
Prerequisite: Have at least one credit card in chrome://settings/payments
1. Navigate to https://alesandroortiz.com/security/chromium/autofill-window-move.html?creditcard
2. (Same as prior PoC, click three times in a row)

Observed and expected behavior are the same as original report.

### al...@alesandroortiz.com (2021-08-18)

Re: https://crbug.com/chromium/1240472#c3, I'm not able to repro the three click behavior if I move my mouse after page load, but maybe that's non-Windows behavior or something else. Could be particularly fast clicking or device/system mouse settings treating one of the clicks as a double click or deduping or something along those lines. In any case, not particularly significant to impact or severity whether it's two or three consecutive clicks.

### ma...@chromium.org (2021-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-01)

mamir: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-15)

mamir: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2021-09-21)

mamir@, koerber@: Another friendly ping. Any updates on this issue? No notable crbug activity since mid-August and don't see an open CL.

### ma...@chromium.org (2021-09-27)

Progress is hindered by vacation/urgent work/other security bugs.
However, it's on my radar! 

### al...@alesandroortiz.com (2021-11-12)

mamir@: Hope you enjoyed your vacations! Given you recently reassigned similar bugs to schwering@, is this one still on your radar or should it also be reassigned?

### ma...@chromium.org (2021-11-15)

Thanks Alesandro for the hint!

Over to Chris!

### sc...@google.com (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### sc...@google.com (2021-11-25)

Some fix ideas: https://docs.google.com/document/d/1-6qi7_T9rIMIuAt94Y5-aKgkVD7QV2g_pdHuKit8wy4/edit#
Draft CL: https://crrev.com/c/3301041

### sc...@google.com (2021-11-25)

CC PMs.

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

Verified as fixed in 98.0.4745.0 Canary on Windows 10, using PoCs from original report and https://crbug.com/chromium/1240472#c7. Really like this solution since mitigates many potential future variants.

However, this mitigation can be bypassed with minimal mouse movement if:
* the attacker convinces the user to click repeatedly while moving the mouse downwards at a not-too-fast speed (e.g. follow a moving dot on the page)
* the first suggestion renders slightly below the current mouse position (the position is indirectly controllable by the attacker page)

The delay when showing the autofill prompt is minimal and predictable, so when the user moves their mouse down at a not-too-fast speed, the cursor is outside the first suggestion when the autofill prompt is initially shown, and shortly thereafter enters the first suggestion which is now clickable. It's perhaps slightly less reliable than the prior PoCs, more so when using touchpads, but a small mouse movement while clicking isn't too much to ask from any user, especially those using a hardware mouse.

I can file this bypass as a separate report if requested, since this patch does fix the most straightforward repro methods and would be effective in most cases. I have a draft working bypass PoC but will clean it up and post it by tomorrow.

This bypass would also work for https://crbug.com/chromium/1241585, except that method results in a larger and more unpredictable delay when showing the autofill prompt, so I wouldn't consider the bypass a reliable attack when using that method.

### al...@alesandroortiz.com (2021-12-05)

Following up https://crbug.com/chromium/1240472#c28:

Steps to reproduce:
1. Navigate to https://alesandroortiz.com/security/chromium/autofill-move-two-clicks.html
2. Follow dot using mouse and click twice while following dot (i.e. moving mouse to the right)

Observed: Autofilled data is provided to page, because page can cause user to select an autofill item with minimal mouse movement.
Expected: Autofilled data is *not* provided to page, because page cannot cause user to select an autofill item without user intentionally moving mouse or using keyboard to select item.

Attached are PoC source and repro videos using 98.0.4747.0 Canary and 96.0.4664.45 Stable.

With PoC modifications, the direction of the mouse can be in any direction (e.g. up, down, left, or right) since the attacker controls the autofill prompt placement relative to the mouse (and its expected movement). It's easier to do right/left since the second-click area is wider, but diagonal works almost as well, and up/down can also work well.

### sc...@google.com (2021-12-10)

Re https://crbug.com/chromium/1240472#c28 and https://crbug.com/chromium/1240472#c29, you're right, of course. I had been thinking about mouse movement a lot for this fix, but not considered this.

Blocking clicks for 500 ms would fix it, but I had hoped to avoid such a timer. Perhaps someone more accustomed to UI has a better idea.

Do you want to file this as a separate bug? Since the more critical attack from https://crbug.com/chromium/1240472#c0 is fixed by https://crbug.com/chromium/1240472#c24, I'd like to leave this one closed.

### al...@alesandroortiz.com (2021-12-13)

Filed as https://crbug.com/chromium/1279268 and requested schwering@google.com be CC'd.

FWIW, I had previously suggested implementing a delay before allowing interaction with autofill prompt in https://bugs.chromium.org/p/chromium/issues/detail?id=1241585#c2

A combination of both strategies (ignoring clicks on initially hovered, unexited suggestion + delay before allowing interaction) should be effective to mitigate variants.

### al...@alesandroortiz.com (2022-01-13)

Will this be merged into Stable? Still repros on 97.0.4692.71 Stable. I accidentally "re-discovered" this vulnerability while working on other research.

### al...@alesandroortiz.com (2022-01-14)

Found another bypass to the fix implemented here, filed as https://crbug.com/chromium/1287364.

### sc...@google.com (2022-01-14)

Adrian, should this bug (see video in https://crbug.com/chromium/1240472#c0) be merged to M97?

### ad...@chromium.org (2022-01-14)

Hmmm. As a medium severity bug, externally reported, I'd have expected sheriffbot to ask to merge this to _beta_ on Dec 4th. I don't know why it didn't. I've added it to my long list of sheriffbot anomalies to look into one day.

Medium severity bugs aren't merged back to stable as a matter of course, but such a beta merge in December would have got this into 97. So adding merge requests now for consideration.

### [Deleted User] (2022-01-14)

Merge review required: M97 is already shipping to stable.

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

### [Deleted User] (2022-01-14)

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

### sc...@google.com (2022-01-14)

1. Security fix.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3302104
3. Yes.
4. No, n/a.
5. N/a.
6. No.

### am...@chromium.org (2022-01-18)

based on comments above, this appears to already have been merged to M98; merge approved to M97 and M96, please merge this fix to branches 4692 and 4664 respectively, ASAP so this can be included in the next respins for Extended and Stable. After this week's release, there are no further planned releases of M97. 

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


### [Deleted User] (2022-01-18)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

[Empty comment from Monorail migration]

### gm...@google.com (2022-01-24)

Merged to 96. No need to cherry pick for LTS.

### gm...@google.com (2022-01-24)

[Empty comment from Monorail migration]

### ad...@google.com (2022-01-31)

I looked into why sheriffbot didn't request a merge here. Tracking as https://crbug.com/chromium/1292625.

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations on another one, Alesandro! The VRP Panel has decided to award you $3000 for this report. Thank you for your efforts and your patience while we resolved this issue. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-02-22)

Thanks for the reward!

### [Deleted User] (2022-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1240472?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Privacy, UI>Browser>Autofill>UI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056900)*
