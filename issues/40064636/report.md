# Security: (Android) PWA Install Dialogs can be overlaid over other origins (PWA install dialog spoofing while navigation).

| Field | Value |
|-------|-------|
| **Issue ID** | [40064636](https://issues.chromium.org/issues/40064636) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile>CompositedUI, UI>Browser>Mobile>CustomTabs, UI>Browser>Mobile>Messages, UI>Browser>WebAppInstalls>Android |
| **Platforms** | Android |
| **Reporter** | el...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2023-05-18 |
| **Bounty** | $1,000.00 |

## Description

## **VULNERABILITY DETAILS** :

This Bug is filled Because the main one " <https://crbug.com/chromium/1442434>" was mistakenly closed as Won't-fix,and i have corrected the related components the this bug is related to, so please update the bug component as mentioned below , also i see that [bauerb@chromium.org](mailto:bauerb@chromium.org) fixed some bugs in custom tabs like in this issue <https://bugs.chromium.org/p/chromium/issues/detail?id=798933>

This bug is straight forward Regression for (<https://crbug.com/chromium/1404230>) in (Android System Webview) But in "CCT" which allows PWA Install prompt to be overlaid over other origins (Cross Origin), that allows user to be tricked to install unknown Apps instead of Legit Ones.

A PWA is essentially a website that can be installed and run like a native app on a user's device. This means that if a user is tricked into downloading a malicious PWA, the malicious code can potentially access sensitive data on the user's device, such as personal information, passwords,Autofill data, and other sensitive data.

Additionally a user may be tricked into installing a PWA that looks like a legitimate app, such as Microsoft Teams or another popular app.The user may then be prompted to enter sensitive information, such as their login credentials, which can then be intercepted by the attacker.

User Can't Defer the original(Legitmate) App and installed PWA(Malicious) one in Android Device,putting privacy and information of user in risk.

On Android, there are two types of installation prompts for PWAs

(1) Installation prompt with description and screenshot fields. This causes a popup from the bottom. This can be seen in <https://coordinated-tartan-individual.glitch.me/a2hs-poc.html>

(2) Installation prompt without description and screenshot fields. This causes a box to be drawn in the middle. This can be seen in <https://shade-cactus-dragon.glitch.me/a2hs-poc.html>

The installation prompt for (1) will disappear on Android when it navigates to other origins - ref: <https://jewel-chip-panama.glitch.me/a2hs-poc.html>. On the other hand, the installation prompt for (2) will NOT disappear when Android navigates to other origins.

## Components:

UI>Browser>Mobile>CustomTabs  

UI>Browser>WebAppInstalls  

UI>Browser>Mobile>CompositedUI

## **VERSION**

Android CCT based on Chrome Version: [112.0.5615.136]  

Operating System: [Android 13]

## The main Bug in Android Browser was Found-In:108

This is the Fix of the Bug In Android Browser in M-111 [111.0.5563.64]

<https://chromium-review.googlesource.com/c/chromium/src/+/4153171>

the fix introduces "The install/A2HS dialog should dismiss with tab navigation or destroy" to prevent Spoofing WPA installs while navigating other origins.

## **REPRODUCTION CASE**

++Before Repro Send the following link as email Msg in Gmail() or in Twitter for Example to be opened in Android CCT++

1. On Android Open Gmail/Twitter MSg, go to <https://vrphunt.com/chrome/spooforigin/pwa-crossorigin.html>
2. Press when tick appears. The prompt appears and Android CCT will navigate to <https://microsoft.com> at the same time of PWA dialog shown.

++All Offline Poc files attached below ,You Can also Download and host the offline files on your server and test.++

## Expected:

The install/A2HS dialog should dismiss with tab navigation or destroy" to prevent Spoofing WPA installs while navigating other origins.

## Observed:

Dialog is shown over Other Origins while navigation takes place ,which could allow easy spoofing tricking user to install PWA that looks like a legitimate app.

## Fix/Mitigation:

Fix is Same as in this Commit:  

<https://chromium-review.googlesource.com/c/chromium/src/+/4153171>

---

**CREDIT INFORMATION**

Reporter credit: Ahmed ElMasry

## Attachments

- [Android CCT-crossorigin-PWA-regression.mp4](attachments/Android CCT-crossorigin-PWA-regression.mp4) (video/mp4, 4.8 MB)
- [pwa-crossorigin.html](attachments/pwa-crossorigin.html) (text/plain, 1.1 KB)
- [pwa-app-crossorigin.js](attachments/pwa-app-crossorigin.js) (text/plain, 2.0 KB)
- [style.css](attachments/style.css) (text/plain, 868 B)
- [dummy-sw.js](attachments/dummy-sw.js) (text/plain, 156 B)
- [pwa-app.webmanifest](attachments/pwa-app.webmanifest) (application/octet-stream, 622 B)
- [phishing.html](attachments/phishing.html) (text/plain, 731 B)
- [Screenshot_20230508-220706.png](attachments/Screenshot_20230508-220706.png) (image/png, 97.8 KB)

## Timeline

### [Deleted User] (2023-05-18)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-19)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Mobile>CompositedUI UI>Browser>Mobile>CustomTabs UI>Browser>WebAppInstalls]

### [Deleted User] (2023-05-19)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-19)

@eirage@chromium.org Hi eirage@, it looks like the reporter sent the bug back with additional details. The older bug was closed by you and if you would be able to help resolve this one as well. Thanks!

### an...@chromium.org (2023-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-02)

eirage: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-06-08)

Hello Sheriff: friendly reminder..,
Any further updates/progress on this one?!
eirage@ is this under your radar?
Thanks 

### am...@chromium.org (2023-06-13)

cc'ing as per request in https://bugs.chromium.org/p/chromium/issues/detail?id=1450203#c20

### di...@chromium.org (2023-06-13)

Unfortunately the fixes in crbug.com/1450203 are only for desktop specific OS. This should be looked at by someone from Android. I assigned the correct component, it will be triaged and prioritized by the Android team.

[Monorail components: -UI>Browser>WebAppInstalls UI>Browser>WebAppInstalls>Android]

### [Deleted User] (2023-06-16)

eirage: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-06-19)

