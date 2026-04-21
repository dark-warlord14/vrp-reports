# Security: UAF when sending tab to device

| Field | Value |
|-------|-------|
| **Issue ID** | [40056058](https://issues.chromium.org/issues/40056058) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Linux, Windows |
| **Reporter** | de...@gmail.com |
| **Assignee** | vi...@google.com |
| **Created** | 2021-06-01 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

The send tab to self functionality allows a tab to be sent to another device signed into the same account. If there's more than one other device, the list of devices will be shown in a submenu. Then, if the tab to be sent is closed before one of the devices is selected, a use-after-free will occur in the browser process.

**VERSION**  

Chrome Version: Tested on 91.0.4472.77 (stable)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Open the browser and sign into it with an account that's used with at least two other devices.
2. Install the attached extension.
3. Once installed, the extension will open a new window with two tabs.
4. Right-click on the first tab in the tab strip.
5. Five seconds after opening the window, the extension will close the first tab.
6. Once the tab has been closed, select one of the devices under the "Send to your devices" submenu. This will result in a use-after-free in the browser process.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 326 B)
- [manifest.json](attachments/manifest.json) (text/plain, 158 B)

## Timeline

### de...@gmail.com (2021-06-01)

The SendTabToSelfSubMenuModel class holds a pointer to the target WebContents:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.h;l=52;drc=a31b7b3a0c35923cba6e9029391ce684a3f20f38

When one of the devices is selected, the stored WebContents will be accessed in order to send the tab to another device:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.cc;l=124;drc=511d2e61f78efa707c00efe3fbdd712b98fc0ebe

If the WebContents has been destroyed since the menu was shown, that will result in a UAF.

### [Deleted User] (2021-06-01)

[Empty comment from Monorail migration]

### ad...@google.com (2021-06-01)

This is not reproducible on OS X.

The extension works as designed, opening two tabs then closing the first five seconds later. But if the pop up menu is open, the tab does not close.

I'll try on Linux but otherwise I'll have to pass this over to someone with a Windows box.

### ad...@google.com (2021-06-01)

OK, confirmed reproducible on Linux, 91.0.4472.77. As a browser process UaF, this would normally be Critical severity but is downgraded to High by the need for UI interaction.

[Monorail components: UI>Browser>Sharing]

### ad...@google.com (2021-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-01)

[Empty comment from Monorail migration]

### ti...@google.com (2021-06-01)

Hi Kristi, could you please help triage the bug? Thank you!

### ad...@google.com (2021-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-02)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@google.com (2021-06-04)

I can take a look at this. Since I don't see any weak ptrs to web contents on code search, I'm guessing the right solution is observing the "tab closed" event somewhere and destroying SendTabToSelfMenuModel. 

### vi...@google.com (2021-06-04)

Fix sent for review crrev.com/c/2940547

### gi...@appspot.gserviceaccount.com (2021-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4b16a8bea2017486654aca28a361bbb5a0b5ae60

commit 4b16a8bea2017486654aca28a361bbb5a0b5ae60
Author: Victor Hugo Vianna Silva <victorvianna@google.com>
Date: Fri Jun 04 13:49:34 2021

Fix use-after-free in SendTabToSelfSubMenuModel

Observe the WebContents destruction and prevent ExecuteCommand() from
using the destroyed object.

Fixed: 1215029
Change-Id: I5b3ce1657610f68b08af7747e1875e53e0a4e16b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2940547
Commit-Queue: Victor Vianna <victorvianna@google.com>
Commit-Queue: Travis Skare <skare@chromium.org>
Auto-Submit: Victor Vianna <victorvianna@google.com>
Reviewed-by: Travis Skare <skare@chromium.org>
Cr-Commit-Position: refs/heads/master@{#889276}

[modify] https://crrev.com/4b16a8bea2017486654aca28a361bbb5a0b5ae60/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.cc
[modify] https://crrev.com/4b16a8bea2017486654aca28a361bbb5a0b5ae60/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.h


### [Deleted User] (2021-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-05)

Requesting merge to stable M91 because latest trunk commit (889276) appears to be after stable branch point (870763).

Requesting merge to beta M92 because latest trunk commit (889276) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-05)

This bug requires manual review: M92's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@google.com (2021-06-06)

1. Yes
2. crrev.com/c/2940547
3. Yes
4. Yes, M91 too
5. They fix a security vulnerability.
6. No
7. If it is a new feature, is it behind a flag using finch?


### pb...@google.com (2021-06-07)

+amyressler(Security TPM) to make merge decision.

### am...@chromium.org (2021-06-07)

We are doing doing a new m91 stable respin tomorrow or Wednesday. As this had only a little time in Canary, recommending leaving a few more days before merging. This means it misses the release for this week (which was originally to be today but it being pushed to later in the week) and will land in the next security refresh. WDYT, victorvianna@? 
I'll go ahead and add merge approved (for M91, branch 4472), but if there's any concern at all about stability or other issues, please don't merge until later this week. TY.

### vi...@google.com (2021-06-07)

SGTM, I've sent the cherry-pick for approval on crrev.com/c/2944871. I'll land it on Wednesday if nothing comes up.

### vi...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### sr...@google.com (2021-06-07)

Merge approved for M92 branch:4515 please merge asap

Please merge to M92 after this CL gets merged to M91. 

### vi...@google.com (2021-06-09)

Merging both cherry-picks now

