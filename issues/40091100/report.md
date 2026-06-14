# Security: URL spoofing on iOS  (repro issue 796777)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091100](https://issues.chromium.org/issues/40091100) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2018-04-13 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 66.3359.98 beta  

Operating System: iOS

This is from <https://crbug.com/chromium/796777>.

**REPRODUCTION CASE**

1. Load outlook.com
2. Load facebook.com
3. Click on any comment on facebook.com
4. Click the time on the top of the iOS screen UI

## Attachments

- [screen_shot.jpeg](attachments/screen_shot.jpeg) (image/jpeg, 124.9 KB)
- [64BFB742-F73C-4852-8E6E-FBA4BBBEE5F0.png](attachments/64BFB742-F73C-4852-8E6E-FBA4BBBEE5F0.png) (image/png, 157.4 KB)

## Timeline

### el...@chromium.org (2018-04-13)

Please include the exact version number of iOS where you were able to reproduce this. Thanks!

### ch...@gmail.com (2018-04-13)

Ah Sorry! 11.2.2 iOS.

### ca...@chromium.org (2018-04-13)

eugenebut: Assigning to you since you had the previous issue.

Assigning medium severity since this requires a specific user action.

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### eu...@chromium.org (2018-04-13)

Could not repro with 66.0.3359.98 on iPhone SE iOS 11.3 and iPhone 6 Plus iOS 11.2.6. Srikanth, could you please try reproducing.

### sh...@chromium.org (2018-04-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@chromium.org (2018-04-16)

I am not able to reproduce either. Tried on iOS 11.1.2, 11.2.6 and 11.4
NTP is displayed after tapping on the system status bar.

### ch...@gmail.com (2018-04-16)

Sometimes looks like it can take several tries to repro. Srikanthg@, Can you please try with using gmail.com instead of outlook.com?

### sr...@chromium.org (2018-04-16)

Yeah, I can repro with gmail.com and facebook.com comnibation.
eugenebut@ lemme know if you need help reproducing.

Here is what I have tried.

Launch Chrome

(Sign into gmail.com and facebook.com in two diff tabs)
1. Now Open a new tab and open gmail.com
2. Open a email, and side swipe to read few more emails
3. In the same tab navigate to facebook.com
4. Open comments section from any post
5. Tap on the status bar.

Observe that Gmail.com is loaded but omnibox still shows facebook.com
Link to video: https://drive.google.com/file/d/1laMYTaJjCjJteQb2hB5zyRwmsDPN1inM/view



### sr...@chromium.org (2018-04-17)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0796ec8ba7af1e8937b071528ff2aa7156860755

commit 0796ec8ba7af1e8937b071528ff2aa7156860755
Author: Eugene But <eugenebut@google.com>
Date: Mon Apr 23 22:19:08 2018

Fix LegacyNavigationManagerImpl::FinishGoToIndex.

This change fixes computing "same_document_navigation" boolean by using
"last committed item" instead of "current item" as a source navigation
item. "current item" can pe pending or transient and it's never correct
to assume that same document navigation happens from pending or
transient item.

Bug: 832734
Cq-Include-Trybots: master.tryserver.chromium.mac:ios-simulator-cronet;master.tryserver.chromium.mac:ios-simulator-full-configs
Change-Id: Ia2c26f29a898f69be3352e04f46fdb4498413a7f
Reviewed-on: https://chromium-review.googlesource.com/1021659
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/heads/master@{#552857}
[modify] https://crrev.com/0796ec8ba7af1e8937b071528ff2aa7156860755/ios/web/navigation/legacy_navigation_manager_impl.mm
[modify] https://crrev.com/0796ec8ba7af1e8937b071528ff2aa7156860755/ios/web/navigation/navigation_manager_impl_unittest.mm


### eu...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-24)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-25)

Your change meets the bar and is auto-approved for M67. Please go ahead and merge the CL to branch 3396 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/244da9e8b795d6946c0ccbdcb9b232739071561a

commit 244da9e8b795d6946c0ccbdcb9b232739071561a
Author: Eugene But <eugenebut@chromium.org>
Date: Wed Apr 25 02:20:08 2018

Fix LegacyNavigationManagerImpl::FinishGoToIndex.

This change fixes computing "same_document_navigation" boolean by using
"last committed item" instead of "current item" as a source navigation
item. "current item" can pe pending or transient and it's never correct
to assume that same document navigation happens from pending or
transient item.

TBR=eugenebut@google.com

(cherry picked from commit 0796ec8ba7af1e8937b071528ff2aa7156860755)

Bug: 832734
Cq-Include-Trybots: master.tryserver.chromium.mac:ios-simulator-cronet;master.tryserver.chromium.mac:ios-simulator-full-configs
Change-Id: Ia2c26f29a898f69be3352e04f46fdb4498413a7f
Reviewed-on: https://chromium-review.googlesource.com/1021659
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#552857}
Reviewed-on: https://chromium-review.googlesource.com/1027089
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#280}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/244da9e8b795d6946c0ccbdcb9b232739071561a/ios/web/navigation/legacy_navigation_manager_impl.mm
[modify] https://crrev.com/244da9e8b795d6946c0ccbdcb9b232739071561a/ios/web/navigation/navigation_manager_impl_unittest.mm


### sh...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

$500 for this one :-)

### aw...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-08-01)

This issue was migrated from crbug.com/chromium/832734?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091100)*
