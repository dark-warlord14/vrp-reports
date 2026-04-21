# Security: Chrome on Android Tablet Mode Select Dropdown Spinner able to Overlap Fullscreen Notification Toast

| Field | Value |
|-------|-------|
| **Issue ID** | [40059710](https://issues.chromium.org/issues/40059710) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2022-05-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

On Chrome for Android Tablet (or smallest width set to 600dp or more than 600dp) the select option dropdown menu is displayed using Android Spinner instead of Android Dialog.

Interestingly the select dropdown menu which displayed using Android Spinner able to overlap fullscreen notification toast.

**VERSION**

- Chrome 101.0.4951.61 on Androis 11; Mi 9T
- Chrome Beta 102.0.5005.58 on Android 11;, Mi 9T
- Chrome Dev 103.0.5055.0 on Android 11; Mi 9T
- Chrome Canary 104.0.5072 0 on Android 11; Mi 9T

(Android "Developer options" -> "Smallest width" set to 600dp for Chrome switch to tablet mode)

**REPRODUCTION CASE**

1. Open Chrome on Android Tablet or for Android Phone set smallest width to 600dp or more than 600dp
2. Visit attached testcase-mi9t.html
3. Tap on select element
4. Select dropdown menu Android Spinner overlap fullscreen notification toast

**CREDIT INFORMATION**  

Reporter credit: Irvan Kurniawan (sourc7)

## Attachments

- [testcase-mi9t.html](attachments/testcase-mi9t.html) (text/plain, 1.5 KB)
- [Chrome on Android Tablet Mode - Select Dropdown Spinner overlap Fullscreen Notification Toast.mp4](attachments/Chrome on Android Tablet Mode - Select Dropdown Spinner overlap Fullscreen Notification Toast.mp4) (video/mp4, 1.4 MB)
- [select-dropdown.png](attachments/select-dropdown.png) (image/png, 62.0 KB)

## Timeline

### [Deleted User] (2022-05-20)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-05-20)

Thanks for the report.

jinsukkim@: This is a Clank UI security issue, are you able to look into it or help triage?

[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2022-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2022-05-24)

<select> is a modeless UI on tablets (unlike a modal dialog on phones, which needs to be dismissed before fullscreen is entered). It is styled by design to cover the top of the screen and obscure the fullscreen notification toast. 

I don't have a good idea how to fix this at this moment.

### tw...@chromium.org (2022-05-24)

When we were using the OS toast, that shows on top of everything else. Now that we're using custom UI, we have to take z-index into account.


> It is styled by design to cover the top of the screen and obscure the fullscreen notification toast. 

I suspect that this is by product of moving to our own UI rather than desired styling.... is there a way to get the z-indexing so that our toast sits above everything else?

### ji...@chromium.org (2022-05-24)

The select dropdown is an AnchoredPopupWindow on a different Window/View hierarchy from the notification toast which is a child view of ContentView (dropdown_layout vs. coordinator in the attached view). I think it will be on top of anything else while visible.


### tw...@chromium.org (2022-05-24)

Yep, popupwindow would be above a child view in our main window.

Sorry for asking a question I've already asked before... but should we use a popupwindow for our toast?

### tw...@chromium.org (2022-05-25)

As another idea from this morning -- could we just dismiss this dropdown spinner when entering fullscreen? It's perhaps a slightly worse UX (user has to retrigger select dropdown) but would fix this security bug, and would be consistent with phone behavior.

### ji...@chromium.org (2022-05-27)

Thank you Theresa. I like the idea of dismissing the dropdown. In practical world it wouldn't cause a problem since sane websites won't design UI in the way the testcase would.

Using popupwindow would sound good too, but there could be hacks to put a view in front of the toast to hide it again. Let me go with the suggestion in https://crbug.com/chromium/1327505#c9.

### [Deleted User] (2022-06-11)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-06-13)

Security marshal here. jinsukkim@, if you're continuing to make progress, can we change the status to Started?

### ji...@chromium.org (2022-06-13)

Will get back to this in a week.

### [Deleted User] (2022-06-27)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-18)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/726a045288fcffacc3ab76705d2effe64ccb4b14

commit 726a045288fcffacc3ab76705d2effe64ccb4b14
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Thu Aug 25 18:25:37 2022

[Android] Dismiss select popup upon entering fullscreen

Chrome dismisses select popup menu when entering fullscreen. This
prevents a potential hack that deliberately hides the fullscreen
notification toast message with the select popup menu.

Bug: 1327505
Change-Id: I788e6dc3f9866beeac5cd58232a1e7facacf43bd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3847044
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Reviewed-by: Bo Liu <boliu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1039341}

[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view.h
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view_mac.mm
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view_child_frame.h
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view_mac.h
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view_aura.h
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view_child_frame.cc
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view_aura.cc
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view_android.cc
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_view_android.h
[modify] https://crrev.com/726a045288fcffacc3ab76705d2effe64ccb4b14/content/browser/web_contents/web_contents_impl.cc


### ji...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1327505?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059710)*
