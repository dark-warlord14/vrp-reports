# Security: After refactor, page can use EyeDropper API to bypass mouse movement/keyboard input requirements for autofill (regression of issue 1287364)

| Field | Value |
|-------|-------|
| **Issue ID** | [40063230](https://issues.chromium.org/issues/40063230) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-02-24 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A page can make a user select an autofill item with two consecutive clicks (three in limited cases), without moving their mouse or pressing keyboard keys after the autofill prompt appears.

This is a regression of <https://crbug.com/chromium/1287364> due to refactor of autofill code tracked in <https://crbug.com/chromium/1411172>, specifically commit 7240cc8e2bc7b6a81307837d4c68fcad4f856423.

(The commit above was reverted briefly in commit aa663d384c34e606f145accedb07c2e42f07971d and relanded in commit 45f4e2501b63e1bbb0d4bd2944a81b3009ceb474 for reasons unrelated to the report.)

The 500ms fix from <https://crbug.com/chromium/1279268> does not seem to mitigate this vulnerability, even though in theory it should still be mitigated (as noted by commit author). I'm not certain why it isn't mitigated, but repro is reliable.

Using the EyeDropper API (enabled by default in Chrome 95) bypasses security checks that prevent unintentional autofill selection. It seems that calling EyeDropper.open() and immediately closing the eye dropper is sufficient to bypass the 500ms mitigation and other mitigations.

**VERSION**  

Chrome Version:  

Repro (AFTER the patch above): 112.0.5614.0 Canary, Chromium snapshot builds 1108872 and 1109002  

No repro (BEFORE the patch above): 112.0.5612.0 Canary, 110.0.5481.104 Stable, Chromium snapshot build 1108853

Operating System: Windows 10 Version 21H2 (Build 19044.2604)

The bisect above confirms issue was introduced by commit 7240cc8e2bc7b6a81307837d4c68fcad4f856423.  

Chromium snapshot builds obtained from <https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/>

**REPRODUCTION CASE**  

PoC for address:  

Prerequisite: Have at least one address with an email address in chrome://settings/addresses

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-eye-dropper-refactor.html>
2. Click the same place twice in a row, anywhere in the page.

PoC for credit card:  

Prerequisite: Have at least one credit card in chrome://settings/payments

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-eye-dropper-refactor.html?creditcard>
2. (Same as prior PoC, click twice in a row)

For all PoCs:  

Observed: Autofilled data is provided to page, because page can cause user to select an autofill item without any mouse movement or keyboard input.  

Expected: Autofilled data is \*not\* provided to page, because page cannot cause user to select an autofill item without user intentionally moving mouse or using keyboard to select item.

Attached screen recording using 112.0.5614.0 Canary.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [autofill-eye-dropper-refactor.html](attachments/autofill-eye-dropper-refactor.html) (text/plain, 3.5 KB)
- [autofill-eye-dropper-refactor-canary.mp4](attachments/autofill-eye-dropper-refactor-canary.mp4) (video/mp4, 996.3 KB)

## Timeline

### [Deleted User] (2023-02-24)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-25)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-02-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-25)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@google.com (2023-02-27)

[Empty comment from Monorail migration]

### jk...@google.com (2023-02-27)

Interesting. I just checked the PoC on Linux, Mac & Windows.
a) The PoC does not work on either Linux or Mac
b) The PoC does work on Windows. It seems that opening the eye dropper leads to a delay in the popup showing, but the mouse clicks are forwarded to the popup nonetheless. Therefore, even if the clicks were less than 500 ms apart, they get registered as being further apart than 500 ms.

### jk...@google.com (2023-02-27)

[Empty comment from Monorail migration]

### jk...@google.com (2023-02-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2611dbf43c03fad48ad279cbe1427bbf7b8e85d2

commit 2611dbf43c03fad48ad279cbe1427bbf7b8e85d2
Author: Jan Keitel <jkeitel@google.com>
Date: Mon Feb 27 17:06:57 2023

Reintroduce paint checks for PopupCellView.

