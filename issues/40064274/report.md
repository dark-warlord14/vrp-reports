# Security: Select option can cover permission buble , lead to spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40064274](https://issues.chromium.org/issues/40064274) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | tu...@chromium.org |
| **Created** | 2023-04-29 |
| **Bounty** | $500.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [Screencast from 2023-05-16 11-11-29.webm](attachments/Screencast from 2023-05-16 11-11-29.webm) (video/webm, 156.3 KB)

## Timeline

### [Deleted User] (2023-04-29)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-04-29)

i updated poc

### pg...@google.com (2023-05-01)

The overlay doesn't seem to happen super reliably (either the text is selected, the blue box doesn't pop up, or the permission pop up is shown as an omnibox-area chip), but I have been able to repro this on M112

Presumably, the design could be updated to look just like the classic theme chrome permission pop up, and hence successfully spoof the UI. My not having been able to reliably reproduce this seems like things that could be fixed with the format of the button, and though this requires a double tap/click (versus a single), I think that is a simple enough action that it doesn't necessarily drop the severity from high to medium (feel free to fight me on this).

[Monorail components: UI>Browser>Permissions>Prompts]

### pg...@google.com (2023-05-01)

tungnh@ I think this might be a dupe of https://crbug.com/chromium/1394410 of which you are currently the owner - can you take a look and confirm?

### pg...@google.com (2023-05-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tu...@chromium.org (2023-05-02)

> tungnh@ I think this might be a dupe of https://crbug.com/chromium/1394410 of which you are currently the owner - can you take a look and confirm?

I think the two bugs are different. In https://crbug.com/chromium/1394410, the attacker is trying to hide the prompt completely, but the user is still able to interact with it = tab move focus + enter. In this ticket, the attacker is trying to spoof the prompt or silently interact with the overlay (might be). In both cases, we should disable the selected area if it intersects with the prompt bubble.


### pg...@google.com (2023-05-02)

Ah, yeah seems like a fair distinction - thank you!

The fix sounds like it may overlap - are you still a good owner for this? if not, let me know!

### pm...@chromium.org (2023-05-16)

Tungnh@: A small nag on this, I was able to reproduce in M-113 see attached video. 
I wasn't able to reproduce by double clicking as in #1 and #2, but by timing the click right during the permission prompt's appearance, it worked.
This seems quite unreliable as an attack vector, unless there's some gamification to force the user to click at a given rythm I guess... 

### [Deleted User] (2023-05-16)

tungnh: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2023-05-17)

This should be Sev-Medium because of the user interaction and the limited visual fidelity of the spoof.

### tu...@chromium.org (2023-05-30)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2023-06-20)

hello any updates?

### tu...@chromium.org (2023-06-21)

Oh, I did not notice that was set back to priority 1 again. Working on this, and thanks for reporting the issue

### tu...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### el...@google.com (2023-06-30)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-07-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/583f07e3957db9bc6eaa936d46a30cc38446ebef

commit 583f07e3957db9bc6eaa936d46a30cc38446ebef
Author: Thomas Nguyen <tungnh@chromium.org>
Date: Wed Jul 19 17:45:37 2023

Dont show popup if its bounds intersect with permission prompt

Bug: 1441228
Change-Id: I3b5d6afff2ca98afb66aca18fc98f2147f52260a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4652611
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1172467}

[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/chrome/browser/ui/views/permissions/permission_prompt_desktop.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/permission_prompt.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/permission_manager.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/browser/renderer_host/render_widget_host_browsertest.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/browser/permissions/permission_controller_impl.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/chrome/browser/ui/views/permissions/permission_prompt_chip.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/browser/permissions/permission_controller_impl.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/android/permission_prompt/permission_prompt_android.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/chrome/browser/ui/views/permissions/permission_prompt_bubble.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/test/mock_permission_prompt.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/test/mock_permission_prompt.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/chrome/browser/ui/views/permissions/permission_prompt_bubble.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/browser/renderer_host/DEPS
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/permission_manager.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/browser/renderer_host/popup_menu_helper_mac.mm
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/chrome/browser/ui/views/permissions/permission_prompt_chip.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/test/BUILD.gn
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/chrome/browser/ui/views/permissions/permission_prompt_desktop.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/android/permission_prompt/permission_prompt_android.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/components/permissions/permission_request_manager.h
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/public/test/mock_permission_controller.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/public/browser/permission_controller_delegate.cc
[modify] https://crrev.com/583f07e3957db9bc6eaa936d46a30cc38446ebef/content/public/browser/permission_controller_delegate.h


### tu...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0748d4be320483bb70986ae18c7e4754b74e4374

commit 0748d4be320483bb70986ae18c7e4754b74e4374
Author: Ian Vollick <vollick@chromium.org>
Date: Fri Jul 21 18:00:02 2023

[ios] Disable popup interceptor browsertests

This aligns with Android (for which these tests are disabled).
Test was introduced in crrev.com/c/4705070.

Bug: 1441228
Change-Id: If9b5e9781ea5e73af9c9223ed2dcb1559b97bbb9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4705070
Commit-Queue: Avi Drissman <avi@chromium.org>
Commit-Queue: Ian Vollick <vollick@chromium.org>
Auto-Submit: Ian Vollick <vollick@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1173616}

[modify] https://crrev.com/0748d4be320483bb70986ae18c7e4754b74e4374/content/browser/renderer_host/render_widget_host_browsertest.cc


### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Thank you for the report. Based on the limited security impact of this issue, the VRP Panel has decided to award you $500 since we were able to land a change from to mitigate this issue. Thank you for taking the time to report this issue to us! 

### sa...@gmail.com (2023-07-28)

thank you amy for the rewards

### am...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1441228?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064274)*
