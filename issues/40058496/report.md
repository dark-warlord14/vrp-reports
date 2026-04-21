# Page can use EyeDropper API to bypass mouse movement/keyboard input requirements for autofill (bypass of issue 1240472 fix)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058496](https://issues.chromium.org/issues/40058496) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Color, UI>Browser>Autofill |
| **Platforms** | Fuchsia, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | sc...@google.com |
| **Created** | 2022-01-14 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description


Page can use EyeDropper API to bypass mouse movement/keyboard input requirements for autofill (bypass of https://crbug.com/chromium/1240472 fix)


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


#### Which URL have you found the vulnerability in?

https://alesandroortiz.com/security/chromium/autofill-eye-dropper.html


---

### The problem


#### Please describe the technical details of the vulnerability

VULNERABILITY DETAILS
A page can make a user select an autofill item with two consecutive clicks (three in limited cases), without moving their mouse or pressing keyboard keys after the autofill prompt appears. This bypasses the fix for https://crbug.com/chromium/1240472 in Canary (the fix is not yet in Stable).

See description of https://crbug.com/chromium/1240472 for details on how the PoC moves the input field under the cursor.

Using the EyeDropper API (enabled by default in Chrome 95) bypasses the checks implemented in commit 43d9f115a8264e6a95840a233a6b971d9ad6d46f. It seems that calling EyeDropper.open() and immediately closing the eye dropper is sufficient to toggle mouse_observed_outside_of_item_ to true. I have not verified the variable state using a local build, but this is the most likely explanation based on code analysis.

VERSION
Chrome Version: 99.0.4828.0 Canary (bypass is *not* for Stable since fix for https://crbug.com/chromium/1240472 is not yet in Stable)
Operating System: Windows 10 Version 20H2 (Build 19042.1348)

REPRODUCTION CASE
The PoC assumes the #autofill-center-aligned-suggestions flag is disabled (AFAIK it's disabled for most user), but PoC can be adjusted to work with the flag enabled.

PoC for address:
Prerequisite: Have at least one address in chrome://settings/addresses
1. Navigate to https://alesandroortiz.com/security/chromium/autofill-eye-dropper.html
2. Click the same place twice in a row, anywhere in the page.

PoC for credit card:
Prerequisite: Have at least one credit card in chrome://settings/payments
1. Navigate to https://alesandroortiz.com/security/chromium/autofill-eye-dropper.html?creditcard
2. (Same as prior PoC, click twice in a row)

For all PoCs:
Observed: Autofilled data is provided to page, because page can cause user to select an autofill item without any mouse movement or keyboard input.
Expected: Autofilled data is *not* provided to page, because page cannot cause user to select an autofill item without user intentionally moving mouse or using keyboard to select item.

Slow PoC to help with analysis:
1. Navigate to https://alesandroortiz.com/security/chromium/autofill-eye-dropper-slow.html
Experiment with clicking once and waiting, clicking once and moving mouse, clicking twice quickly vs. slowly, etc. to observe slightly different behavior which might be helpful for analysis.

CREDIT INFORMATION
Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

See above


---

### The cause


#### What version of Chrome have you found the security issue in?

99.0.4828.0 Canary


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Other


#### How would you like to be publicly acknowledged for your report?

Alesandro Ortiz




## Attachments

- [autofill-eye-dropper.html](attachments/autofill-eye-dropper.html) (text/plain, 3.6 KB)
- [autofill-eye-dropper.mp4](attachments/autofill-eye-dropper.mp4) (video/mp4, 565.1 KB)
- [autofill-eye-dropper-slow.mp4](attachments/autofill-eye-dropper-slow.mp4) (video/mp4, 458.7 KB)

## Timeline

### ch...@appspot.gserviceaccount.com (2022-01-14)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-01-14)

I tried filing this directly via Monorail as I usually do but kept getting "500 Server Error" responses, so I filed via https://bughunters.google.com/report/vrp

Attachments below.

### ct...@chromium.org (2022-01-14)

+schwering@ could you please take a look? Thanks.

The root cause here may fall on the eyedropper implementation, so also cc'ing eyedropper OWNERS (for the DIR_METADATA that has the Blink>Forms>Color component).

Reporter: If the fix for https://crbug.com/chromium/1240472 was fully merged back, do you think this would bypass that fix going all the way back to Chrome 95 (when the Eye Dropper API was shipped)? If so, I'll update this to be FoundIn-95.


[Monorail components: Blink>Forms>Color UI>Browser>Autofill]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2022-01-14)

Re: https://crbug.com/chromium/1287364#c3, yes, I think it would bypass back in 95 if fix was there. Relevant EyeDropper and autofill code has not changed much since 95 unless root cause is a far-away change.

As an FYI, per https://chromiumdash.appspot.com/commit/43d9f115a8264e6a95840a233a6b971d9ad6d46f the fix is also in 98 Dev and 98 Beta.

### ct...@chromium.org (2022-01-14)

Thanks. Setting FoundIn-95 accordingly.

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### sc...@google.com (2022-01-16)

The fix of https://crbug.com/chromium/1279268 (delay) will also address this one.

I can't reproduce this issue on Linux so far, only on Windows.

### sc...@google.com (2022-01-17)

The planned fix is to ignore clicks for 500 ms after a suggestion was displayed.

Discussed this with PM nepper@ and UX dsholkov@ in the feature sync today and reached the conclusion that the potential negative impact on usability outweighs the risk of leaking user data. We plan to do a Finch study about the fix.

### sc...@google.com (2022-01-17)

I'm also looking into alternative ways to fix this that don't need a feature.

### sc...@google.com (2022-01-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/403ebfda330f64d2cb0e102d215f32f15df449a0

commit 403ebfda330f64d2cb0e102d215f32f15df449a0
Author: Christoph Schwering <schwering@google.com>
Date: Tue Jan 18 20:02:21 2022

[Autofill] Ignore clicks on unexited items also after overlay.

A previous CL ignored clicks on an Autofill popup item if that
item has been initially hovered and unexited.

An item was considered "exited" if OnMouseExited() event had fired,
which is also the case when the suggestion is overlaid by another popup.

This CL changes excludes the overlay case.

Bug: 1287364
Change-Id: I7c0bef84975c5b3ba0e7ee31e56aea43453a0393
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3395838
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#960556}

[modify] https://crrev.com/403ebfda330f64d2cb0e102d215f32f15df449a0/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc


### sc...@google.com (2022-01-18)

The above fix avoids the 500 ms delay.

### [Deleted User] (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-19)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-01-21)

Verified as fixed in ASan build 961550 on Windows 10, using fix specific to this issue in https://crbug.com/chromium/1287364#c14. The 500ms delay to fix https://crbug.com/chromium/1279268 would also help this case but I tested without the delay to verify this issue's specific fix.

### [Deleted User] (2022-01-22)

Not requesting merge to dev (M99) because latest trunk commit (960556) appears to be prior to dev branch point (961656). If this is incorrect, please replace the Merge-NA-99 label with Merge-Request-99. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-03)

Congratulations, Alesandro - the VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts in reporting these issues to us and nice work! 

### al...@alesandroortiz.com (2022-03-04)

Thanks for the reward!

### am...@google.com (2022-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1287364?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>Color, UI>Browser>Autofill]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058496)*