Hello there..,

Any further updates on this?! , Could you triage this further?!, This is a friendly reminder to be sure that this issue under your radar as it's been 1 month without activity.

Thanks for your time in advance!

### el...@gmail.com (2023-07-10)

Hello there.., @eirage@chromium.org

Just wanted to check that this issue under your radar, if this issue slipped from queue please pump it up, also please merge this https://crbug.com/chromium/1442434 here , as it was closed and may go to public next month before this one here fixed .

Thanks.

### am...@chromium.org (2023-07-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-17)

Merged 1442434 (and earlier version of this report) into this issue since it was closed as WontFix back in May. This report is from the same reporter of that earlier report, so this version can be treated as the canonical one. 

eirage@ -- this looks almost identical to https://crbug.com/chromium/1404230, which was resolved by you back in January. 
Can you PTAL when you have a moment. If this is unable to be prioritized at this time, can you kindly update with a next-action date with a ballpark date on which work can take place on this issue. Thank you! 

### ei...@chromium.org (2023-07-18)

I am still unable to reproduce this. I think this is the same root cause as https://crbug.com/chromium/1404230. 
I'll try again later this week.

### dm...@chromium.org (2023-07-18)

Ella - I wonder if this can be solved by making a more formal 'installation UX registration' class that pulls that part out of the MlPromotionManager, and allows us to more easily 'close' that UX if the AppBannerManager detects a change.

### ei...@chromium.org (2023-07-19)

That is possible, but will require a complete change on the android dialog class lifecycle. 

I might have found the potential root cause of why this is fixed for browser tabs but not CCT, working on verifying

### ei...@chromium.org (2023-07-19)

I fixed https://crbug.com/chromium/1404230 with changing the instal modal dialog type from "APP" to "TAB" so it would be closed when tab changes.
The fixed dose not apply to CCT because TabModalLifetimeHandler was initialized for `ChromeTabbedActivity` but not for `BaseCustomTabActivity`

