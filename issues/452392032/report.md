# When in split-view mode, the mini address bar does not appear above the virtual keyboard, leading to a spoof.

| Field | Value |
|-------|-------|
| **Issue ID** | [452392032](https://issues.chromium.org/issues/452392032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2025-10-16 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS
This vulnerability is similar to https://issues.chromium.org/issues/439262604 (iOS version), but this bug occurs on the Android version. When in split-view mode, the mini address bar does not appear above the virtual keyboard.

VERSION
Chrome Version: [143.0.7472.0] + [Canary]
Operating System: Android 16
Device: Samsung S25 Edge

REPRODUCTION CASE
1. Open https://you-can-billowy-nimble-login-secure-docs-google-source-attacker.com/spoofnewxiov.html or open spoofnewxiov.html on a local web server using the https:// protocol and open it in split-view mode.
2. Click on the "google" link.


## Attachments

- [spoofsplitview.mp4](attachments/spoofsplitview.mp4) (video/mp4, 6.0 MB)
- [spoofnewxiov.html](attachments/spoofnewxiov.html) (text/html, 3.5 KB)
- [8eWXXFfj3qsanP5.png](attachments/8eWXXFfj3qsanP5.png) (image/png, 278.8 KB)
- [Screenshot_20251018_182618_Chrome Canary~2.jpg](attachments/Screenshot_20251018_182618_Chrome Canary~2.jpg) (image/jpeg, 207.9 KB)

## Timeline

### dr...@chromium.org (2025-10-17)

[security triage] Thanks for the report. This does not reproduce for me. I see the chip as intended. Is this specific to certain devices? Certain settings?

### sa...@gmail.com (2025-10-17)

It is affected on split mode screen. I see at your screenshoot you didnt  tested on split mode screen

### sa...@gmail.com (2025-10-17)

I reproduced using samsung 25 edge. There is no other certains settings

### pe...@google.com (2025-10-17)

Thank you for providing more feedback. Adding the requester to the CC list.

### sa...@gmail.com (2025-10-18)

You must test using https:// and domain to autofill toolbar is shown i see in you screenshoot the autofill toolbar is not shown

### dr...@chromium.org (2025-10-20)

Got it, thanks. I did have split screen (the "Got it" at the top of my screenshot was gmail), but the https requirement was what I was missing. For posterity, the prerequisites here are:

- Address bar is on the bottom
- Split screen is active
- The site is secure (either HTTPS or listed in #unsafely-treat-insecure-origin-as-secure)

That made it reproduce once in M140, but I've still struggled to get it to happen since. So there might be another requirement in there (something in autofill logic, maybe?) Either way, this is good enough for me.

### sa...@gmail.com (2025-10-21)

It seems like this is because the minibar position doesn't reach the top due to the limited screen and autofill is displayed. This is different from when autofill is not displayed, the minibar still appears.

### ch...@google.com (2025-10-21)

Setting milestone because of s2 severity.

### ch...@google.com (2025-10-21)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pn...@google.com (2025-10-21)

> It seems like this is because the minibar position doesn't reach the top due to the limited screen and autofill is displayed. This is different from when autofill is not displayed, the minibar still appears.

I think you're right that this is a failure to coordinate positions with the autofill bar

### dx...@google.com (2025-10-22)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7069866>

[mobar] Fix keyboard accessory overlap in multiwindow

---


Expand for full commit details
```
     
    For reasons as yet unknown to me, multi-window seems to cause 
    ToolbarControlContainer to not be drawn when its pre-translation 
    position overlaps with the keyboard accessory. This may be an 
    optimization of sorts; I was not able to turn it off by fiddling with 
    clipChildren/clipToBounds. 
     
    Instead, we resolve it by removing kb accessory height from the 
    translation calculation, using it instead to set the bottom margin. This 
    should be safe since we don't use the bottom margin for another purpose 
    and performant since the keyboard accessory doesn't change height often. 
     
    Two related issues are resolved at the same time: 
    * The revamped kb accessory reports the wrong height, referencing the 
      old dimen. This is changed to be feature aware. 
    * There is no insets animation in multiwindow, meaning minimization 
      progress isn't set properly. We now explicitly call it when skipping 
      the animation. 
     
    Bug: 452392032, 438136964 
    Change-Id: I0df6bffdbbb0885e70b5c7ff0614faa5447b93e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7069866 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1533841}

```

---

Files:

- M `chrome/android/features/keyboard_accessory/internal/java/src/org/chromium/chrome/browser/keyboard_accessory/ManualFillingMediator.java`
- M `chrome/android/features/keyboard_accessory/junit/src/org/chromium/chrome/browser/keyboard_accessory/ManualFillingControllerTest.java`
- M `chrome/browser/keyboard_accessory/android/internal/java/res/values/dimens.xml`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarController.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/ToolbarPositionController.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/ToolbarPositionControllerTest.java`

---

Hash: [316d6696542c7cd0307eeb8df3a914a8eda9989f](https://chromiumdash.appspot.com/commit/316d6696542c7cd0307eeb8df3a914a8eda9989f)  

Date: Wed Oct 22 19:30:26 2025


---

### pn...@google.com (2025-10-23)

Fixed in Canary.

### ch...@google.com (2025-10-24)

Security Merge Request Consideration: Requesting merge to beta (M142) because latest trunk commit (1533841) appears to be after beta branch point (1522585).
Security Merge Request - Manual Review: Merge review required: M142 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pn...@google.com (2025-10-24)

1. <https://chromium-review.googlesource.com/7069866>
2. Yes
3. No
4. No
5. No

### ya...@chromium.org (2025-10-24)

Please proceed with merging to M142.

### dx...@google.com (2025-10-27)

Project: chromium/src  

Branch:  refs/branch-heads/7444  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7081862>

[m142][mobar] Fix keyboard accessory overlap in multiwindow

---


Expand for full commit details
```
     
    For reasons as yet unknown to me, multi-window seems to cause 
    ToolbarControlContainer to not be drawn when its pre-translation 
    position overlaps with the keyboard accessory. This may be an 
    optimization of sorts; I was not able to turn it off by fiddling with 
    clipChildren/clipToBounds. 
     
    Instead, we resolve it by removing kb accessory height from the 
    translation calculation, using it instead to set the bottom margin. This 
    should be safe since we don't use the bottom margin for another purpose 
    and performant since the keyboard accessory doesn't change height often. 
     
    Two related issues are resolved at the same time: 
    * The revamped kb accessory reports the wrong height, referencing the 
      old dimen. This is changed to be feature aware. 
    * There is no insets animation in multiwindow, meaning minimization 
      progress isn't set properly. We now explicitly call it when skipping 
      the animation. 
     
    (cherry picked from commit 316d6696542c7cd0307eeb8df3a914a8eda9989f) 
     
    Bug: 452392032, 438136964 
    Change-Id: I0df6bffdbbb0885e70b5c7ff0614faa5447b93e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7069866 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1533841} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7081862 
    Reviewed-by: Luchen Peng <luchenpeng@google.com> 
    Cr-Commit-Position: refs/branch-heads/7444@{#2147} 
    Cr-Branched-From: 29907d3c18078029695f458b42fb8e6fda3e493d-refs/heads/main@{#1522585}

```

---

Files:

- M `chrome/android/features/keyboard_accessory/internal/java/src/org/chromium/chrome/browser/keyboard_accessory/ManualFillingMediator.java`
- M `chrome/android/features/keyboard_accessory/junit/src/org/chromium/chrome/browser/keyboard_accessory/ManualFillingControllerTest.java`
- M `chrome/browser/keyboard_accessory/android/internal/java/res/values/dimens.xml`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarController.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/ToolbarPositionController.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/ToolbarPositionControllerTest.java`

---

Hash: [d2ca6ac8e0f2ae4e36c5869f5dff8e818ce36257](https://chromiumdash.appspot.com/commit/d2ca6ac8e0f2ae4e36c5869f5dff8e818ce36257)  

Date: Mon Oct 27 16:06:23 2025


---

### sp...@google.com (2025-11-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
hides security sensitive ui but attacker does not control the UI. The panel thank you for your contribution but this bug is low security impact.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> hides security sensitive ui but attacker does not control the UI. The panel thank you for your contribution but this bug is low security impact.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/452392032)*
