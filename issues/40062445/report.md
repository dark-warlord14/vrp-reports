# Security:  (Android) PWA Install prompt can be overlaid over other origins.

| Field | Value |
|-------|-------|
| **Issue ID** | [40062445](https://issues.chromium.org/issues/40062445) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls>Android |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ei...@chromium.org |
| **Created** | 2022-12-30 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

I found that by changing the PoC a little, it is indeed possible to reproduce <https://bugs.chromium.org/p/chromium/issues/detail?id=1404001> on Android.

On Android, there are two types of installation prompts for PWAs

(1) Installation prompt with description and screenshot fields. This causes a popup from the bottom. This can be seen in <https://coordinated-tartan-individual.glitch.me/a2hs-poc.html>

(2) Installation prompt without description and screenshot fields. This causes a box to be drawn in the middle. This can be seen in <https://shade-cactus-dragon.glitch.me/a2hs-poc.html>

The installation prompt for (1) will disappear on Android when it navigates to other origins - ref: <https://jewel-chip-panama.glitch.me/a2hs-poc.html>. On the other hand, the installation prompt for (2) will NOT disappear when Android navigates to other origins.

**VERSION**  

Chrome Version: [108.0.5359.128]  

Operating System: [Android 11]

**REPRODUCTION CASE**

1. On Android, go to <https://shade-cactus-dragon.glitch.me/a2hs-poc.html>
2. Press when tick appears. The prompt appears and Android will navigate to <https://microsoft.com> at the same time.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [a2hs-poc.html](attachments/a2hs-poc.html) (text/plain, 939 B)
- [app.js](attachments/app.js) (text/plain, 1.7 KB)
- [app.webmanifest](attachments/app.webmanifest) (application/octet-stream, 622 B)
- [dummy-sw.js](attachments/dummy-sw.js) (text/plain, 156 B)
- [phishing.html](attachments/phishing.html) (text/plain, 731 B)
- [style.css](attachments/style.css) (text/plain, 868 B)
- [mobizen_20221230_155420.mp4](attachments/mobizen_20221230_155420.mp4) (video/mp4, 1.4 MB)
- [mobizen_20230117_011517.mp4](attachments/mobizen_20230117_011517.mp4) (video/mp4, 7.8 MB)

## Timeline

### [Deleted User] (2022-12-30)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-12-30)

The key difference in the PoCs is in app.webmanifest, description and screenshot fields are removed, this triggers prompt (2) to appear.

### ha...@gmail.com (2022-12-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-03)

Copying labels from https://bugs.chromium.org/p/chromium/issues/detail?id=1404001

[Monorail components: UI>Browser>WebAppInstalls]

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2023-01-05)

Moving to Android component within WebAppInstalls since this bug is Android specific.

[Monorail components: -UI>Browser>WebAppInstalls UI>Browser>WebAppInstalls>Android]

### ei...@chromium.org (2023-01-05)

assign to myself and move Dan to cc


### gi...@appspot.gserviceaccount.com (2023-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5e9547cb44713c1944f499c8b633aaa43fb46013

commit 5e9547cb44713c1944f499c8b633aaa43fb46013
Author: Ella Ge <eirage@chromium.org>
Date: Mon Jan 16 15:52:45 2023

Change AddToHomescreen dialog to ModalDialogType.TAB

The install/A2HS dialog should dismiss with tab navigation or destroy

Bug: 1404230
Change-Id: I62b87732a6f7bf29f864786d94dd66d351391038
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4153171
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Commit-Queue: Ella Ge <eirage@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1093070}

[modify] https://crrev.com/5e9547cb44713c1944f499c8b633aaa43fb46013/components/webapps/browser/android/java/src/org/chromium/components/webapps/AddToHomescreenDialogView.java
[modify] https://crrev.com/5e9547cb44713c1944f499c8b633aaa43fb46013/chrome/browser/banners/android/java/src/org/chromium/chrome/browser/banners/AppBannerManagerTest.java


### ei...@chromium.org (2023-01-16)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-01-16)

Forgot to mention the security implication of downloading a malicious PWA:

The security implication is that a user who is tricked into installing a PWA may be convinced that they have downloaded the real "Microsoft Teams" app / PWA. This can  lead to phishing of the user as the user thinks that the PWA is the real Microsoft Teams app and the PWA lacks any omnibox.

### [Deleted User] (2023-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-16)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations, Axel! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-02)

For some reason the bot does not request merge approval for certain medium severity bugs. Since M110 becomes Stable next week, please merge this fix to M110, branch 5418 so it can be included in the first M110/Stable refresh. Thank you!

### gi...@appspot.gserviceaccount.com (2023-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a54a8c5e6b8ee10c19bd8982353dbb451aedd7b0

commit a54a8c5e6b8ee10c19bd8982353dbb451aedd7b0
Author: Ella Ge <eirage@chromium.org>
Date: Thu Feb 02 23:53:55 2023

[M110]Change AddToHomescreen dialog to ModalDialogType.TAB

The install/A2HS dialog should dismiss with tab navigation or destroy

(cherry picked from commit 5e9547cb44713c1944f499c8b633aaa43fb46013)

Bug: 1404230
Change-Id: I62b87732a6f7bf29f864786d94dd66d351391038
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4153171
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Commit-Queue: Ella Ge <eirage@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1093070}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4219346
Cr-Commit-Position: refs/branch-heads/5418@{#3}
Cr-Branched-From: 0b8917a0141e6f9ab16a9c0ac880807964d44679-refs/heads/main@{#1070820}

[modify] https://crrev.com/a54a8c5e6b8ee10c19bd8982353dbb451aedd7b0/components/webapps/browser/android/java/src/org/chromium/components/webapps/AddToHomescreenDialogView.java
[modify] https://crrev.com/a54a8c5e6b8ee10c19bd8982353dbb451aedd7b0/chrome/browser/banners/android/java/src/org/chromium/chrome/browser/banners/AppBannerManagerTest.java


### [Deleted User] (2023-02-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-06)

has been merged, removing merge approval label

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1404230?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062445)*