so presumable any dialog that opens in CCT might have the same issue. 

the fix might by duplicating ChromeTabbedActivity#createModalDialogManager for CCT. I'm not entirely sure whether it should be.

twellington@ your team seems to own modaldialog, maybe someone from your side can take a look?
Thanks

### tw...@chromium.org (2023-07-19)

-> Lijin to take a look

### tw...@chromium.org (2023-07-21)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Mobile>Messages]

### gi...@appspot.gserviceaccount.com (2023-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8c03adfed840cc86026ff4e88e9e53f93abdb40a

commit 8c03adfed840cc86026ff4e88e9e53f93abdb40a
Author: Lijin Shen <lazzzis@google.com>
Date: Thu Jul 27 00:48:40 2023

Introduce Tab Modal dialog to CCT.

Before this CL, only App Modal dialog is supported on CCT. This CL
adds Tab Modal dialog to CCT and tests whether they can be
correctly dismissed by navigation and back press.

Bug: 1446709
Change-Id: Id113b2c0bcae7284deb55f970ff2b30fc96177ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4706547
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Lijin Shen <lazzzis@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1175793}

[modify] https://crrev.com/8c03adfed840cc86026ff4e88e9e53f93abdb40a/chrome/android/java/src/org/chromium/chrome/browser/ui/RootUiCoordinator.java
[modify] https://crrev.com/8c03adfed840cc86026ff4e88e9e53f93abdb40a/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/8c03adfed840cc86026ff4e88e9e53f93abdb40a/chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java
[modify] https://crrev.com/8c03adfed840cc86026ff4e88e9e53f93abdb40a/chrome/android/java/src/org/chromium/chrome/browser/tabbed_mode/TabbedRootUiCoordinator.java
[modify] https://crrev.com/8c03adfed840cc86026ff4e88e9e53f93abdb40a/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java
[modify] https://crrev.com/8c03adfed840cc86026ff4e88e9e53f93abdb40a/chrome/android/java/src/org/chromium/chrome/browser/customtabs/BaseCustomTabActivity.java


### la...@chromium.org (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations, Ahmed! The VRP Panel has decided to award you $1,000 for this report. The reward amount was decided upon based on the limited impact of this spoof, given that the correct origin is displayed on the PWA installation prompt. Thank you for your efforts and reporting this issue to us!

### el...@gmail.com (2023-08-02)

Hi Amy amyressler@
Could you please check the similar one at https://crbug.com/chromium/1404230  , they are the same impact,same scenario,and same poc behavior and results, could you PTAL and review decided reward amount for this one?!
Thanks 

### am...@chromium.org (2023-08-02)

Hello Ahmed, in assessment of this report during VRP Panel toady, we did review the similar prior report and reward. We came to the determination that we made a mistake a slightly over-rewarded that/this issue given the relatively low security impact with the correct origin being presented in the install prompt. Unfortunately, this happens sometimes and we try to ensure all future reward decisions are more consistent with the actual security impact being presented in reference to our reward amount matrix. 

### el...@gmail.com (2023-08-02)

Hi Amy, amyressler@
Thanks for cleaning this, is this https://crbug.com/chromium/1449874 will be on today's  vrp panel table too , it was assigned reward top-panel before this one 
Thanks

### el...@gmail.com (2023-08-02)

**Clearing* typo error  

### am...@chromium.org (2023-08-02)

Reward decisions are made in the order of bug severity, not the date the reward-topanel label was added to this issue, so that one will be evaluated at a forthcoming panel session. 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4ad51737e574d4d31b2f8f6a8fd18a5e485d0abe

commit 4ad51737e574d4d31b2f8f6a8fd18a5e485d0abe
Author: Theresa Sullivan <twellington@chromium.org>
Date: Thu Sep 28 19:08:36 2023

Revert "Introduce Tab Modal dialog to CCT."

This reverts commit 8c03adfed840cc86026ff4e88e9e53f93abdb40a.

