# Security: PWA dialog selects an install button by default Bypassing Google Security Measures in Chrome UI 

| Field | Value |
|-------|-------|
| **Issue ID** | [40064335](https://issues.chromium.org/issues/40064335) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-05-02 |
| **Bounty** | $1,500.00 |

## Description

## **VULNERABILITY DETAILS**

The PWA dialog has the "install" button focused by default. This presents an issue as this makes the dialog key-jackable,Bypassing Google Security measures in Chrome UI sensitive area `installing PWA` which lead to (user information disclosure without being aware) and

In a regular keyjacking attack (also works in this case), the Enter key would have to be pressed twice.

What is likely happening (if key events are propagated `keydown`:

1. The page listens for the Enter `keydown` event.
2. The page opens a PWA dialog, with the 1st keyevent,and 2nd keypress accepts the install because it is default to install not cancel.
3. The PWA dialog receives an Enter `keypress`, and the default confirm button is pressed.

## Impact:

User Can be Tricked to press Enter key twice in game and Unknowingly install PWA Apps that could be Like legit Ones and user can provide passwords and sensitive data in , and send his data to Attacker C&C server without suspect as he didn't see accept/install button,nobody will send critical information to unknown sites. but this can be done here, in this case nobody are able to notice that they are sending their data to unknown attackers or non legit apps (user information disclosure without being aware) and ( Bypassing Google Security measures in Chrome UI sensitive area `installing PWA`).

# **VERSION**

Exploit tested with the following properties:

## Chrome Version: 112.0.5615.138 (Official Build) (64-bit) (cohort: Stable) Revision: b160f1d9e90aa6940d17d5cb44d9e815205d2024-refs/branch-heads/5615@{#1281} OS: Windows 11 Version 22H2 (Build 22621.1635)

## Google Chrome: 115.0.5747.0 (Official Build) canary (64-bit) (cohort: Clang-64) Revision: bfbf32ed7b1be2d640ce1be293d964700e1b56e2-refs/branch-heads/5747@{#1} OS: Windows 11 Version 22H2 (Build 22621.1635)

## Google Chrome: 114.0.5735.6(Official Build)dev(64-bit) Branch:5735 Branch Base Position: 1135570 OS: Linux

## Google Chrome:112.0.5615.165 (Official Build)(64-bit)-stable Branch:5615 Branch Base Position:1109224

**REPRODUCTION CASE**

1. Host the attached files of simple PWA App on your Server and test , or simply Use Online Poc
2. Navigate <https://vrphunt.com/chrome/spooforigin/a2hs-poc.html>
3. Press `Enter twice immediately` , you will see PWA app installed and a new simple page Requesting Username and password.

## Observed:

PWA dialog selects an install button by default Bypassing Google Security Measures in Chrome

## Expected:

According to References Below

# Don't have a default-selected accept button

-PWA dialog should selects cancel button by default instead of install button.

# References:

Docs (docs/security/security-considerations-for-browser-ui.md):

> # Don't have a default-selected accept button
> 
> If your dialog or UI has a call-to-action triggered by a button that is default-selected, the dialog is subject to keyjacking. An evil webpage can trick a user into mashing or repeatedly hitting the Enter key especially in games, and then trigger your dialog to show, causing the user to unknowingly accept and install the PWA.

## \*PoC Videos for Linux Tests in the following URLs:

Stable: <https://drive.google.com/file/d/1WYVCgj_h8fhShvXNcBHz7ehxU7toXgCy/view?usp=sharing>  

Dev: <https://drive.google.com/file/d/1Pqsf6RPnFH7r8q0g6p0wK_n-5hrJ2L_4/view?usp=sharing>

\*\*Poc Videos of Windows Tests Directly Attached  

\*\*Local Offline PWA Files (Poc) Directly Attached

**CREDIT INFORMATION**  

Reporter credit: Ahmed ElMasry

## Attachments

- [pwa-app-install-accept.js](attachments/pwa-app-install-accept.js) (text/plain, 2.0 KB)
- [a2hs-poc.html](attachments/a2hs-poc.html) (text/plain, 1.1 KB)
- [pwa-app.webmanifest](attachments/pwa-app.webmanifest) (application/octet-stream, 622 B)
- [dummy-sw.js](attachments/dummy-sw.js) (text/plain, 156 B)
- [phishing.html](attachments/phishing.html) (text/plain, 731 B)
- [style.css](attachments/style.css) (text/plain, 868 B)
- [Canary-WIN 2023-05-02 22-45-02-887.mp4](attachments/Canary-WIN 2023-05-02 22-45-02-887.mp4) (video/mp4, 2.0 MB)
- [Stable-WIN  2023-05-02 22-36-43-208.mp4](attachments/Stable-WIN  2023-05-02 22-36-43-208.mp4) (video/mp4, 2.5 MB)

## Timeline

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-05-03)

+DPWA team. Ideally the dialog should avoid focusing the omnibox install button per [1]. 

1. https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-considerations-for-browser-ui.md#don_t-have-a-default_selected-accept-button

[Monorail components: UI>Browser>WebAppInstalls]

### do...@chromium.org (2023-05-03)

(also: thanks reporter for sending this in)

### [Deleted User] (2023-05-03)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-05-03)

To clarify my comment in #2: it should be the install dialog and possibly the omnibox chip that need to avoid the default focus.

### [Deleted User] (2023-05-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### di...@chromium.org (2023-05-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/82bf83a0639fbcd6c8daaf7a67ab6ce4f5654551

commit 82bf83a0639fbcd6c8daaf7a67ab6ce4f5654551
Author: Dibyajyoti Pal <dibyapal@google.com>
Date: Fri May 05 14:08:09 2023

[dPWA] Make Cancel button default on PWA install dialogs.

To prevent keyjacking schemes, ensure that the Cancel button is set as
the default button instead of the Accept one so that users spoofed
with multiple Enter keys do not install a spoofed app by mistake.

The fix cannot be applied to the NONE button on the new detailed
installed dialog because the DialogBuilder does not allow making
buttons that are not implemented default.

Bug: 1442018
Change-Id: I94ea8558877698bca138ce50e62a213f58b973f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4505003
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1140100}

