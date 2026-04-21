# Security: Android Text Selection Menu Able to Overlap Fullscreen Notification Toast

| Field | Value |
|-------|-------|
| **Issue ID** | [40062567](https://issues.chromium.org/issues/40062567) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2023-01-10 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

After <https://crbug.com/chromium/1264561> has been fixed, the full screen notification toast now displayed using Custom Toast view, I found Android text selection menu able to overlap the fullscreen toast so user don't see the toast.

On the attached testcase.html the Android text selection menu has been adjusted to fits well to overlap toast on Pixel\_2\_API\_33 and Pixel\_4\_API\_33

**VERSION**

- Chrome Canary 111.0.5529.0 on Android 13; Pixel\_4\_API\_33
- Chrome Canary 111.0.5529.0 on Android 13; Pixel\_2\_API\_33
- Chrome Dev 110.0.5481.23 on Android 13; Pixel\_4\_API\_33
- Chrome Dev 110.0.5481.23 on Android 13; Pixel\_2\_API\_33

**REPRODUCTION CASE**

1. Visit attached testcase.html
2. Tap anywhere on the page
3. Android text selection menu overlap the fullscreen notification toast

**CREDIT INFORMATION**  

Irvan Kurniawan (sourc7)

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 544 B)
- [Android Text Selection Menu overlap Fullscreen Toast on Pixel_2_API_33.webm](attachments/Android Text Selection Menu overlap Fullscreen Toast on Pixel_2_API_33.webm) (video/webm, 722.6 KB)
- [testcase-gspoof.html](attachments/testcase-gspoof.html) (text/plain, 865.5 KB)
- [Chrome Dev - testcase-gspoof.html on Pixel_4_API_33.webm](attachments/Chrome Dev - testcase-gspoof.html on Pixel_4_API_33.webm) (video/webm, 8.4 MB)

## Timeline

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-01-13)

I'm able to repro this in beta (110.0.5481.29) but not in stable (108.0.5359.128). I'm not sure what happened to M109 here; I'm going to tag with FoundIn-109 out of an abundance of caution (someone should test 109 and validate if this bug happens there or not).

[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2023-01-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-01-13)

Also, it might be worth noting that the overlap is not complete on my test platform; however, I'm guessing this probably depends on device and UI scale.

### [Deleted User] (2023-01-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-24)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2023-01-24)

Working on it now

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e3909a77753d55778f5c23b978c80abf6fd5aab1

commit e3909a77753d55778f5c23b978c80abf6fd5aab1
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Thu Mar 02 19:55:08 2023

Fullscreen notification uses Android Toast

This CL switches fullscreen notification from using a custom view back
to using Android toast widget. The custom view-based implementation
caused lots of conflict cases with other views within Chrome. With
limit-rating capability/priority mechanism installed, Android toast
can hopefully avoid them.

The change is behind a feature flag android-widget-fullscreen-toast,
and enabled by default.

Bug: 1406120
Change-Id: I20107ce9ad23df63fd185680022c06a792b9c6e1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4263951
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1112382}

[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/browser/flag_descriptions.cc
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/browser/about_flags.cc
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/browser/flag_descriptions.h
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/browser/flag-metadata.json
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/android/chrome_java_sources.gni
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/browser/flags/android/chrome_feature_list.h
[add] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenToast.java
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java
[modify] https://crrev.com/e3909a77753d55778f5c23b978c80abf6fd5aab1/chrome/browser/flags/android/chrome_feature_list.cc


### ji...@chromium.org (2023-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### su...@gmail.com (2023-03-08)

Thanks! I confirmed this has been fixed on Chrome Canary 113.0.538.0

For a better spoof demonstration video, here the updated test case which impersonate google login page + automatically trigger keyboard.

### am...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations Irvan! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1406120?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1409153, crbug.com/chromium/1409198, crbug.com/chromium/1411678, crbug.com/chromium/1413056, crbug.com/chromium/1414503, crbug.com/chromium/1421471, crbug.com/chromium/1422293, crbug.com/chromium/1423137]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062567)*