Reason for revert: crbug.com/1486017

Original change's description:
> Introduce Tab Modal dialog to CCT.
>
> Before this CL, only App Modal dialog is supported on CCT. This CL
> adds Tab Modal dialog to CCT and tests whether they can be
> correctly dismissed by navigation and back press.
>
> Bug: 1446709
> Change-Id: Id113b2c0bcae7284deb55f970ff2b30fc96177ee
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4706547
> Reviewed-by: Theresa Sullivan <twellington@chromium.org>
> Commit-Queue: Lijin Shen <lazzzis@google.com>
> Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
> Cr-Commit-Position: refs/heads/main@{#1175793}

Bug: 1446709, 1486017
Change-Id: I6bb31f485c26500b84ea731c307f24fc3720dcc2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4902771
Reviewed-by: Harry Souders <harrysouders@google.com>
Commit-Queue: Harry Souders <harrysouders@google.com>
Cr-Commit-Position: refs/branch-heads/6036@{#4}
Cr-Branched-From: a4d3150237b37bfc8a345a6fdbbae4c6822ddce6-refs/heads/main@{#1202576}

[modify] https://crrev.com/4ad51737e574d4d31b2f8f6a8fd18a5e485d0abe/chrome/android/java/src/org/chromium/chrome/browser/ui/RootUiCoordinator.java
[modify] https://crrev.com/4ad51737e574d4d31b2f8f6a8fd18a5e485d0abe/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/4ad51737e574d4d31b2f8f6a8fd18a5e485d0abe/chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java
[modify] https://crrev.com/4ad51737e574d4d31b2f8f6a8fd18a5e485d0abe/chrome/android/java/src/org/chromium/chrome/browser/customtabs/BaseCustomTabActivity.java
[modify] https://crrev.com/4ad51737e574d4d31b2f8f6a8fd18a5e485d0abe/chrome/android/java/src/org/chromium/chrome/browser/tabbed_mode/TabbedRootUiCoordinator.java
[modify] https://crrev.com/4ad51737e574d4d31b2f8f6a8fd18a5e485d0abe/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java


### gi...@appspot.gserviceaccount.com (2023-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0c012e704b7b990e6e416a8a1493c3b65035cb8b

commit 0c012e704b7b990e6e416a8a1493c3b65035cb8b
Author: Theresa Sullivan <twellington@chromium.org>
Date: Thu Sep 28 22:10:47 2023

Revert "Introduce Tab Modal dialog to CCT."

This reverts commit 8c03adfed840cc86026ff4e88e9e53f93abdb40a.

Reason for revert: crbug.com/1486017

Original change's description:
> Introduce Tab Modal dialog to CCT.
>
> Before this CL, only App Modal dialog is supported on CCT. This CL
> adds Tab Modal dialog to CCT and tests whether they can be
> correctly dismissed by navigation and back press.
>
> Bug: 1446709
> Change-Id: Id113b2c0bcae7284deb55f970ff2b30fc96177ee
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4706547
> Reviewed-by: Theresa Sullivan <twellington@chromium.org>
> Commit-Queue: Lijin Shen <lazzzis@google.com>
> Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
> Cr-Commit-Position: refs/heads/main@{#1175793}

Bug: 1446709, 1486017
Change-Id: I6bb31f485c26500b84ea731c307f24fc3720dcc2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4902342
Reviewed-by: Lijin Shen <lazzzis@google.com>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Theresa Sullivan <twellington@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1202876}

[modify] https://crrev.com/0c012e704b7b990e6e416a8a1493c3b65035cb8b/chrome/android/java/src/org/chromium/chrome/browser/ui/RootUiCoordinator.java
[modify] https://crrev.com/0c012e704b7b990e6e416a8a1493c3b65035cb8b/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/0c012e704b7b990e6e416a8a1493c3b65035cb8b/chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java
[modify] https://crrev.com/0c012e704b7b990e6e416a8a1493c3b65035cb8b/chrome/android/java/src/org/chromium/chrome/browser/customtabs/BaseCustomTabActivity.java
[modify] https://crrev.com/0c012e704b7b990e6e416a8a1493c3b65035cb8b/chrome/android/java/src/org/chromium/chrome/browser/tabbed_mode/TabbedRootUiCoordinator.java
[modify] https://crrev.com/0c012e704b7b990e6e416a8a1493c3b65035cb8b/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java


### gi...@appspot.gserviceaccount.com (2023-10-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e3344ddefa12e60436fa28c81cf207c1afb4d0a9

commit e3344ddefa12e60436fa28c81cf207c1afb4d0a9
Author: Lijin Shen <lazzzis@google.com>
Date: Mon Oct 02 15:38:46 2023

[M117] Revert "Introduce Tab Modal dialog to CCT."

This reverts commit 8c03adfed840cc86026ff4e88e9e53f93abdb40a.

Reason for revert: crbug.com/1486017

Original change's description:
> Introduce Tab Modal dialog to CCT.
>
> Before this CL, only App Modal dialog is supported on CCT. This CL
> adds Tab Modal dialog to CCT and tests whether they can be
> correctly dismissed by navigation and back press.
>
> Bug: 1446709
> Change-Id: Id113b2c0bcae7284deb55f970ff2b30fc96177ee
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4706547
> Reviewed-by: Theresa Sullivan <twellington@chromium.org>
> Commit-Queue: Lijin Shen <lazzzis@google.com>
> Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
> Cr-Commit-Position: refs/heads/main@{#1175793}

Bug: 1446709, 1486017
Change-Id: I6bb31f485c26500b84ea731c307f24fc3720dcc2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4903623
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/5938@{#1539}
Cr-Branched-From: 2b50cb4bcc2318034581a816714d9535dc38966d-refs/heads/main@{#1181205}

[modify] https://crrev.com/e3344ddefa12e60436fa28c81cf207c1afb4d0a9/chrome/android/java/src/org/chromium/chrome/browser/ui/RootUiCoordinator.java
[modify] https://crrev.com/e3344ddefa12e60436fa28c81cf207c1afb4d0a9/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/e3344ddefa12e60436fa28c81cf207c1afb4d0a9/chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java
[modify] https://crrev.com/e3344ddefa12e60436fa28c81cf207c1afb4d0a9/chrome/android/java/src/org/chromium/chrome/browser/customtabs/BaseCustomTabActivity.java
[modify] https://crrev.com/e3344ddefa12e60436fa28c81cf207c1afb4d0a9/chrome/android/java/src/org/chromium/chrome/browser/tabbed_mode/TabbedRootUiCoordinator.java
[modify] https://crrev.com/e3344ddefa12e60436fa28c81cf207c1afb4d0a9/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java


### gi...@appspot.gserviceaccount.com (2023-10-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4b4e0691149db980f2f6bad46e26ffeef9088f87

commit 4b4e0691149db980f2f6bad46e26ffeef9088f87
Author: Theresa Sullivan <twellington@chromium.org>
Date: Mon Oct 02 16:40:59 2023

[M118] Revert "Introduce Tab Modal dialog to CCT."

This reverts commit 8c03adfed840cc86026ff4e88e9e53f93abdb40a.

Reason for revert: crbug.com/1486017

Original change's description:
> Introduce Tab Modal dialog to CCT.
>
> Before this CL, only App Modal dialog is supported on CCT. This CL
> adds Tab Modal dialog to CCT and tests whether they can be
> correctly dismissed by navigation and back press.
>
> Bug: 1446709
> Change-Id: Id113b2c0bcae7284deb55f970ff2b30fc96177ee
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4706547
> Reviewed-by: Theresa Sullivan <twellington@chromium.org>
> Commit-Queue: Lijin Shen <lazzzis@google.com>
> Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
> Cr-Commit-Position: refs/heads/main@{#1175793}

Bug: 1446709, 1486017
Change-Id: I6bb31f485c26500b84ea731c307f24fc3720dcc2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4903131
Commit-Queue: Krishna Govind <govind@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Cr-Commit-Position: refs/branch-heads/5993@{#1049}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/4b4e0691149db980f2f6bad46e26ffeef9088f87/chrome/android/java/src/org/chromium/chrome/browser/ui/RootUiCoordinator.java
[modify] https://crrev.com/4b4e0691149db980f2f6bad46e26ffeef9088f87/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/4b4e0691149db980f2f6bad46e26ffeef9088f87/chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java
[modify] https://crrev.com/4b4e0691149db980f2f6bad46e26ffeef9088f87/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java
[modify] https://crrev.com/4b4e0691149db980f2f6bad46e26ffeef9088f87/chrome/android/java/src/org/chromium/chrome/browser/tabbed_mode/TabbedRootUiCoordinator.java
[modify] https://crrev.com/4b4e0691149db980f2f6bad46e26ffeef9088f87/chrome/android/java/src/org/chromium/chrome/browser/customtabs/BaseCustomTabActivity.java


### pg...@google.com (2023-10-06)

Re-opening this as the fix has been reverted

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-04)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/35fc109dd382d2961cbffe4b3f181a48644af819

commit 35fc109dd382d2961cbffe4b3f181a48644af819
Author: Lijin Shen <lazzzis@google.com>
Date: Tue Dec 12 19:05:42 2023

Re-Introduce Tab Modal dialog to CCT.

Before this CL, only App Modal dialog is supported on CCT. This CL
adds Tab Modal dialog to CCT and tests whether they can be
correctly dismissed by navigation and back press.

This CL also adds a default enabled flag.

Previous CL: https://crrev.com/c/4706547

In previous CL, since PWA/TWA extends BaseCCTActivity, they can also
request to show a tab modal dialog. But since there is no browser
UI on PWA/TWA, the tab modal dialog is always suspended and no dialog
is shown as a result.

This CL fixes that by only allowing CCTActivity to initialize a
tab modal handler, such that CCT can now a tab modal dialog and
PWA/TWA is still only allowed to show APP modal dialogs.

Bug: 1446709, 1509163
Change-Id: Id5f13f6348b02efb3b31d1f524bbb6003a9a4712
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4913775
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Lijin Shen <lazzzis@google.com>
Cr-Commit-Position: refs/heads/main@{#1236474}

[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/java/src/org/chromium/chrome/browser/ui/RootUiCoordinator.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabActivity.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/javatests/src/org/chromium/chrome/browser/webapps/WebApkActivityTest.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/java/src/org/chromium/chrome/browser/customtabs/BaseCustomTabActivity.java
[add] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabModalDialogTest.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/browser/flags/android/chrome_feature_list.h
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/javatests/src/org/chromium/chrome/browser/webapps/WebappNavigationTest.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/OWNERS
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/java/src/org/chromium/chrome/browser/customtabs/BaseCustomTabRootUiCoordinator.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/browser/flags/android/chrome_feature_list.cc
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/java/src/org/chromium/chrome/browser/tabbed_mode/TabbedRootUiCoordinator.java
[modify] https://crrev.com/35fc109dd382d2961cbffe4b3f181a48644af819/chrome/android/chrome_test_java_sources.gni


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1446709?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Mobile>CompositedUI, UI>Browser>Mobile>CustomTabs, UI>Browser>Mobile>Messages, UI>Browser>WebAppInstalls>Android]
[Monorail mergedwith: crbug.com/chromium/1442434]
[Monorail components added to Component Tags custom field.]

### la...@google.com (2024-03-27)

See [crbug.com/330175031](https://crbug.com/330175031)

### dm...@google.com (2024-07-10)

As per Ella - "the issue is with the model dialog in Clank, twellington@'s team owns this space. Maybe "UI>Browser>Mobile>Messages""

### tw...@chromium.org (2024-07-10)

Lijin, why was this reopened at #59? What's the remaining work?

### la...@google.com (2024-07-10)

I can't recall why I reopened that. Perphas a misoperation. I think this should have been fixed by [crbug.com/330175031](https://crbug.com/330175031)

### pe...@google.com (2024-10-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064636)*
