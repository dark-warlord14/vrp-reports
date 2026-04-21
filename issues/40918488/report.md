# Security: [Fix bypass] PWA Install prompt can still be overlaid over other origins

| Field | Value |
|-------|-------|
| **Issue ID** | [40918488](https://issues.chromium.org/issues/40918488) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Platform>WebAppProvider |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2023-06-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

In <https://chromium-review.googlesource.com/c/chromium/src/+/4616004> it was fixed such that PWA install prompt closes after navigation. While testing in Canary with the fix absorbed, if popup blocker is disabled, I found that a page can still call the install prompt and open a new window at the same time which causes the PWA install prompt to overlay other origin.  

This is because the fix only fixes main frame navigations

**VERSION**  

Chrome Version: 117.0.5850.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 10 Version 22H2 (Build 19045.3086)

**REPRODUCTION CASE**  

0. Use Canary to absorb the fix for <https://chromium-review.googlesource.com/c/chromium/src/+/4616004>

1. Disable popup blocker
2. Go to <https://rigorous-ajar-marionberry.glitch.me/a2hs-poc.html>
3. Click when the tick is green. The install prompt overlay other origins.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [dummy-sw.js](attachments/dummy-sw.js) (text/plain, 156 B)
- [app.webmanifest](attachments/app.webmanifest) (application/octet-stream, 1.2 KB)
- [app.js](attachments/app.js) (text/plain, 1.8 KB)
- [a2hs-poc.html](attachments/a2hs-poc.html) (text/plain, 939 B)
- [Untitled_ Jun 24, 2023 2_47 PM.webm](attachments/Untitled_ Jun 24, 2023 2_47 PM.webm) (video/webm, 1.2 MB)

## Timeline

### ha...@gmail.com (2023-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-24)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-06-24)

[Empty comment from Monorail migration]

### ah...@google.com (2023-06-26)

Thanks for the report!
I was able to reproduce using canary 117.0.5854.0 (Official Build) on windows (with pop-ups allowed)
It indeed looks similar to https://crbug.com/chromium/1450203. => setting severity to medium similarly.
Security_Impact-None since it only happens on a non-default configuration.

dibyapal@chromium.org could you PTAL?




[Monorail components: UI>Browser>WebAppInstalls]

### di...@chromium.org (2023-06-26)

Was able to reproduce as well. Since this is Medium Severity, marking it available and assigned to correct component so that it shows up during triaging.

[Monorail components: -UI>Browser>WebAppInstalls Platform>WebAppProvider]

### dm...@chromium.org (2023-06-26)

Interesting- I thought that we anchored the dialog on the web contents but maybe we did on the browser itself?

We should be observing the web contents no longer being visible - but perhaps we aren't doing that correctly?

I wonder if this is something that we can do by splitting out the installation UX tracking into a separate thing, and then the AppBannerManager can invalidate installation UX on visibility change? Or whatever other manager would be managing that?

### ad...@google.com (2023-07-17)

dibyapal@ dmurph@ we don't like to leave security bugs unassigned - please pick which of you it goes to.

Also, our security shepherd in https://crbug.com/chromium/1457704#c4 marked this as Security_Impact-None because this applied in non-default configurations. However I believe the setting in question is disabling the popup blocker which can be done in the UI, so as per https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#TOC-Security-Impact-None, we do regard this as impacting mainstream Chrome users and I'm removing that label.

It looks like https://chromium-review.googlesource.com/c/chromium/src/+/4616004 probably landed in M116 based on commit position, so labelling thus.

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

dibyapal: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2023-07-18)

I don't think this should block stable release of m116

### dm...@chromium.org (2023-07-18)

I'll pick this up.

### dm...@chromium.org (2023-07-18)

[Empty comment from Monorail migration]

### be...@google.com (2023-07-18)

Adding Hotlist-RBS-Removed for tracking purposes.

### ha...@gmail.com (2023-07-19)

dmurph@, dibyapal@ maybe you'd want to take a closer look at the  LocationBarBubbleDelegateView::OnVisibilityChanged method in https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/location_bar/location_bar_bubble_delegate_view.cc;l=145 to see whether that can fix the problem

### ha...@gmail.com (2023-07-19)

Actually looking at the code, OnVisibilityChanged should be triggered as the original installer is hidden, maybe it is possible that the web_contents is being incorrectly observed as https://microsoft.com instead of the original installer (due to it being too fast?)