[modify] https://crrev.com/82bf83a0639fbcd6c8daaf7a67ab6ce4f5654551/chrome/browser/ui/views/web_apps/pwa_confirmation_bubble_view.cc
[modify] https://crrev.com/82bf83a0639fbcd6c8daaf7a67ab6ce4f5654551/chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog.cc


### di...@chromium.org (2023-05-05)

[Empty comment from Monorail migration]

### di...@chromium.org (2023-05-05)

Requesting merge approval to M113 and M114, this is a security issue that needs to be patched.

### di...@chromium.org (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-06)

Merge review required: M114 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-06)

Merge review required: M113 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### di...@chromium.org (2023-05-08)

For M114 release:

1. This fixes a keyjacking medium security issue on the PWA installation dialog, and requires merging to stable channels after M112.
2. This is the fix that will be merged: https://chromium-review.googlesource.com/c/chromium/src/+/4505003
3. Yes, the changes have been released and tested on canary.
4. No, this is not behind a Finch Flag.
5. +jinrongwu@ fyi
6. This requires a fix to Stable, so manual testing steps:

For the normal installation bubble:
1. Navigate to https://vrphunt.com/chrome/spooforigin/a2hs-poc.html
2. Wait for app to finish loading, press enter twice.
3. Verify app is not installed on chrome://apps (the first enter focuses on the omnibox icon and clicks on it, the 2nd enter opens the installation dialog and closes it).

For the detailed PWA installation bubble:
1. Navigate to https://squoosh.app/
2. Wait for app to finish loading, and press tab to navigate to the omnibox install icon.
3. Once the icon is highlighted, press enter twice.
4. Verify app is not installed on chrome://apps.

### di...@chromium.org (2023-05-08)

For M113 release:

1. This fixes a keyjacking medium security issue on the PWA installation dialog, and requires merging to stable channels after M112.
2. This is the fix that will be merged: https://chromium-review.googlesource.com/c/chromium/src/+/4505003
3. Yes, the changes have been released and tested on canary.
4. No, this is not behind a Finch Flag.
5. +jinrongwu@ fyi
6. This requires a fix to Stable, so manual testing steps:

For the normal installation bubble:
1. Navigate to https://vrphunt.com/chrome/spooforigin/a2hs-poc.html
2. Wait for app to finish loading, press enter twice.
3. Verify app is not installed on chrome://apps (the first enter focuses on the omnibox icon and clicks on it, the 2nd enter opens the installation dialog and closes it).

For the detailed PWA installation bubble:
1. Navigate to https://squoosh.app/
2. Wait for app to finish loading, and press tab to navigate to the omnibox install icon.
3. Once the icon is highlighted, press enter twice.
4. Verify app is not installed on chrome://apps.

### di...@chromium.org (2023-05-08)

[Empty comment from Monorail migration]

### di...@chromium.org (2023-05-08)

Slight change in Q5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents after discussion for both M113 and M114:

We will not need ChromeOS approval since this affects the dialog that is only seen on Chrome browser and is not connected to the ChromeOS system in any way.

### am...@chromium.org (2023-05-09)

M114 merge approved, please merge this fix to branch 5735 by EOD tomorrow / Tuesday 9 May so this fix can be included in the next M114/Beta release 


M113 merge approved, please merge to branch 5672 by EOD Friday, 12 May so this fix can be included in the next M113/Stable update 
M112 merge approved, please merge to branch 5615 by the above deadline so this fix can be included in the next M112/Extended Stable udpate 

