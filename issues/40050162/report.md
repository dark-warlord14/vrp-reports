# Security: tel: URL scheme reference origin spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40050162](https://issues.chromium.org/issues/40050162) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | kn...@chromium.org |
| **Created** | 2019-09-19 |
| **Bounty** | $2,000.00 |

## Description

Chrome Version: 79.0.3917.0  

Operating System: Mac

**REPRODUCTION CASE**  

This is another kind of spoof.

1. Open the testcase
2. Click on the button

The sharing dialog will display on <https://www.apple.com/contact/> to call a number chosen by the attacker  

, and in this case the victim would think that the '<https://www.apple.com/contact/>' is intended to make a call. and

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [Screen Shot 2019-09-19 at 03.29.09.png](attachments/Screen Shot 2019-09-19 at 03.29.09.png) (image/png, 482.0 KB)
- [testcase.html](attachments/testcase.html) (text/plain, 163 B)

## Timeline

### ch...@gmail.com (2019-09-19)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-09-19)

Confirmed this and the screenshot require the ClickToCallUI to be enabled. That looks like it’s currently only on beta.

[Monorail components: UI>Browser>Sharing]

### mv...@chromium.org (2019-09-19)

The poc.html in the original report seems to be about PaymentRequest not Click To Call. Is this the correct poc?

### mv...@chromium.org (2019-09-19)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-09-19)

The PoC in #1 is about click to call.

### ch...@gmail.com (2019-09-19)

Oops! sorry... I forgot to remove the wrong PoC.

### ch...@gmail.com (2019-09-19)

To fix this, I think chrome must prevent attempt to initiate navigation for frame with origin 'https://www.apple.com/contact/' from frame with URL 'testcase.html'.

### kn...@chromium.org (2019-09-19)

[Comment Deleted]

### kn...@chromium.org (2019-09-19)

As far as I can tell this is the same cause as in https://crbug.com/754304, +Emily who is working on that one

### sh...@chromium.org (2019-09-20)

Setting milestone and target because of Security_Impact=Beta and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-09-30)

estark@ can you merge the two issues, and make sure RBS label carries over to the bug tracking the fix ( if this is indeed a RBS)

### ge...@google.com (2019-10-01)

[BULK EDIT] Reminder M78 Stable is coming up fast. Please review this issue and provide an update on if this will make it for M78. If not please move to appropriate milestone. If required and will not be on time, please provide info on what needs to be done and when you expect it to be completed by. Thanks.

### es...@chromium.org (2019-10-02)

[Empty comment from Monorail migration]

### sr...@google.com (2019-10-03)

estark@ friendly ping to help update the status of this bug for M78.

### es...@chromium.org (2019-10-03)

I think we should leave this bug open since it's a different dialog and will need a different fix than https://crbug.com/chromium/754304. However, it need not be RBS because https://crbug.com/chromium/754304 has been open forever and this is not a fundamentally new vulnerability from that one. We can fix this one in 79 same as the other one.

### sh...@chromium.org (2019-10-04)

mvanouwerkerk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-04)

Setting milestone and target because of Security_Impact=Beta and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-10-07)

+adetaylor@ can you pls review https://crbug.com/chromium/1005596#c16 from estark@ where RBS is removed and sheriffbot@ has added it back , We should figure out a way to avoid this if possible as this would be lot of churn for TPM/dev to re-review the bugs again.

### ad...@chromium.org (2019-10-07)

I had a word with Sheriffbot. She explains that the right thing to do is to add ReleaseBlock-NA, so I've done so, and she promises to stop adding RBS.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8bd8d190b3947baaa9d5e053fa2c3e902da7c724

commit 8bd8d190b3947baaa9d5e053fa2c3e902da7c724
Author: Richard Knoll <knollr@chromium.org>
Date: Tue Oct 15 14:01:12 2019

Show origin in Click to Call dialog.

Mostly mechanical change to pipe the origin through to the dialog view.
The dialog shows the origin in a label with rounded corners, see
screenshot: https://imgur.com/LPAWxy2

Changes the BubbleFrameView to size |header_view_| to the ContentBounds
instead of centering it.

Bug: 1010920,1005596
Change-Id: I72f2e163552165b39ef00aaa1d1ea7cce8ce4895
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1849382
Commit-Queue: Richard Knoll <knollr@chromium.org>
Reviewed-by: Michael Wasserman <msw@chromium.org>
Reviewed-by: Alex Chau <alexchau@chromium.org>
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Cr-Commit-Position: refs/heads/master@{#705942}

[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/external_protocol/external_protocol_handler.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/sharing/click_to_call/click_to_call_ui_controller.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/sharing/click_to_call/click_to_call_ui_controller.h
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/sharing/click_to_call/click_to_call_ui_controller_unittest.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/sharing/sharing_dialog_data.h
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/sharing/sharing_ui_controller.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/sharing/sharing_ui_controller.h
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/ui/views/autofill/payments/local_card_migration_browsertest.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/ui/views/autofill/payments/save_card_bubble_views_browsertest.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/ui/views/sharing/sharing_dialog_view.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/chrome/browser/ui/views/sharing/sharing_dialog_view_unittest.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/ui/strings/ui_strings.grd
[add] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/ui/strings/ui_strings_grd/IDS_BROWSER_SHARING_CLICK_TO_CALL_DIALOG_INITIATING_ORIGIN.png.sha1
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/ui/views/bubble/bubble_dialog_delegate_view_unittest.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/ui/views/bubble/bubble_frame_view.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/ui/views/bubble/bubble_frame_view.h
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/ui/views/bubble/bubble_frame_view_unittest.cc
[modify] https://crrev.com/8bd8d190b3947baaa9d5e053fa2c3e902da7c724/ui/views/window/dialog_delegate_unittest.cc


### ch...@gmail.com (2019-10-17)

Fixed? 

### sh...@chromium.org (2019-10-19)

mvanouwerkerk: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kn...@chromium.org (2019-10-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### kn...@chromium.org (2019-11-01)

This is now done in Canary and will be released with the next version of M79. There is a follow-up CL to investigate if we can deprecate cross origin external protocol requests: https://crbug.com/1011429

### sh...@chromium.org (2019-11-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-05)

Not requesting merge to beta (M79) because latest trunk commit (705942) appears to be prior to beta branch point (706915). If this is incorrect, please replace the Merge-na label with Merge-Request-79. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats! The Panel decided to reward $2,000  for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1005596?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050162)*
