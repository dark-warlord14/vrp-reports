# heap-use-after-free in DevToolsWindow::ActivateWindow

| Field | Value |
|-------|-------|
| **Issue ID** | [40059395](https://issues.chromium.org/issues/40059395) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Windows |
| **Reporter** | xp...@gmail.com |
| **Assignee** | wo...@chromium.org |
| **Created** | 2022-04-16 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Enable chrome://flags/#quick-commands
2. Open to a page and open devtools undocked.
3. While viewing devtools window, execute "Ctrl+Space" to open quick commands.  
   
   4: Type "Move tabs to window". Move tab that you opened devtools from.  
   
   5: Click "Select an element in the page to inspect it ..." button in upper right corner.  
   
   6: Click tab in tab bar and select an element within the page. UAF ensues.

**Problem Description:**  

Similar if not the same as: <https://crbug.com/chromium/1283681>

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.5008.0 (Developer Build) (64-bit) \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 14.9 KB)
- [6VbKQ0rARV.mp4](attachments/6VbKQ0rARV.mp4) (video/mp4, 1.7 MB)
- [patch.txt](attachments/patch.txt) (text/plain, 660 B)

## Timeline

### xp...@gmail.com (2022-04-17)

Confirmed on latest Chrome stable 100.0.4896.127.

### xp...@gmail.com (2022-04-19)

Possible patch:

### dt...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

Assigning per the previous bug. Severity medium at best due to the gestures involved.

[Monorail components: Platform>DevTools]

### wo...@chromium.org (2022-04-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-20)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-04-26)

Marking Impact=None as the quick commands feature is disabled by default.

### lg...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/79263428f32457d6b41938e112067a141750f7a6

commit 79263428f32457d6b41938e112067a141750f7a6
Author: Wolfgang Beyer <wolfi@chromium.org>
Date: Mon May 02 08:55:57 2022

[DevTools] Disallow quick commands for DevTools windows

Bug: 1316889
Change-Id: I67b34a37dfd503b4cf56e31adf6fbef8aa8db1b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3596189
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Wolfgang Beyer <wolfi@chromium.org>
Reviewed-by: Leonard Grey <lgrey@chromium.org>
Cr-Commit-Position: refs/heads/main@{#998284}

[modify] https://crrev.com/79263428f32457d6b41938e112067a141750f7a6/chrome/browser/ui/views/commander_frontend_views.cc


### wo...@chromium.org (2022-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

[Empty comment from Monorail migration]

### wo...@chromium.org (2022-05-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-03)

Merge review required: M102 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wo...@chromium.org (2022-05-03)

1. Why does your merge fit within the merge criteria for these milestones?
Security issue
2. What changes specifically would you like to merge? Please link to Gerrit.
https://crrev.com/c/3596189
3. Have the changes been released and tested on canary?
Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
-
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No

### sr...@google.com (2022-05-09)

Merge approved for M102 branch: pls refer to go/chrome-branches for more info

### sr...@google.com (2022-05-09)

Please complete your merge to M102 branch before 2pm PT ( May 10 tuesday) so this change can be part of the beta release this week, I would like to get all changes beta coverage asap as we are approaching stable RC cut next week

### gi...@appspot.gserviceaccount.com (2022-05-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca30b6c0c0becea7a1d20d275327055a92d3d573

commit ca30b6c0c0becea7a1d20d275327055a92d3d573
Author: Wolfgang Beyer <wolfi@chromium.org>
Date: Tue May 10 08:42:04 2022

[DevTools] Disallow quick commands for DevTools windows

(cherry picked from commit 79263428f32457d6b41938e112067a141750f7a6)

Bug: 1316889
Change-Id: I67b34a37dfd503b4cf56e31adf6fbef8aa8db1b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3596189
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Wolfgang Beyer <wolfi@chromium.org>
Reviewed-by: Leonard Grey <lgrey@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#998284}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3637058
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Auto-Submit: Wolfgang Beyer <wolfi@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#609}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/ca30b6c0c0becea7a1d20d275327055a92d3d573/chrome/browser/ui/views/commander_frontend_views.cc


### am...@google.com (2022-05-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-24)

Congratulations! The VRP Panel has decided to award you $3,000 for this report based on this issue not being web accessible and the amount of user interaction required to trigger. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### xp...@gmail.com (2022-07-07)

@amyressler@chromium.org Can my credit information be modified to include my twitter handle? It would be: Sven Dysthe (@svn_dy) 

### am...@chromium.org (2022-07-07)

Sure thing, Sven! Updated in our database and will be reflected in security fix notes the next time this or any fixes from your reports are released in a Stable channel release. 

### [Deleted User] (2022-08-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-08)

This issue was migrated from crbug.com/chromium/1316889?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059395)*
