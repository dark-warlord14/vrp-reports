# Security: Android : http authentication spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40094242](https://issues.chromium.org/issues/40094242) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Auth, UI>Browser>Mobile, UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | ch...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2019-03-08 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: 74,0,3726.0 canary  

Operating System: Android 8.1.0

(similar to <https://crbug.com/chromium/884179> )

**REPRODUCTION CASE**

1. Go to <https://lbstyle.github.io/spoof.html>
2. Click here

## Attachments

- [screenshot.jpeg](attachments/screenshot.jpeg) (image/jpeg, 34.8 KB)

## Timeline

### oc...@chromium.org (2019-03-11)

tedchoc, can you please take a look?

[Monorail components: Internals>Network>Auth UI>Browser>Mobile UI>Browser>Navigation]

### sh...@chromium.org (2019-03-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-11)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2019-03-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/89bf8cdddd76a4110b9419e19600928637ebd7ee

commit 89bf8cdddd76a4110b9419e19600928637ebd7ee
Author: Ted Choc <tedchoc@chromium.org>
Date: Tue Mar 12 22:05:14 2019

Suppress HTTP auth dialogs if the tab is hidden (or gets hidden).

BUG=939689

Change-Id: Iac8e4043448ea6c313c22b5447548b1bb331db3e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1515639
Reviewed-by: Becky Zhou <huayinz@chromium.org>
Commit-Queue: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/heads/master@{#640118}
[modify] https://crrev.com/89bf8cdddd76a4110b9419e19600928637ebd7ee/chrome/android/java/src/org/chromium/chrome/browser/ChromeHttpAuthHandler.java
[modify] https://crrev.com/89bf8cdddd76a4110b9419e19600928637ebd7ee/chrome/android/javatests/src/org/chromium/chrome/browser/ChromeHttpAuthHandlerTest.java
[modify] https://crrev.com/89bf8cdddd76a4110b9419e19600928637ebd7ee/chrome/browser/ui/android/chrome_http_auth_handler.cc
[modify] https://crrev.com/89bf8cdddd76a4110b9419e19600928637ebd7ee/chrome/browser/ui/android/chrome_http_auth_handler.h
[modify] https://crrev.com/89bf8cdddd76a4110b9419e19600928637ebd7ee/chrome/browser/ui/android/login_handler_android.cc


### te...@chromium.org (2019-03-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-03-12)

Please mark this security bug as fixed since the fix has landed, and before requesting merges. Thanks :-)

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-13)

Your change meets the bar and is auto-approved for M74. Please go ahead and merge the CL to branch 3729 (refs/branch-heads/3729) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@appspot.gserviceaccount.com (2019-03-18)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/8a311541ba70fe756890b0c4f47bc25ea6220e3b

Commit: 8a311541ba70fe756890b0c4f47bc25ea6220e3b
Author: tedchoc@chromium.org
Commiter: tedchoc@chromium.org
Date: 2019-03-18 17:42:05 +0000 UTC

Suppress HTTP auth dialogs if the tab is hidden (or gets hidden).

BUG=939689

Change-Id: Iac8e4043448ea6c313c22b5447548b1bb331db3e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1515639
Reviewed-by: Becky Zhou <huayinz@chromium.org>
Commit-Queue: Ted Choc <tedchoc@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#640118}(cherry picked from commit 89bf8cdddd76a4110b9419e19600928637ebd7ee)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1528916
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#237}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}

### na...@google.com (2019-03-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-20)

Congrats the Panel decided to reward $1,000 for this report! 

### aw...@google.com (2019-03-21)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2019-04-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/939689?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>Auth, UI>Browser>Mobile, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094242)*
