# Security: Download notification can hide 'Press Esc to exit fullscreen' warning

| Field | Value |
|-------|-------|
| **Issue ID** | [40060572](https://issues.chromium.org/issues/40060572) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Bubbles>Download, UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | bh...@google.com |
| **Created** | 2022-08-12 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 106.0.5235.0 (Official Build) canary  

Operating System: Windows 10

**REPRODUCTION CASE**

- Enable chrome://flags/#download-bubble

1. Open poc.html
2. Click anywhere

Note that the download notification can replace the "Press Esc to exit full screen" warning before the victim realizes they're in full screen mode and this allows the page to impersonate other origins.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 295 B)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 118.5 KB)
- [Screenshot (2).png](attachments/Screenshot (2).png) (image/png, 76.0 KB)

## Timeline

### [Deleted User] (2022-08-12)

[Empty comment from Monorail migration]

### bh...@google.com (2022-08-12)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Downloads]

### th...@chromium.org (2022-08-12)

Could potentially be High severity, but tentatively setting as Medium since the message is still telling you to press Esc.

### [Deleted User] (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bh...@google.com (2022-08-12)

I think it should Security_Severity_None as the feature is disabled by default.

### bh...@google.com (2022-08-12)

Security_Impact-None

### th...@chromium.org (2022-08-12)

We're not setting Security_Impact-None because the field trial configuration has been switched on. (Per the recommendations here: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/security-labels.md#when-to-use-security_impact_none-toc_security_impact_none )

### [Deleted User] (2022-08-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-08-16)

[Bulk Edit] We are cutting M105 Stable RC on Aug-23rd which is 1 week away, Since this bug has been marked as Releaseblock-Stable request to evaluate the bug asap,  if this is indeed a Stable blocker please get the fix landed on trunk on or before this friday for multiple canary coverage If not, please remove the RBS label. Thank you.

### bh...@google.com (2022-08-18)

CL out for review at https://crrev.com/c/3837016

### gi...@appspot.gserviceaccount.com (2022-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8

commit 6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8
Author: Rohit Bhatia <bhatiarohit@google.com>
Date: Thu Aug 18 16:34:47 2022

[DownloadBubble] Update full screen notification text

Update the full screen notification for downloads if the notification is
overriding another notification.

Screencast: http://go/scrcast/NjIyNTkwOTYzNjkyMzM5MnxhNDU4YTFlNy1kYw

POC screencast: http://go/scrcast/NDg2ODIzMjIyMjYwNTMxMnw0MGJkNzAwMi0wMg

Bug: 1352388
Change-Id: Ibfaeff033258247c8354740090d8d84d80655009
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3837016
Commit-Queue: Rohit Bhatia <bhatiarohit@google.com>
Reviewed-by: Peter Boström <pbos@chromium.org>
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1036641}

[modify] https://crrev.com/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8/chrome/browser/ui/exclusive_access/exclusive_access_manager.cc
[modify] https://crrev.com/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8/chrome/browser/ui/exclusive_access/exclusive_access_bubble_type.h
[add] https://crrev.com/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8/components/fullscreen_control_strings_grdp/IDS_FULLSCREEN_PRESS_TO_SEE_DOWNLOADS_AND_EXIT.png.sha1
[modify] https://crrev.com/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8/chrome/browser/download/bubble/download_display_controller.cc
[modify] https://crrev.com/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8/chrome/browser/ui/exclusive_access/exclusive_access_bubble_type.cc
[modify] https://crrev.com/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8/chrome/browser/ui/views/exclusive_access_bubble_views.cc
[modify] https://crrev.com/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8/chrome/browser/ui/views/exclusive_access_bubble_views.h
[modify] https://crrev.com/6bfaa7b0640b59e7da1fc8ecc256daa35bd112e8/components/fullscreen_control_strings.grdp


### ch...@gmail.com (2022-08-18)

Thanks for the fix!

### bh...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-20)

Requesting merge to beta M105 because latest trunk commit (1036641) appears to be after beta branch point (1027018).

Not requesting merge to dev (M106) because latest trunk commit (1036641) appears to be prior to dev branch point (1036826). If this is incorrect, please replace the Merge-NA-106 label with Merge-Request-106. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-20)

Merge review required: M105 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bh...@google.com (2022-08-22)

1. Yes, it is a release blocking security bug.
2.  https://chromium-review.googlesource.com/c/chromium/src/+/3837016
3. Yes
4. Yes, and yes. Active in stable 1%
5. N/A
6. Run the poc attached above. You should see the string "Press {something} to exit full screen and see download."

### am...@chromium.org (2022-08-22)

Hi Rohit, thanks for your work on this because this strings translations has not been completed and status is still pending, I'm going to hold off on approving merge for this fix. Please be prepared to land/merge the CL to rollback field trial on this feature to 0% for 105 just in case. Thank you. 

### am...@chromium.org (2022-08-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-22)

(apologies for the label confusion, I had already updated as approved until I checked in on the status of the strings translations task) 

### bh...@google.com (2022-08-22)

Updating platforms. While the bug exists for Linux, Mac, Windows, and Lacros, the field trial is active only on Windows.

### bh...@google.com (2022-08-23)

Rolling back 1% experiment in http://cl/468520767

### bh...@google.com (2022-08-23)

Finch experiment is rolled back to beta only. Removing RelaseBlock-Stable label

### xi...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Bubbles>Download]

### am...@chromium.org (2022-08-31)

Since the string translations has been completed, approving for merge to 105. If you wish to re-enable the field trial experiment during 105/stable, please feel free to merge this fix to branch 5195 at your earliest convenience. If the goal is to re-enable experimentation in 106, merging to 105 is not needed and feel free to remove the merge approval label accordingly. 


### bh...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### bh...@google.com (2022-08-31)

Thanks for checking back!

### am...@google.com (2022-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-30)

Congratulations, Khalil! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1352388?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Bubbles>Download, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060572)*
