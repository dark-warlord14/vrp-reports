# Security: Heap-use-after-free in ~ExtensionUninstallDialogViews

| Field | Value |
|-------|-------|
| **Issue ID** | [40058934](https://issues.chromium.org/issues/40058934) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | me...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2022-03-02 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36

Steps to reproduce the problem:
1. download asan-linux-release-976045.zip and unzip
2. install the extension
3. open 'chrome://apps', select to remove the apps
4. close the 'chrome://apps' tab by the Dock. See the video for more informations.

What is the expected behavior?

What went wrong?
When close the chrome://apps, the `AppLauncherHandler` will be destructed first, then the `ExtensionUninstallDialog` will be destructed. But `ExtensionUninstallDialog` hold a raw ptr to `AppLauncherHandler`, the `extensions::ExtensionUninstallDialog::Delegate`[1]. So when `ExtensionUninstallDialog` is destructed, UAF occurs.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/extension_uninstall_dialog.h;l=163;bpv=1;bpt=0;drc=9e30513cb5818b899ef42ad3a9f26eb2dabdffc9

Did this work before? N/A 

Chrome version: 98.0.4758.102  Channel: n/a
OS Version:

## Attachments

- [background.js](attachments/background.js) (text/plain, 0 B)
- [manifest.json](attachments/manifest.json) (text/plain, 227 B)
- [asan.txt](attachments/asan.txt) (text/plain, 24.8 KB)
- [video.webm](attachments/video.webm) (video/webm, 547.6 KB)

## Timeline

### [Deleted User] (2022-03-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-02)

Simple "fix" is probably to move `std::unique_ptr<extensions::ExtensionUninstallDialog> extension_uninstall_dialog_` to be the last field with a comment that it calls back into `this`.

It's a bit sketchy of course :)

While this is a UaF in the browser, I think it'd be difficult to exploit in practice, so I'm going to label this as medium.

[Monorail components: UI>Browser>NewTabPage]

### [Deleted User] (2022-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/64f02e6e38d192a234a1d4f873d01e05aa85a367

commit 64f02e6e38d192a234a1d4f873d01e05aa85a367
Author: Evan Stade <estade@chromium.org>
Date: Thu Mar 03 07:20:05 2022

Fix UAF in apps page.

Bug: 1302157
Change-Id: I078d20add15bccec84ba13c384c191fd3b60c85b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3498946
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#977002}

[modify] https://crrev.com/64f02e6e38d192a234a1d4f873d01e05aa85a367/chrome/browser/ui/webui/ntp/app_launcher_handler.cc
[modify] https://crrev.com/64f02e6e38d192a234a1d4f873d01e05aa85a367/chrome/browser/ui/webui/ntp/app_launcher_handler.h
[modify] https://crrev.com/64f02e6e38d192a234a1d4f873d01e05aa85a367/chrome/browser/ui/webui/ntp/app_launcher_handler_unittest.cc


### es...@chromium.org (2022-03-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-05)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-03-07)

based on labels I'm guessing we want to cherry pick the fix back to 99?

### [Deleted User] (2022-03-07)

Merge review required: M99 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2022-03-07)

1. Why does your merge fit within the merge criteria for these milestones?

medium security bug

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3498946

3. Have the changes been released and tested on canary?

yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

no

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

non cros bug

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

no

### es...@chromium.org (2022-03-07)

(manually tested with asan-linux-release-977999 )

### am...@chromium.org (2022-03-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-07)

Hi estade@ thanks for landing this fix. Yes, we'll want to CP this to M99, but also to M100 since it was landed on canary and dev past 100 branching. In the future, once you've resolved a security bug, please update as Fixed immediately upon submitting the fix CL and sheriffbot will update with appropriate merge labels accordingly 

### am...@chromium.org (2022-03-07)

merge approved to M100, please merge to branch 4896 at your earliest convenience 
merge approved to M99, please merge to branch 4844 NLT noon PST, Thursday 10 March so this fix can be included in the next stable respin -- thank you! 

### am...@chromium.org (2022-03-07)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-03-07)

> In the future, once you've resolved a security bug, please update as Fixed immediately upon submitting the fix CL and sheriffbot will update with appropriate merge labels accordingly

I did this in https://crbug.com/chromium/1302157#c6 and sheriffbot did not mention anything about merging.

### sr...@google.com (2022-03-07)

This bug is approved for M100 merge, please complete your merge asap so this can be included in the beta release this week. Beta RC will be cut tomorrow ( tuesday) March 8th at 3pm PST [Bulk Update]

### gi...@appspot.gserviceaccount.com (2022-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/db2176c1d001ff4f52026c0920c2393ee24115b7

commit db2176c1d001ff4f52026c0920c2393ee24115b7
Author: Evan Stade <estade@chromium.org>
Date: Mon Mar 07 20:50:22 2022

Fix UAF in apps page.

(cherry picked from commit 64f02e6e38d192a234a1d4f873d01e05aa85a367)

Bug: 1302157
Change-Id: I078d20add15bccec84ba13c384c191fd3b60c85b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3498946
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#977002}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3508256
Auto-Submit: Evan Stade <estade@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4896@{#349}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/db2176c1d001ff4f52026c0920c2393ee24115b7/chrome/browser/ui/webui/ntp/app_launcher_handler.cc
[modify] https://crrev.com/db2176c1d001ff4f52026c0920c2393ee24115b7/chrome/browser/ui/webui/ntp/app_launcher_handler.h
[modify] https://crrev.com/db2176c1d001ff4f52026c0920c2393ee24115b7/chrome/browser/ui/webui/ntp/app_launcher_handler_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e400cb1bdffdc10f87cf648481d3eadf96fd8496

commit e400cb1bdffdc10f87cf648481d3eadf96fd8496
Author: Evan Stade <estade@chromium.org>
Date: Mon Mar 07 21:13:06 2022

Fix UAF in apps page.

(cherry picked from commit 64f02e6e38d192a234a1d4f873d01e05aa85a367)

Bug: 1302157
Change-Id: I078d20add15bccec84ba13c384c191fd3b60c85b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3498946
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#977002}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3508332
Auto-Submit: Evan Stade <estade@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4844@{#999}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/e400cb1bdffdc10f87cf648481d3eadf96fd8496/chrome/browser/ui/webui/ntp/app_launcher_handler.cc
[modify] https://crrev.com/e400cb1bdffdc10f87cf648481d3eadf96fd8496/chrome/browser/ui/webui/ntp/app_launcher_handler.h
[modify] https://crrev.com/e400cb1bdffdc10f87cf648481d3eadf96fd8496/chrome/browser/ui/webui/ntp/app_launcher_handler_unittest.cc


### am...@chromium.org (2022-03-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-11)

re: https://crbug.com/chromium/1302157#c17: hi estade@, sheriffbot runs the merge labeling rules every 24 hours at the same time, you were about two hours early from when the bot would have woken up and reported to work :) 

### am...@google.com (2022-03-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Congratulations! The VRP Panel has decided to award you $3,000 for this report amount. The Panel assess security impact and exploitation potential and determined this reward amount due to the high reliance on specific and direct user interaction required to trigger this issue. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xp...@gmail.com (2022-06-15)

Can the attachments in the original report be undeleted?

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1302157?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058934)*
