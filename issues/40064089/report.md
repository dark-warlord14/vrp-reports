# Security: cursor pointer can cover autofill prompt

| Field | Value |
|-------|-------|
| **Issue ID** | [40064089](https://issues.chromium.org/issues/40064089) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | sc...@google.com |
| **Created** | 2023-04-18 |
| **Bounty** | $1,000.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-04-19)

deleted

### za...@google.com (2023-04-19)

Hi thanks for reporting. The video is broken can you please upload again? And I am not able to reproduce this issue following your poc steps and can you also provide the expected behavior thanks!

### sa...@gmail.com (2023-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-19)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2023-04-19)

deleted

### sa...@gmail.com (2023-04-21)

redacted

### za...@google.com (2023-04-24)

Hi schwering@ can you please take a look at this bug. It can be constantly reproduced. Thanks. 

[Monorail components: UI>Browser>Autofill]

### za...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-02)

schwering: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@google.com (2023-05-04)

Thanks for the report! 

I've attached a simplified version of the PoC; internally it's also available under [1].

I'm not sure how critical this is. The cursor can occlude only parts of the Autofill popup because the cursor size is limited at 128x128 pixels [2] and the Autofill popup is wider than that because of the "Manage addresses" / "Manage payment methods" string. To be safe, we should perhaps increase the popup's minimum width [3,4].

Adrian, do you agree with reducing the severity?

[1] https://codebin.googleplex.com/view/jhsbbn2nqq3
[2] https://source.chromium.org/chromium/chromium/src/+/main:ui/base/cursor/cursor.cc;l=100;drc=e77d8705ea2d252a74e0fbd7778e653c010f5c53
[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/views/autofill/popup/popup_view_views.cc;l=73;drc=e0e0d24aaa54727dc0a8bc4b159ccdf80d3f5d8d
[4] https://crrev.com/c/4506703

### ba...@chromium.org (2023-05-04)

I think that a proper solution would be to show a default cursor over all chrome menus. (I am not saying that I know how to do that.)

### sc...@google.com (2023-05-04)

We already do that. But when the mouse position (in [1], the top left corner of the blue square) is sufficiently close to the menu, the mouse pointer overlays the menu.

### ad...@google.com (2023-05-04)

I have asked zackhan@ to explain his reasoning behind this severity, and tweak if necessary.

### za...@google.com (2023-05-04)

I gave it a high severity at first because it might be able to allows an attacker to read or modify confidential data belonging to other web sites (saved in password manager) but based on the discussion, I think medium severity is reasonable. Thanks for tagging me. 

### ba...@chromium.org (2023-05-05)

+Mason for representation from the renderer side. I am not sure how to best handle this.

### sc...@google.com (2023-05-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/41321c91ec48a1bb68e9656d63def67f44d21ddc

commit 41321c91ec48a1bb68e9656d63def67f44d21ddc
Author: Christoph Schwering <schwering@google.com>
Date: Tue May 09 13:01:10 2023

[Autofill] Require minimum width of Autofill popup

This CL sets the minimum width of the Autofill popup to 150 px so
that it exceeds the maximum width of a cursor.

Bug: 1434330
Change-Id: Iecdf80e03d93b5e440847935eb5e71636c687381
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4506703
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Quick-Run: Dima Sholkov <dsholkov@google.com>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#1141320}

[modify] https://crrev.com/41321c91ec48a1bb68e9656d63def67f44d21ddc/chrome/browser/ui/views/autofill/popup/popup_view_views.cc


### sc...@google.com (2023-05-12)

I'm not sure how much more we can do in Autofill-specific code about this issue other than the CL https://crbug.com/chromium/1434330#c21, so I'll unassign this.

Here are a few thoughts (I'm not a UI person though):

Popups like the context menu switch a different cursor globally. I suppose they grab the focus, which is not an option for the Autofill popup because user keyboard input should be passed to the focused text field while the Autofill popup is being displayed.

The cursor also overlays permission bubbles. Unlike the Autofill popup, the website has no control over their position, so it's not exactly comparable. The cursor even reaches beyond the borders of the WebContents and even Chrome window (only tested on Mac).

I'm not sure this issue is actually needs any further fix because all dialogs I'm aware of are significantly larger than 128 x 128 pixels.

### ad...@chromium.org (2023-05-15)

Hi, as this is a security bug we can't lave it un-assigned. In addition, once this is marked Fixed, various processes will kick off including paying a reward to the original reporter, so we need to get it to Fixed state when we can.

Can I suggest the following course of action:

1) we consider https://crbug.com/chromium/1434330#c21 a "fix" and mark this bug Fixed
2) we file a new bug for the potential risk of cursors overlaying permissions bubbles (done - https://crbug.com/chromium/1445459 - though I think it will probably turn out not to be a real issue)
3) if you think there are remaining known flaws which we can't fix due to design/compatibility limitations, we document them in a new entry on the Chromium Security FAQ (https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md). The main reason to do this is so that our VRP reporters don't waste their time filing bugs about them, only to suffer the disappointment of having those bugs WontFixed.

However per your last sentence:
> I'm not sure this issue is actually needs any further fix because all dialogs I'm aware of are significantly larger than 128 x 128 pixels.

it sounds like we do genuinely consider this Fixed, so step 3 probably isn't necessary?

### sc...@google.com (2023-05-15)

Thanks for filing the bug about permission bubbles.

I agree that Step 3 isn't necessary. I've pinged the other Autofill people on this bug to weigh in if they disagree.

Note that https://crbug.com/chromium/1434330#c21 is a fix against future regressions. As far as I know, also before https://crbug.com/chromium/1434330#c21 the Autofill popup in all cases was wider than 128 px.

### [Deleted User] (2023-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-15)

[Empty comment from Monorail migration]

### el...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-05-18)

besides the custom cursor it also covers the permission request prompt it also covers the omni box, I have made a report on: https://bugs.chromium.org/p/chromium/issues/detail?id=1357442 can you check it too because it's very old (a year ago)

### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Congratulations, Hafiizh! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-05-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1434330?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064089)*