### gi...@appspot.gserviceaccount.com (2021-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4261abbb1403732528d36de5645abb788fea2ae5

commit 4261abbb1403732528d36de5645abb788fea2ae5
Author: Victor Hugo Vianna Silva <victorvianna@google.com>
Date: Wed Jun 09 09:00:01 2021

Fix use-after-free in SendTabToSelfSubMenuModel

Observe the WebContents destruction and prevent ExecuteCommand() from
using the destroyed object.

(cherry picked from commit 4b16a8bea2017486654aca28a361bbb5a0b5ae60)

Fixed: 1215029
Change-Id: I5b3ce1657610f68b08af7747e1875e53e0a4e16b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2940547
Commit-Queue: Victor Vianna <victorvianna@google.com>
Commit-Queue: Travis Skare <skare@chromium.org>
Auto-Submit: Victor Vianna <victorvianna@google.com>
Reviewed-by: Travis Skare <skare@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#889276}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944889
Cr-Commit-Position: refs/branch-heads/4515@{#446}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/4261abbb1403732528d36de5645abb788fea2ae5/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.cc
[modify] https://crrev.com/4261abbb1403732528d36de5645abb788fea2ae5/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.h


### gi...@appspot.gserviceaccount.com (2021-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eb6ddec9b4b448ef79c393860fdabfcf59386c57

commit eb6ddec9b4b448ef79c393860fdabfcf59386c57
Author: Victor Hugo Vianna Silva <victorvianna@google.com>
Date: Wed Jun 09 09:09:49 2021

Fix use-after-free in SendTabToSelfSubMenuModel

Observe the WebContents destruction and prevent ExecuteCommand() from
using the destroyed object.

(cherry picked from commit 4b16a8bea2017486654aca28a361bbb5a0b5ae60)

Fixed: 1215029
Change-Id: I5b3ce1657610f68b08af7747e1875e53e0a4e16b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2940547
Commit-Queue: Victor Vianna <victorvianna@google.com>
Commit-Queue: Travis Skare <skare@chromium.org>
Auto-Submit: Victor Vianna <victorvianna@google.com>
Reviewed-by: Travis Skare <skare@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#889276}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944871
Cr-Commit-Position: refs/branch-heads/4472@{#1469}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/eb6ddec9b4b448ef79c393860fdabfcf59386c57/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.cc
[modify] https://crrev.com/eb6ddec9b4b448ef79c393860fdabfcf59386c57/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.h


### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

And another one -- congrats! The VRP Panel has decided to award you $10,000 for this report. Nice work! 

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-17)

[Empty comment from Monorail migration]

### as...@google.com (2021-06-21)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6f74d0a094fa6a758b323f3392cd1b4d7240e991

commit 6f74d0a094fa6a758b323f3392cd1b4d7240e991
Author: Victor Hugo Vianna Silva <victorvianna@google.com>
Date: Tue Jun 22 13:45:15 2021

[M90-LTS] Fix use-after-free in SendTabToSelfSubMenuModel

Observe the WebContents destruction and prevent ExecuteCommand() from
using the destroyed object.

(cherry picked from commit 4b16a8bea2017486654aca28a361bbb5a0b5ae60)

(cherry picked from commit eb6ddec9b4b448ef79c393860fdabfcf59386c57)

Fixed: 1215029
Change-Id: I5b3ce1657610f68b08af7747e1875e53e0a4e16b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2940547
Commit-Queue: Victor Vianna <victorvianna@google.com>
Commit-Queue: Travis Skare <skare@chromium.org>
Auto-Submit: Victor Vianna <victorvianna@google.com>
Reviewed-by: Travis Skare <skare@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#889276}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944871
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1469}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2975450
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1533}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/6f74d0a094fa6a758b323f3392cd1b4d7240e991/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.cc
[modify] https://crrev.com/6f74d0a094fa6a758b323f3392cd1b4d7240e991/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.h


### gi...@appspot.gserviceaccount.com (2021-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/61c58cf2c1558a429daae9624d683ae2468bf386

commit 61c58cf2c1558a429daae9624d683ae2468bf386
Author: Victor Hugo Vianna Silva <victorvianna@google.com>
Date: Tue Jun 22 13:48:53 2021

[M86-LTS] Fix use-after-free in SendTabToSelfSubMenuModel

Observe the WebContents destruction and prevent ExecuteCommand() from
using the destroyed object.

(cherry picked from commit 4b16a8bea2017486654aca28a361bbb5a0b5ae60)

(cherry picked from commit eb6ddec9b4b448ef79c393860fdabfcf59386c57)

Fixed: 1215029
Change-Id: I5b3ce1657610f68b08af7747e1875e53e0a4e16b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2940547
Commit-Queue: Victor Vianna <victorvianna@google.com>
Commit-Queue: Travis Skare <skare@chromium.org>
Auto-Submit: Victor Vianna <victorvianna@google.com>
Reviewed-by: Travis Skare <skare@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#889276}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944871
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1469}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2975449
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1676}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/61c58cf2c1558a429daae9624d683ae2468bf386/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.cc
[modify] https://crrev.com/61c58cf2c1558a429daae9624d683ae2468bf386/chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.h


### as...@google.com (2021-06-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2021-06-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-10)

added as cc for visibility since this is before this issue can be made allpublic 

### [Deleted User] (2021-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1215029?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056058)*
