# Security: heap-over-flow in AutofillPopupControllerImpl::RemoveSuggestion

| Field | Value |
|-------|-------|
| **Issue ID** | [40055842](https://issues.chromium.org/issues/40055842) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android |
| **Reporter** | zh...@gmail.com |
| **Assignee** | fr...@chromium.org |
| **Created** | 2021-05-13 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/autofill/autofill_keyboard_accessory_adapter.cc;l=127;drc=2f8e0536eb97ce2131e7a74e3ca06077aa0b64b3;bpv=1;bpt=1>  

bool AutofillKeyboardAccessoryAdapter::RemoveSuggestion(int index) {  

DCHECK(view\_) << "RemoveSuggestion called before a View was set!";  

std::u16string title, body;  

if (!GetRemovalConfirmationText(index, &title, &body))  

return false;

view\_->ConfirmDeletion(  

title, body,  

base::BindOnce(&AutofillKeyboardAccessoryAdapter::OnDeletionConfirmed, //[1]  

weak\_ptr\_factory\_.GetWeakPtr(), index));  

return true;  

}

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/autofill/autofill_keyboard_accessory_adapter.cc;drc=2f8e0536eb97ce2131e7a74e3ca06077aa0b64b3;bpv=1;bpt=1;l=216>  

void AutofillKeyboardAccessoryAdapter::OnDeletionConfirmed(int index) {  

if (controller\_)  

controller\_->RemoveSuggestion(OffsetIndexFor(index)); //[2]  

}

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/autofill/autofill_popup_controller_impl.cc;drc=2f8e0536eb97ce2131e7a74e3ca06077aa0b64b3;bpv=1;bpt=1;l=352>

bool AutofillPopupControllerImpl::RemoveSuggestion(int list\_index) {  

if (!delegate\_->RemoveSuggestion(suggestions\_[list\_index].value, //[3]  

suggestions\_[list\_index].frontend\_id)) {  

return false;  

}

// Remove the deleted element.  

suggestions\_.erase(suggestions\_.begin() + list\_index); //[4]

selected\_line\_.reset();

if (HasSuggestions()) {  

delegate\_->ClearPreviewedForm();  

OnSuggestionsChanged();  

} else {  

Hide(PopupHidingReason::kNoSuggestions);  

}

return true;  

}

AutofillKeyboardAccessoryAdapter::OnDeletionConfirmed callback hold an `index`, the `index` is used for accessing `suggestions_`[3][4] when user confirm that.  

`suggestions_`'s size can be changed while the confirm dialog is showing, then click the OK button, heap-over-flow occurs.

**VERSION**  

Chrome Version: [Chrome 90.0.4430.210] + [stable]  

Operating System: [Android 8.0.0; SM-G965F Build/R16NW]

**REPRODUCTION CASE**

1. python3 -m http.server
2. visit test.html
3. cache two suggestions "aa" and "bb"
4. click the input control, press a and then hold the second suggestion on the popup, wait a second, click OK button

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [test.html](attachments/test.html) (text/plain, 590 B)
- [tombstone_06](attachments/tombstone_06) (text/plain, 637.4 KB)
- [20210513_132138.mp4](attachments/20210513_132138.mp4) (video/mp4, 7.8 MB)
- [debuginfo.txt](attachments/debuginfo.txt) (text/plain, 16.7 KB)
- [tombstone_03](attachments/tombstone_03) (text/plain, 1.1 MB)
- [20210513_142803.mp4](attachments/20210513_142803.mp4) (video/mp4, 11.5 MB)

## Timeline

### [Deleted User] (2021-05-13)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-05-13)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-05-13)

compile chrome_public_apk and test it on arm64 device.

### xi...@chromium.org (2021-05-13)

Thanks for the report! fhorschig@, could you take a look? Thanks! Assigning high severity due to the interaction required.

[Monorail components: UI>Browser>Autofill]

### sc...@google.com (2021-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-14)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@gmail.com (2021-05-15)

caching suggestions and shrinking `suggestion_`'s size can be done by a compromised renderer, the only interaction required is choosing a suggestion to delete.

### fr...@chromium.org (2021-05-17)

Thanks for the detailed reproduction steps!

This is indeed an issue and (as was demonstrated) affects at least all Android surfaces. The accessory path was mentioned in #1 and is seen in #3 and the dropdown path as seen in #2 doesn't use a callback but stores the index until the dialog confirmation returns [1].

The deletion on Desktop platforms use a different path (e.g. on Linux Shift + Del while focusing a item in the dropdown) and therefore don't seem affected (i.e. because the dropdown is updated with further input and there isn't even a confirmation dialog). I haven't checked what iOS does but it doesn't seem to use any of the involved classes.

