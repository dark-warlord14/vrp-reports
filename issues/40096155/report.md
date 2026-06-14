# Security: Tab sharing UI crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40096155](https://issues.chromium.org/issues/40096155) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia, UI>Browser>Permissions>Prompts |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2019-08-31 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 78.0.3898.0 Canary  

Operating System: All

This is similar to <https://crbug.com/chromium/981202>

**REPRODUCTION CASE**

1. Go to <https://permission.site>
2. Open a new tab
3. Back to <https://permission.site> and click on "Screen Share"
4. Switch "Chrome Tab" and try to share the new tab
5. Open task manager and end process of the new tab.
6. Back to <https://permission.site> then click on "Stop"

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 975.1 KB)
- deleted (application/octet-stream, 0 B)
- [asan-bug999760-r681086.log](attachments/asan-bug999760-r681086.log) (text/plain, 13.0 KB)
- [asan-bug999760-r691930.log](attachments/asan-bug999760-r691930.log) (text/plain, 26.1 KB)

## Timeline

### ch...@gmail.com (2019-08-31)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-09-03)

Reproduced this on a recent ASAN build. Here's the relevant part of the log:

==65157==ERROR: AddressSanitizer: heap-use-after-free on address 0x61900005eb88 at pc 0x00011f03a138 bp 0x7ffeea77dcc0 sp 0x7ffeea77dcb8
READ of size 8 at 0x61900005eb88 thread T0
    #0 0x11f03a137 in infobars::InfoBar::RemoveSelf() infobar.cc:74
    #1 0x12541bffb in TabSharingUIViews::RemoveInfobarsForAllTabs() tab_sharing_ui_views.cc:237
    #2 0x12541c180 in TabSharingUIViews::StopSharing() tab_sharing_ui_views.cc:162
    #3 0x124707c2f in TabSharingInfoBarDelegate::Accept() tab_sharing_infobar_delegate.cc:78
    #4 0x1250d0c33 in ConfirmInfoBar::ButtonPressed(views::Button*, ui::Event const&) confirm_infobar.cc:102
    #5 0x1a0123aca in views::Button::NotifyClick(ui::Event const&) button.cc:515
    #6 0x1a01216be in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) button.cc:443
    #7 0x1a012e522 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) button_controller.cc:47

Setting this to Sev-High (memory corruption in browser process, but it requires a specific user permission to be granted via the screen share chooser).

I can repro on M-78 trunk (r691930) and M-77 Beta (r681086) on macOS, but not on M-76 Stable (r664996). I wasn't able to repro on Windows.

marinaciocea@ can you take a look a this since it may be similar to https://crbug.com/chromium/981202? Thanks!

+engedy@ in case there's a broader issue in how permission infobar lifetimes are handled.

[Monorail components: Blink>GetUserMedia>Tab UI>Browser>Permissions>Prompts]

### ct...@chromium.org (2019-09-03)

Re-uploading ASAN logs to include M-78 and M-77 ones in case there's a difference.

### ma...@chromium.org (2019-09-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2019-09-03)

I have a fix, I'll land it soon.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/215188815131ddd3a27aa2414401506a9b203407

commit 215188815131ddd3a27aa2414401506a9b203407
Author: Marina Ciocea <marinaciocea@chromium.org>
Date: Tue Sep 03 15:06:36 2019

Fix TabSharingUI crash on killing a renderer process.

The TabSharingUI maintains a map of pointers to tab sharing infobars on
all current tabs, that gets updated OnTabStripModelChanged. However,
killing a renderer process does not trigger a tab strip model change
since the tab still exists, but its WebContents is replaced by the sad tab.

Make TabSharingUI observe InfoBarManager for OnInfoBarRemoved events to
remove the infobars from the map, and for TabChangedAt events to
recreate the infobar for tabs that don't display it, i.e. tab that
crashed and got reloaded.
Don't display the infobar on the Sad Tab, because its content cannot be
shared.

Bug: 999760
Change-Id: If33943ee86d409d2c18b93b3e04ef0d3e2cfb559
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1781593
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Marina Ciocea <marinaciocea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#692645}

[modify] https://crrev.com/215188815131ddd3a27aa2414401506a9b203407/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/215188815131ddd3a27aa2414401506a9b203407/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h


### ma...@chromium.org (2019-09-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-09-03)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-77; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-77 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### ma...@chromium.org (2019-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2019-09-03)

Requesting merge for change in https://crbug.com/chromium/999760#c7

### sh...@chromium.org (2019-09-03)

This bug requires manual review: We are only 6 days from stable.
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
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2019-09-03)

1. Does your merge fit within the Merge Decision Guidelines?
Yes, this is a security bug, release blocker, with low complexity fix (https://crbug.com/chromium/999760#c7) and trivial to merge.

2. Links to the CLs you are requesting to merge.
https://crrev.com/c/1781593

3. Has the change landed and been verified on master/ToT?
Yes.

4. Why are these changes required in this milestone after branch?
Security bug fix.

5. Is this a new feature?
No.

6. If it is a new feature, is it behind a flag using finch?
Not a new feature.

### sh...@chromium.org (2019-09-03)

This bug requires manual review: We are only 6 days from stable.
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
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-09-03)

merge approved for M77 branch 3865

### la...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/570baab26c5bf1211d83e9503d595ee348c1d76b

commit 570baab26c5bf1211d83e9503d595ee348c1d76b
Author: Marina Ciocea <marinaciocea@chromium.org>
Date: Tue Sep 03 22:03:46 2019

[M77] Fix TabSharingUI crash on killing a renderer process.

The TabSharingUI maintains a map of pointers to tab sharing infobars on
all current tabs, that gets updated OnTabStripModelChanged. However,
killing a renderer process does not trigger a tab strip model change
since the tab still exists, but its WebContents is replaced by the sad tab.

Make TabSharingUI observe InfoBarManager for OnInfoBarRemoved events to
remove the infobars from the map, and for TabChangedAt events to
recreate the infobar for tabs that don't display it, i.e. tab that
crashed and got reloaded.
Don't display the infobar on the Sad Tab, because its content cannot be
shared.

(cherry picked from commit 215188815131ddd3a27aa2414401506a9b203407)

Bug: 999760
Change-Id: If33943ee86d409d2c18b93b3e04ef0d3e2cfb559
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1781593
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Marina Ciocea <marinaciocea@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#692645}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1781443
Cr-Commit-Position: refs/branch-heads/3865@{#723}
Cr-Branched-From: 0cdcc6158160790658d1f033d3db873603250124-refs/heads/master@{#681094}

[modify] https://crrev.com/570baab26c5bf1211d83e9503d595ee348c1d76b/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/570baab26c5bf1211d83e9503d595ee348c1d76b/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h


### sh...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-05)

Congrats! The Panel decided to reward $500 for this report! 

### na...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2020-07-07)

[Empty comment from Monorail migration]

### be...@google.com (2020-11-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>GetUserMedia]

### be...@google.com (2020-11-05)

[Empty comment from Monorail migration]

[Monorail components: -Blink>GetUserMedia>Tab]

### is...@google.com (2020-11-05)

This issue was migrated from crbug.com/chromium/999760?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GetUserMedia, UI>Browser>Permissions>Prompts]
[Monorail mergedwith: crbug.com/chromium/983264]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096155)*