### gi...@appspot.gserviceaccount.com (2023-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/998645c5c452b7ccbad3402e0f243af887a519ad

commit 998645c5c452b7ccbad3402e0f243af887a519ad
Author: Dibyajyoti Pal <dibyapal@google.com>
Date: Tue May 09 15:15:10 2023

[dPWA][M113] Make Cancel button default on PWA install dialogs.

To prevent keyjacking schemes, ensure that the Cancel button is set as
the default button instead of the Accept one so that users spoofed
with multiple Enter keys do not install a spoofed app by mistake.

The fix cannot be applied to the NONE button on the new detailed
installed dialog because the DialogBuilder does not allow making
buttons that are not implemented default.

(cherry picked from commit 82bf83a0639fbcd6c8daaf7a67ab6ce4f5654551)

Bug: 1442018
Change-Id: I94ea8558877698bca138ce50e62a213f58b973f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4505003
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1140100}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4516718
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Dibyajyoti Pal <dibyapal@chromium.org>
Cr-Commit-Position: refs/branch-heads/5672@{#1137}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/998645c5c452b7ccbad3402e0f243af887a519ad/chrome/browser/ui/views/web_apps/pwa_confirmation_bubble_view.cc
[modify] https://crrev.com/998645c5c452b7ccbad3402e0f243af887a519ad/chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog.cc


### gi...@appspot.gserviceaccount.com (2023-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1cd6314657765047b9920129cb1dd69530f17d6a

commit 1cd6314657765047b9920129cb1dd69530f17d6a
Author: Dibyajyoti Pal <dibyapal@google.com>
Date: Tue May 09 15:16:40 2023

[dPWA][M114] Make Cancel button default on PWA install dialogs.

To prevent keyjacking schemes, ensure that the Cancel button is set as
the default button instead of the Accept one so that users spoofed
with multiple Enter keys do not install a spoofed app by mistake.

The fix cannot be applied to the NONE button on the new detailed
installed dialog because the DialogBuilder does not allow making
buttons that are not implemented default.

(cherry picked from commit 82bf83a0639fbcd6c8daaf7a67ab6ce4f5654551)

Bug: 1442018
Change-Id: I94ea8558877698bca138ce50e62a213f58b973f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4505003
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1140100}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4517241
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Dibyajyoti Pal <dibyapal@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#430}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/1cd6314657765047b9920129cb1dd69530f17d6a/chrome/browser/ui/views/web_apps/pwa_confirmation_bubble_view.cc
[modify] https://crrev.com/1cd6314657765047b9920129cb1dd69530f17d6a/chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog.cc


### gi...@appspot.gserviceaccount.com (2023-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4973f896432feaaaa90ca1258ca4dfe712ab2268

commit 4973f896432feaaaa90ca1258ca4dfe712ab2268
Author: Dibyajyoti Pal <dibyapal@google.com>
Date: Tue May 09 16:23:56 2023

[dPWA][M112] Make Cancel button default on PWA install dialogs.

To prevent keyjacking schemes, ensure that the Cancel button is set as
the default button instead of the Accept one so that users spoofed
with multiple Enter keys do not install a spoofed app by mistake.

The fix cannot be applied to the NONE button on the new detailed
installed dialog because the DialogBuilder does not allow making
buttons that are not implemented default.

(cherry picked from commit 82bf83a0639fbcd6c8daaf7a67ab6ce4f5654551)

Bug: 1442018
Change-Id: I94ea8558877698bca138ce50e62a213f58b973f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4505003
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1140100}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4517182
Auto-Submit: Dibyajyoti Pal <dibyapal@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5615@{#1411}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/4973f896432feaaaa90ca1258ca4dfe712ab2268/chrome/browser/ui/views/web_apps/pwa_confirmation_bubble_view.cc
[modify] https://crrev.com/4973f896432feaaaa90ca1258ca4dfe712ab2268/chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog.cc


### di...@chromium.org (2023-05-09)

Merged to M112, M113 and M114.

### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations, Ahmed! The VRP Panel has decided to award you $1,000 for this report + $500 as a partial bisect bonus. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-05-15)

Hello Amy..,

Thank you so much for the Reward!
Could you please reopen this( https://crbug.com/chromium/1442434) as it was mistakenly closed won't-fix , but the bug found and repro.

Thanks, Appreciate your time and help.

### am...@chromium.org (2023-05-15)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-05-15)

amyressler@


### am...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-01)

https://crbug.com/chromium/1403836 is a much earlier report of this issue and was closed based on the landing of https://chromium-review.googlesource.com/c/chromium/src/+/4505003 the fix for this issue. Merging this report into the earlier version now that merges are complete. 

### [Deleted User] (2023-08-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1442018?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1403836]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064335)*