I'll start a fix that just aborts the removal operation if the index is out of bounds which should be easy to merge to any branch.


[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/autofill/autofill_popup_view_android.cc;l=142;drc=46bbb9795fcc1934c6cfbec096764f888c4d400a

### gi...@appspot.gserviceaccount.com (2021-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/995e7b9aba32b194962d98b0bf44e8fe03d4011e

commit 995e7b9aba32b194962d98b0bf44e8fe03d4011e
Author: Friedrich Horschig <fhorschig@chromium.org>
Date: Mon May 17 11:17:16 2021

[Android] Fix trying to remove out-of-bounds autofill suggestion

If the suggestions known to the popup controller change but a removal
confirmation is still pending, the index held by the confirmation is out
of date and can either:
* delete an incorrect suggestions or
* cause a crash due to an out-of-bounds access.

This CL only fixes the latter case but might need to be merged.
A proper fix would involve wide-spread changes to the identification
of a selected suggestions (see https://crbug.com/1209792).

Bug: 1208721
Change-Id: Ib5d352b1752583faf01aa28ef61c983f0c655921
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2896977
Commit-Queue: Friedrich [CET] <fhorschig@chromium.org>
Reviewed-by: Marc Treib <treib@chromium.org>
Cr-Commit-Position: refs/heads/master@{#883425}

[modify] https://crrev.com/995e7b9aba32b194962d98b0bf44e8fe03d4011e/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc


### fr...@chromium.org (2021-05-17)

@adetaylor: Can you please help us to figure out which milestone this should go into?
(The bug says M90 but M91 is already cut in two days. And although it's an easy fix, I am not sure merging to M91 would still be accepted.)

### [Deleted User] (2021-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-17)

Requesting merge to stable M90 because latest trunk commit (883425) appears to be after stable branch point (857950).

Requesting merge to beta M91 because latest trunk commit (883425) appears to be after beta branch point (965).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-17)

This bug requires manual review: We are only 7 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-05-17)

Approving merge to M91; please merge to branch 4472.

### gi...@appspot.gserviceaccount.com (2021-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d8cb34212e2383a6b87c2f37060013eb82de1541

commit d8cb34212e2383a6b87c2f37060013eb82de1541
Author: Friedrich Horschig <fhorschig@chromium.org>
Date: Tue May 18 07:57:37 2021

[Android] Fix trying to remove out-of-bounds autofill suggestion

If the suggestions known to the popup controller change but a removal
confirmation is still pending, the index held by the confirmation is out
of date and can either:
* delete an incorrect suggestions or
* cause a crash due to an out-of-bounds access.

This CL only fixes the latter case but might need to be merged.
A proper fix would involve wide-spread changes to the identification
of a selected suggestions (see https://crbug.com/1209792).

(cherry picked from commit 995e7b9aba32b194962d98b0bf44e8fe03d4011e)

Bug: 1208721
Change-Id: Ib5d352b1752583faf01aa28ef61c983f0c655921
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2896977
Commit-Queue: Friedrich [CET] <fhorschig@chromium.org>
Reviewed-by: Marc Treib <treib@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#883425}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2902703
Auto-Submit: Friedrich [CET] <fhorschig@chromium.org>
Commit-Queue: Marc Treib <treib@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1136}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/d8cb34212e2383a6b87c2f37060013eb82de1541/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc


### am...@google.com (2021-05-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-20)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. Excellent work!! 

### ad...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Comment Deleted]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

Hello zhanjiasong@- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ac...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### as...@google.com (2021-06-07)

Marking not applicable for LTS since Android-only issue.

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1208721?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055842)*
