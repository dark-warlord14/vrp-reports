# UAF in AutofillPopupControllerImpl::HandleKeyPressEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40058131](https://issues.chromium.org/issues/40058131) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@gmail.com |
| **Assignee** | sc...@google.com |
| **Created** | 2021-12-06 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36

Steps to reproduce the problem:
1.php -S 0.0.0.0:8081 (python not support post so use php)
2.out/asan/chrome http://localhost:8081/poc1.html
3.click the form text and press pageup to trigger the UAF

What is the expected behavior?

What went wrong?
If user press pageup to call AutofillPopupControllerImpl::HandleKeyPressEvent when mouse is locked.  AutofillPopupControllerImpl will be delete through following chains.

AutofillPopupControllerImpl::HandleKeyPressEvent->
AutofillPopupControllerImpl::SetSelectedLine[1]->
AutofillPopupControllerImpl::Hide->
AutofillPopupControllerImpl::HideViewAndDie()->
delete this

And UAF will happen when accessing selected_line_ through [2]. Note in release version. It will finally call delete this again. Double free will Make this bug more exploitable.
I test it in the newest version chrome and find miracleptr will not mitigate this UAF because the this pointer AutofillPopupControllerImpl owned is still raw pointer rather then raw_ptr.

bool AutofillPopupControllerImpl::HandleKeyPressEvent(
    const content::NativeWebKeyboardEvent& event) {
  switch (event.windows_key_code) {
    case ui::VKEY_UP:
      SelectPreviousLine();
      return true;
    case ui::VKEY_DOWN:
      SelectNextLine();
      return true;
    case ui::VKEY_PRIOR:  // Page up.
      // Set no line and then select the next line in case the first line is not
      // selectable.
      SetSelectedLine(absl::nullopt);----------------------------------------------- [1]
      SelectNextLine(); -------------------------------------------------- [2]
      return true;
    case ui::VKEY_NEXT:  // Page down.
      SetSelectedLine(GetLineCount() - 1);
      return true;
    case ui::VKEY_ESCAPE:
      Hide(PopupHidingReason::kUserAborted);
      return true;
    case ui::VKEY_DELETE:
      return (event.GetModifiers() &
              content::NativeWebKeyboardEvent::kShiftKey) &&
             RemoveSelectedLine();
    case ui::VKEY_TAB:
      // A tab press should cause the selected line to be accepted, but still
      // return false so the tab key press propagates and changes the cursor
      // location.
      AcceptSelectedLine();
      return false;
    case ui::VKEY_RETURN:
      return AcceptSelectedLine();
    default:
      return false;
  }
}

Did this work before? N/A 

Chrome version: 96.0.4664.45  Channel: stable
OS Version:

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 27.8 KB)
- [poc1.html](attachments/poc1.html) (text/plain, 932 B)
- [patch.diff](attachments/patch.diff) (text/plain, 998 B)

## Timeline

### [Deleted User] (2021-12-06)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-06)

Another UaF in this method - a previous one came up last year in https://crbug.com/chromium/1133671

[Monorail components: UI>Browser>Autofill]

### do...@chromium.org (2021-12-06)

schwering/battre, do you mind taking a look? Also cc'ing jdoerrie from https://crbug.com/chromium/1133671

### [Deleted User] (2021-12-06)

[Empty comment from Monorail migration]

### ro...@gmail.com (2021-12-06)

I also upload the patch.diff for this bug. thank you!

### ro...@gmail.com (2021-12-06)

And sorry for my mistak. I test it on the newest version chromium rather than on the newest version chrome. I think it can't be triggered in stable version.

### sc...@google.com (2021-12-06)

Thanks a lot for the detailed report and the patch. I'll look into this now.

Your patch looks good to m; additionally we'd need to check for deallocation between SetSelectedLine() and SetSelectedLine().

In addition I'll revisit the more fundamental fix ideas we discussed a few weeks ago (defer deletion and/or WeakPtrs), which we may need to land behind a feature..

### do...@chromium.org (2021-12-06)

Thanks for the patch and clarification on impact. Looks like the vulnerability was introduced in https://chromium-review.googlesource.com/c/chromium/src/+/3297919, which is in M98. Updating labels to match.

### [Deleted User] (2021-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@google.com (2021-12-10)

The fix CL https://chromium-review.googlesource.com/c/chromium/src/+/3318616 landed in Canary 98.0.4755.0. For some reason, Git Watcher didn't leave a comment.

### sc...@google.com (2021-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-11)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M98. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-11)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-12-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf3e0d913e2374e2d783ceecbccc4b400d26fa39

commit cf3e0d913e2374e2d783ceecbccc4b400d26fa39
Author: Christoph Schwering <schwering@google.com>
Date: Wed Dec 08 03:50:33 2021

[Autofill] Check for self-destruction after selecting a suggestions.

This UAF was introduced in crrev.com/c/3297919 by hiding the popup
in SetSelectedLine() if the window holds a pointer lock. Since hiding
the popup deletes the popup, |this| must not be accessed afterwards.

This CL is a quick fix that adds checks after calling SetSelectedLine().
The followup CLs will make this and other checks for weak_this
redundant: crrev.com/c/3317979, crrev.com/c/3318297.

Bug: 1276850, 1239496
Change-Id: I79ce4df48ae969ba13033640f2ac2ac8c322373b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3318616
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Auto-Submit: Christoph Schwering <schwering@google.com>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#949363}

[modify] https://crrev.com/cf3e0d913e2374e2d783ceecbccc4b400d26fa39/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/cf3e0d913e2374e2d783ceecbccc4b400d26fa39/chrome/browser/ui/autofill/autofill_popup_controller_impl.h


### sc...@google.com (2021-12-11)

1. yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/3318616
3. yes
4. no
5. n/a
6. no

Note that the CL https://chromium-review.googlesource.com/c/chromium/src/+/3318616 has landed in Canary 98.0.4755.0.

I've filed https://bugs.chromium.org/p/monorail/issues/detail?id=10412 about the missing Git Watcher comment.

### sc...@google.com (2021-12-11)

(#c18 is the belated Git Watcher comment. I triggered it by leaving a comment the CL as per https://bugs.chromium.org/p/chromium/issues/detail?id=1250083#c2.)

### ad...@google.com (2021-12-13)

https://crbug.com/chromium/1276850#c18 landed prior to M98 branch point (950365) so I don't think there's anything to merge here.

### [Deleted User] (2021-12-13)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M98, which branched on 2021-12-09 (Chromium branch: 4758, Chromium branch position: 950365)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2021-12-13)

+adetaylor@, PTAL https://crbug.com/chromium/1276850#c22. Thank you. 

### sc...@google.com (2021-12-13)

Note that the patch landed before the branch point (#c12). I suppose https://crbug.com/chromium/1276850#c22 is a false positive. 

### ad...@chromium.org (2021-12-13)

Yep per https://crbug.com/chromium/1276850#c21 nothing to do here. I don't know what bit of sheriffbot said https://crbug.com/chromium/1276850#c22, that's not one of our normal security related merge rules!

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. Thank you for your report and excellent work! 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@google.com (2022-03-25)

Cleanup reminder: we fix the UAF by checking in [1] whether the popup has been deleted. Once AutofillDelayPopupControllerDeletion is launched (https://crbug.com/chromium/1277218), this is no longer necessary. Therefore, we can remove SetSelectedLineHelper().

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/autofill/autofill_popup_controller_impl.cc;l=285;drc=191ad533845b7c475d946caaba1724a12edfcf6b

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1276850?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058131)*
