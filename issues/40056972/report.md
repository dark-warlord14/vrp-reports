# Security: Manifest.json can display overlay on non-origin tabs

| Field | Value |
|-------|-------|
| **Issue ID** | [40056972](https://issues.chromium.org/issues/40056972) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>WebAppInstalls>Android |
| **Platforms** | Android |
| **Reporter** | te...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2021-08-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

A user opening a new tab may see the new tab's manifest pop-up on the original tab.

I don't think this is a Site Isolation bypass, but it may used in Security UI Spoofing,

**VERSION**  

Chrome Version: 92.0.4515.159 stable  

Operating System: Android 10 (patch 2020-09-01)

**REPRODUCTION CASE**

See attached video. A user on a non-Twitter page (twistory.ml) opens a new tab to mobile.twitter.com. Twitter's web page contains a manifest.json which launches a pop-up prompting an app install. The pop-up should \*only\* be shown on Twitter's site, instead it is shown on the non-Twitter site.

A malicious user could look at the HTTP referer of the original tab, and craft a manifest.json which spoof's the parent page.

For example:

example.com -> open new tab to -> evil.com

evil.com displays an app install banner over example.com which spoofs example.com

Please let me know if you'd like any more details.

**CREDIT INFORMATION**  

Reporter credit: Terence Eden <https://shkspr.mobi/blog/>

## Attachments

- [Chrome Bug.mp4](attachments/Chrome Bug.mp4) (video/mp4, 6.9 MB)
- [Screenshot_20210823-160027.jpg](attachments/Screenshot_20210823-160027.jpg) (image/jpeg, 25.2 KB)

## Timeline

### [Deleted User] (2021-08-23)

[Empty comment from Monorail migration]

### ko...@google.com (2021-08-23)

[Empty comment from Monorail migration]

### ar...@google.com (2021-08-23)

I agree with you. I think Chrome should avoid displaying the banner for installing android package when triggered from a document that isn't in the foreground.

I am assuming it exists a mechanism for ensuring a given origin can only advertise for android apps it owns. That's what would be somehow broken here.

+dominickn@. I believe you own this component, could you please triage this further?

This doesn't look very scary to me. The banner still display the origin of the app to be installed. I will tentatively apply "Security_Severity-Low", don't hesitate to change if you think otherwise.

[Monorail components: UI>Browser>WebAppInstalls>Desktop]

### ar...@google.com (2021-08-23)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>WebAppInstalls>Desktop UI>Browser>WebAppInstalls>Android]

### [Deleted User] (2021-08-23)

[Empty comment from Monorail migration]

### te...@gmail.com (2021-08-23)

> The banner still display the origin of the app to be installed.

In this example, it says `mobile.twitter.com` but there's not much room there. It would be trivial to have an origin of mobile.BankOfAmerica.com.login.evil.com`

(I'm assuming that the origin display doesn't wrap or shrink font size. Do correct me if I'm wrong.)


### [Deleted User] (2021-08-23)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-08-23)

The origin is truncated from the left, so `mobile.BankOfAmerica.com.login.evil.com` is going to show up as "...login.evil.com" when it's too long.

Note that this is not for installing an Android app, it's for installing the web site. I really can't see a meaningful use for such a spoof, since the origin is clearly displayed in the install prompt and is truncated correctly when it's too long. It also feels equivalent to the native app banner feature, which allows any website to link to any app in Play. This is more of a functional bug than anything else.

However, the install prompt should not be shown if the page it's open on is in the background. +fbeaufort +finnur, can you investigate this?

### ad...@chromium.org (2021-08-24)

cc tsteiner per twitter discussion about this bug.

### ts...@google.com (2021-08-24)

[Empty comment from Monorail migration]

### fi...@chromium.org (2021-08-25)

Didn't notice that fbeaufort@ was assigned to this, but I have a fix in review. Hope I'm not stepping on anyone's toes. :)
https://chromium-review.googlesource.com/c/chromium/src/+/3119088/ 

### fi...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c6ff7cf538252086d2d14d8ba7a7a754be26aa67

commit c6ff7cf538252086d2d14d8ba7a7a754be26aa67
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Thu Aug 26 11:33:21 2021

[Android]: Don't show banner from background tabs.

Bug: 1242315
Change-Id: I039ab17c99be7d21fa880d0baf3669b1403e258d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3119088
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Cr-Commit-Position: refs/heads/main@{#915541}

[modify] https://crrev.com/c6ff7cf538252086d2d14d8ba7a7a754be26aa67/chrome/browser/banners/android/BUILD.gn
[modify] https://crrev.com/c6ff7cf538252086d2d14d8ba7a7a754be26aa67/chrome/browser/banners/android/java/src/org/chromium/chrome/browser/banners/AppBannerManagerTest.java
[modify] https://crrev.com/c6ff7cf538252086d2d14d8ba7a7a754be26aa67/chrome/browser/webapps/android/java/src/org/chromium/chrome/browser/webapps/PwaBottomSheetController.java
[modify] https://crrev.com/c6ff7cf538252086d2d14d8ba7a7a754be26aa67/chrome/browser/webapps/android/java/src/org/chromium/chrome/browser/webapps/PwaBottomSheetControllerProvider.java
[modify] https://crrev.com/c6ff7cf538252086d2d14d8ba7a7a754be26aa67/components/webapps/browser/android/app_banner_manager_android.cc
[modify] https://crrev.com/c6ff7cf538252086d2d14d8ba7a7a754be26aa67/components/webapps/browser/android/app_banner_manager_android.h
[modify] https://crrev.com/c6ff7cf538252086d2d14d8ba7a7a754be26aa67/components/webapps/browser/android/java/src/org/chromium/components/webapps/AppBannerManager.java


### fi...@chromium.org (2021-08-27)

[Empty comment from Monorail migration]

### fi...@chromium.org (2021-08-27)

Actually, I just checked and the same thing is possible with the InProductHelp for PWAs. 

Fix in progress...
https://chromium-review.googlesource.com/3124684


### fi...@chromium.org (2021-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b46122bc45580337bf682442a6251b11700aa000

commit b46122bc45580337bf682442a6251b11700aa000
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Mon Aug 30 03:52:59 2021

[Android]: Don't show IPH from background content.

Bug: 1242315
Change-Id: I0ff16ebeb5e08d2afef99acef5f62e564d906239
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3124684
Auto-Submit: Finnur Thorarinsson <finnur@chromium.org>
Commit-Queue: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Cr-Commit-Position: refs/heads/main@{#916306}

[modify] https://crrev.com/b46122bc45580337bf682442a6251b11700aa000/chrome/browser/banners/android/java/src/org/chromium/chrome/browser/banners/AppBannerInProductHelpControllerProvider.java
[modify] https://crrev.com/b46122bc45580337bf682442a6251b11700aa000/chrome/browser/banners/android/java/src/org/chromium/chrome/browser/banners/AppBannerManagerTest.java


### te...@gmail.com (2021-09-17)

Hello. As this is marked fix, are you happy for me to write up a short blog post about it? If so, please let me know the acceptable timings. Thanks!

### am...@chromium.org (2021-09-28)

Hi, thanks for your question. Apologies for the delay in response as Fixed low-severity bugs are not highly monitored after they are fixed.
The fix for this issue has not yet shipped in a release, and in general, we would ask you would refrain from any sort of public disclosure or a blog post until this bug is made public by us. That occurs 14 weeks after the issue is updated as Fixed and the bug will automatically be updated with the 'allpublic' label at that time. This allows for sufficient time for users to have upgraded once the patch is included in a Stable channel release. Thank you!



### te...@gmail.com (2021-09-28)

Thanks Amy, I'll publish on 5th December (14 weeks after 27 August).
I assume the reward panel will have made a decision by then as well.

### am...@google.com (2021-09-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-28)

Hi Terence! Reward panel decision was today, I noticed your question while prepping for the bugs we were to discuss this week...and congratulations - the VRP Panel has decided to award you $1000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for reporting this issue to us! 

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1242315?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056972)*