### ha...@gmail.com (2023-07-19)

Maybe it is also because somewhere along the code web_contents is not being passed?

For example, in https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/web_applications/web_app_dialog_utils.cc;l=189, web_contents is not being passed to OnWebAppInstallShowInstallDialog method (https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/web_applications/web_app_dialog_utils.cc;l=51;bpv=1;bpt=1)??

Then again, I am not an expert in the code.

### [Deleted User] (2023-07-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2023-07-19)

I guess the FoundIn should be set before the Target in order for the bot to stop nagging.

### dm...@google.com (2023-07-19)

I'm setting this to low severity, as it is limited scope requiring the user to disable the popup blocking for this origin. I'm working on a fix now, but I don't think this needs to be m116 stable release blocker.

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### dm...@chromium.org (2023-07-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a

commit 942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a
Author: Daniel Murphy <dmurph@chromium.org>
Date: Wed Jul 26 17:52:36 2023

[dPWA] Observe web contents visibility when installing

This change:
- Starts observation of the web contents immediately for install,
  instead of on command start.
- Cancels the installation if the visibility changes.
- Cancels the installation if the web contents is navigated.

Bug: 1457704
Change-Id: Ic52a48901c20b36a5fcebeef235f8c84f3566410
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4702391
Auto-Submit: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1175542}

[modify] https://crrev.com/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a/components/segmentation_platform/public/testing/mock_segmentation_platform_service.h
[modify] https://crrev.com/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a/chrome/browser/installable/ml_promotion_browsertest.cc
[modify] https://crrev.com/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a/chrome/browser/web_applications/commands/fetch_manifest_and_install_command.h
[modify] https://crrev.com/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a/chrome/browser/web_applications/commands/fetch_manifest_and_install_command.cc
[modify] https://crrev.com/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a/components/segmentation_platform/public/segmentation_platform_service.cc
[modify] https://crrev.com/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a/chrome/browser/web_applications/commands/fetch_manifest_and_install_command_unittest.cc
[modify] https://crrev.com/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a/components/segmentation_platform/public/segmentation_platform_service.h
[modify] https://crrev.com/942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a/chrome/browser/web_applications/commands/fetch_manifest_and_install_command_browsertest.cc


### gi...@appspot.gserviceaccount.com (2023-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/543f3238c481fa50226b3c64d29740f52ae08ba1

commit 543f3238c481fa50226b3c64d29740f52ae08ba1
Author: Viktor Semeniuk <vsemeniuk@google.com>
Date: Thu Jul 27 08:09:56 2023

Revert "[dPWA] Observe web contents visibility when installing"

This reverts commit 942e821ba94f5fb2dbc05cc6f68066b75ad3ff6a.

Reason for revert: causes tests timeout on multiple builds linux-lacros-asan-lsan-rel [1] and linux-lacros-tester-rel [2]

[1]https://ci.chromium.org/ui/p/chromium/builders/ci/linux-lacros-asan-lsan-rel/5853/overview
[2]https://ci.chromium.org/ui/p/chromium/builders/ci/linux-lacros-tester-rel/50550/overview

Original change's description:
> [dPWA] Observe web contents visibility when installing
>
> This change:
> - Starts observation of the web contents immediately for install,
>   instead of on command start.
> - Cancels the installation if the visibility changes.
> - Cancels the installation if the web contents is navigated.
>
> Bug: 1457704
> Change-Id: Ic52a48901c20b36a5fcebeef235f8c84f3566410
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4702391
> Auto-Submit: Daniel Murphy <dmurph@chromium.org>
> Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org>
> Reviewed-by: Min Qin <qinmin@chromium.org>
> Commit-Queue: Min Qin <qinmin@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1175542}

