# Security: tel: URL scheme reference origin spoof on Windows and Linux

| Field | Value |
|-------|-------|
| **Issue ID** | [40050770](https://issues.chromium.org/issues/40050770) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | kn...@chromium.org |
| **Created** | 2019-11-22 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 80.0.3973.4 canary  

Operating System: Windows and Linux

**REPRODUCTION CASE**

This is the same bug as <https://crbug.com/chromium/1005596> but I'm still able to repro it on Windows.

The sharing dialog will display on <https://www.apple.com/contact/> to call a number chosen by the attacker  

and in this case the victim would think that the '<https://www.apple.com/contact/>' is intended to make a call.

- On macOS, the sharing dialog disappears after the navigation.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 147 B)
- [Recording #10.mp4](attachments/Recording #10.mp4) (video/mp4, 243.2 KB)

## Timeline

### ch...@gmail.com (2019-11-22)

[Comment Deleted]

### ch...@gmail.com (2019-11-22)

[Comment Deleted]

### ch...@gmail.com (2019-11-22)

[Comment Deleted]

### ch...@gmail.com (2019-11-22)

[Empty comment from Monorail migration]

### me...@google.com (2019-11-22)

The previous fix (crrev.com/c/1849382) doesn't seem Mac specific so not sure why it doesn't help here. .

knollr: PTAL? Thanks!



[Monorail components: UI>Browser>Sharing]

### sh...@chromium.org (2019-11-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-24)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kn...@chromium.org (2019-11-25)

Thanks! I'm taking a look why this is different from the original fix.

### kn...@chromium.org (2019-11-25)

The scenario here is slightly different from the one in https://crbug.com/1005596. This opens the dialog on the same origin, so we don't display the source origin it in the dialog, and then navigates to a different origin. The dialog keeps open on Linux, Windows and CrOS, but closes on Mac, probably because of different implementations of the RenderWidgetHostView [1] ?

The external protocol dialog for non-tel links on Linux and Windows closes automatically as it is a modal view and uses WebContentsModalDialogManager [2].

Other dialogs that inherit from BubbleDialogDelegateView would also have the same behavior (they close on navigation to different origin on Mac only), e.g. the bookmarks bubble is simple to test for this.

Emily, do you know what the expected behavior here is? Specifically for this dialog, I think we should just close it. Should this apply to all dialogs when navigating to a different origin or is this a special case for the Click to Call dialog?

[1]: https://cs.chromium.org/chromium/src/content/browser/renderer_host/render_widget_host_view_mac.mm?l=444&rcl=0ff2da3a87117be8cee1c1432fb2a6cb8408f4f2
[2]: https://cs.chromium.org/chromium/src/components/web_modal/web_contents_modal_dialog_manager.cc?l=135&rcl=82ee2f16eefe2f9cf8faa85708115b660eb17019

### kn...@chromium.org (2019-12-03)

CL up for review to close the Click to Call dialogs when navigating cross origin: https://crrev.com/c/1948839

### es...@chromium.org (2019-12-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/888f8247e6478c7858828f0805b404c55eeff19f

commit 888f8247e6478c7858828f0805b404c55eeff19f
Author: Richard Knoll <knollr@chromium.org>
Date: Wed Dec 04 18:42:11 2019

Close SharingDialogs on main frame cross origin navigation

This closes SharingDialogViews when the main frame navigates to a
different origin. Right now this only affects the SharingDialog and
(for CrOS) the IntentPickerBubbleView but will be enabled for all
subclasses of LocationBarBubbleDelegateView in a subsequent change.

Bug: 1027408
Change-Id: I07ca9ce55042265d85e56a84c5e43efa3cb026d0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1948839
Commit-Queue: Richard Knoll <knollr@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Emily Stark <estark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#721565}

[modify] https://crrev.com/888f8247e6478c7858828f0805b404c55eeff19f/chrome/browser/ui/views/intent_picker_bubble_view.cc
[modify] https://crrev.com/888f8247e6478c7858828f0805b404c55eeff19f/chrome/browser/ui/views/location_bar/location_bar_bubble_delegate_view.cc
[modify] https://crrev.com/888f8247e6478c7858828f0805b404c55eeff19f/chrome/browser/ui/views/location_bar/location_bar_bubble_delegate_view.h
[modify] https://crrev.com/888f8247e6478c7858828f0805b404c55eeff19f/chrome/browser/ui/views/sharing/click_to_call_browsertest.cc
[modify] https://crrev.com/888f8247e6478c7858828f0805b404c55eeff19f/chrome/browser/ui/views/sharing/sharing_dialog_view.cc


### kn...@chromium.org (2019-12-05)

Fixed in 80.0.3986.0, it now closes the dialog after navigation on non-macOS as well.

### sh...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-12)

Requesting merge to beta M79 because latest trunk commit (721565) appears to be after beta branch point (706915).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-12)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-12-12)

+adetaylor@ (Security TPM) for M79 merge review

This is severity medium,   no merge to M79 unless it is really needed. We would like to minimize the merges for next respin to reduce risk if possible at all. 

### ad...@chromium.org (2019-12-12)

Yep let's reject this merge. Sheriffbot wants to merge to *beta*, which is currently the same as stable, so let's not.

### na...@google.com (2019-12-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-17)

Congrats! The Panel decided to reward $2,000 for this report

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-26)

See also https://crbug.com/chromium/1036832 for a related problem which still remains even after this fix.

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1027408?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050770)*