Bug: 1411172, 1418837
Change-Id: I60d7639849d9efb912c667663a23e2bf41749ced
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4291660
Reviewed-by: Christoph Schwering <schwering@google.com>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Cr-Commit-Position: refs/heads/main@{#1110396}

[modify] https://crrev.com/2611dbf43c03fad48ad279cbe1427bbf7b8e85d2/chrome/browser/ui/views/autofill/popup/popup_cell_view_unittest.cc
[modify] https://crrev.com/2611dbf43c03fad48ad279cbe1427bbf7b8e85d2/chrome/browser/ui/views/autofill/popup/popup_cell_view.cc
[modify] https://crrev.com/2611dbf43c03fad48ad279cbe1427bbf7b8e85d2/chrome/browser/ui/views/autofill/popup/popup_cell_view.h
[modify] https://crrev.com/2611dbf43c03fad48ad279cbe1427bbf7b8e85d2/chrome/browser/ui/views/autofill/popup/popup_view_views_unittest.cc


### al...@alesandroortiz.com (2023-02-27)

Thanks for fixing, jkeitel@!

OS labels should be updated if it only repros on Windows. A comment by schwering@ in original issue also indicated Windows-only repro: https://bugs.chromium.org/p/chromium/issues/detail?id=1287364#c10

Verified as fixed on Windows 10 Version 21H2 (Build 19044.2604) using snapshot build 1110448 from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/

### jk...@google.com (2023-02-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/73db4bddcce5e5b9dd180ddbd0081c09dd1ef3d6

commit 73db4bddcce5e5b9dd180ddbd0081c09dd1ef3d6
Author: Jan Keitel <jkeitel@google.com>
Date: Tue Feb 28 13:01:32 2023

Reset threshold for accepting Autofill popup entries on view update.

Currently, the Autofill controller measures when a popup view is shown
the first time and measures against this point in time when checking
whether the necessary time threshold is met in "AcceptSuggestion".
This CL makes the change to update the time measurement also if the
view is updated. In this way, the threshold cannot be circumvented
by showing the popup in one part of the screen and then clicking
somewhere else so that the popup's coordinates are updated.

Bug: 1411172, 1418837
Change-Id: Ice0acc8d11fddf0d8d32a1a22b40e15c6941285a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4295697
Commit-Queue: Jan Keitel <jkeitel@google.com>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1110907}

[modify] https://crrev.com/73db4bddcce5e5b9dd180ddbd0081c09dd1ef3d6/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/73db4bddcce5e5b9dd180ddbd0081c09dd1ef3d6/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc


### [Deleted User] (2023-03-01)

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/93489522de64cc69af693587e655e057f27a0501

commit 93489522de64cc69af693587e655e057f27a0501
Author: Jan Keitel <jkeitel@google.com>
Date: Wed Mar 01 17:02:37 2023

Reintroduce paint checks for PopupCellView.

(cherry picked from commit 2611dbf43c03fad48ad279cbe1427bbf7b8e85d2)

Bug: 1411172, 1418837
Change-Id: I60d7639849d9efb912c667663a23e2bf41749ced
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4291660
Reviewed-by: Christoph Schwering <schwering@google.com>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1110396}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4295831
Cr-Commit-Position: refs/branch-heads/5615@{#97}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/93489522de64cc69af693587e655e057f27a0501/chrome/browser/ui/views/autofill/popup/popup_cell_view_unittest.cc
[modify] https://crrev.com/93489522de64cc69af693587e655e057f27a0501/chrome/browser/ui/views/autofill/popup/popup_cell_view.cc
[modify] https://crrev.com/93489522de64cc69af693587e655e057f27a0501/chrome/browser/ui/views/autofill/popup/popup_cell_view.h
[modify] https://crrev.com/93489522de64cc69af693587e655e057f27a0501/chrome/browser/ui/views/autofill/popup/popup_view_views_unittest.cc


### jk...@google.com (2023-03-01)

Requesting merge approval for the other, small fix (https://crbug.com/chromium/1418837#c14).

### [Deleted User] (2023-03-01)

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2023-03-01)

jkeitel@: Can this be marked as fixed, or are there additional fixes pending? Thanks for the additional fix in https://crbug.com/chromium/1418837#c14.

### gi...@appspot.gserviceaccount.com (2023-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3bd4ba54c78a03fb90f5d79da99f0cb0f813f79a

commit 3bd4ba54c78a03fb90f5d79da99f0cb0f813f79a
Author: Jan Keitel <jkeitel@google.com>
Date: Thu Mar 02 07:34:00 2023

Reset threshold for accepting Autofill popup entries on view update.

Currently, the Autofill controller measures when a popup view is shown
the first time and measures against this point in time when checking
whether the necessary time threshold is met in "AcceptSuggestion".
This CL makes the change to update the time measurement also if the
view is updated. In this way, the threshold cannot be circumvented
by showing the popup in one part of the screen and then clicking
somewhere else so that the popup's coordinates are updated.

(cherry picked from commit 73db4bddcce5e5b9dd180ddbd0081c09dd1ef3d6)

Bug: 1411172, 1418837
Change-Id: Ice0acc8d11fddf0d8d32a1a22b40e15c6941285a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4295697
Commit-Queue: Jan Keitel <jkeitel@google.com>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1110907}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4299449
Cr-Commit-Position: refs/branch-heads/5615@{#122}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/3bd4ba54c78a03fb90f5d79da99f0cb0f813f79a/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/3bd4ba54c78a03fb90f5d79da99f0cb0f813f79a/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc


### jk...@google.com (2023-03-02)

Now that the second CL has been merged, I am marking it as fixed.

### [Deleted User] (2023-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations, Alesandro! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-04-22)

Thanks for the reward!

### [Deleted User] (2023-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-07-06)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-13)

The issue was introduced in M112.

### vo...@google.com (2023-07-27)

Merged before M114.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1418837?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063230)*