Bug: 1457704, 1468187
Change-Id: Id83572acaca8be298009f081a856a5fb8e392134
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4720556
Owners-Override: Viktor Semeniuk <vsemeniuk@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Viktor Semeniuk <vsemeniuk@google.com>
Cr-Commit-Position: refs/heads/main@{#1175918}

[modify] https://crrev.com/543f3238c481fa50226b3c64d29740f52ae08ba1/components/segmentation_platform/public/testing/mock_segmentation_platform_service.h
[modify] https://crrev.com/543f3238c481fa50226b3c64d29740f52ae08ba1/chrome/browser/installable/ml_promotion_browsertest.cc
[modify] https://crrev.com/543f3238c481fa50226b3c64d29740f52ae08ba1/chrome/browser/web_applications/commands/fetch_manifest_and_install_command.cc
[modify] https://crrev.com/543f3238c481fa50226b3c64d29740f52ae08ba1/chrome/browser/web_applications/commands/fetch_manifest_and_install_command.h
[modify] https://crrev.com/543f3238c481fa50226b3c64d29740f52ae08ba1/components/segmentation_platform/public/segmentation_platform_service.cc
[modify] https://crrev.com/543f3238c481fa50226b3c64d29740f52ae08ba1/chrome/browser/web_applications/commands/fetch_manifest_and_install_command_unittest.cc
[modify] https://crrev.com/543f3238c481fa50226b3c64d29740f52ae08ba1/components/segmentation_platform/public/segmentation_platform_service.h
[modify] https://crrev.com/543f3238c481fa50226b3c64d29740f52ae08ba1/chrome/browser/web_applications/commands/fetch_manifest_and_install_command_browsertest.cc


### [Deleted User] (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-09-19)

Hello, any updates here?

### dm...@chromium.org (2023-09-20)

Nope. Still on our backlog. The challenge here is that it's hard to just 'close' all isntalled if we lose focus, as that makes a bunch of our browsertests fail (as they are run in parallel).

So instead we should probably do something where we detect the web contents navigating somewhere else... or... I forget. I wish I wrote down my new strategy back when I tried to fix that patch above.

I would expect us to get to this sometime early Q4.

### ha...@gmail.com (2023-09-24)

Thanks for the update dmurph@! I think a simpler approach to that flaky test problem would be, in the OnVisibilityChanged event handler in your previous patch, to pass in a browser() object and perform an additional check if browser->tab_strip_model()->GetActiveWebContents() is equal to the current web contents, aborting the install dialog only if they are not the same.

That way the web install dialog will close only if the current active web contents is different from the installer's web contents which represents a navigation / popup opening

WDYT?

### gi...@appspot.gserviceaccount.com (2023-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/983989b3e894c0082b8da024d1dae5bed5ca19d6

commit 983989b3e894c0082b8da024d1dae5bed5ca19d6
Author: Haxatron Sec <haxatron1@gmail.com>
Date: Fri Sep 29 21:42:56 2023

[dPWA] Observe web contents visibility when installing

This change:
- Starts observation of the web contents immediately for install,
  instead of on command start.
- Cancels the installation if the visibility changes and the currently
  active web contents do not match the installer web contents
- Cancels the installation if the web contents is navigated.

Bug: 1457704

Change-Id: If563d04c990c657b5468c3f388a17a49881e2e02
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4899736
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1203462}

[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/web_applications/commands/fetch_manifest_and_install_command.cc
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/web_applications/commands/fetch_manifest_and_install_command.h
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/ui/web_applications/web_app_ui_manager_impl.cc
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/web_applications/test/fake_web_app_ui_manager.cc
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/ui/web_applications/web_app_ui_manager_impl.h
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/web_applications/web_app_command_scheduler.cc
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/web_applications/commands/fetch_manifest_and_install_command_unittest.cc
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/web_applications/commands/fetch_manifest_and_install_command_browsertest.cc
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/web_applications/web_app_ui_manager.h
[modify] https://crrev.com/983989b3e894c0082b8da024d1dae5bed5ca19d6/chrome/browser/web_applications/test/fake_web_app_ui_manager.h


### ha...@gmail.com (2023-10-05)

dmurph@, dibyapal@, given ~5 days have passed since https://crbug.com/chromium/1457704#c31 without any reverts and I have verified the fix on Canary. I think it is safe to mark this as fixed. Thanks!

### ha...@gmail.com (2023-10-06)

friendly ping on the above.

### di...@chromium.org (2023-10-06)

Thank you Axel for the fix! Sounds like it worked, and apologies for the delay.

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations Axel! The Chrome VRP Panel has decided to award you $2,000 for this report. The reward amount was decided upon based on the limited security impact from this issue given that the correct origin is displayed on the PWA install prompt. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-18)

Hi Axel, we have updated your VRP reward to reflect a $1,000 patch bonus. While the patch wasn't wholly yours, we do appreciate you making an update to resolve the flaky test issue and getting this fix landed sooner than later. Thank you for your efforts! 

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

Adding reward-unpaid since the patch bonus payment does not appear to have been processed. 

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-12)

This issue was migrated from crbug.com/chromium/1457704?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40918488)*
