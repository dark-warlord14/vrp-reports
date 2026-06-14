# Permissions request clickjacking flaw report:

| Field | Value |
|-------|-------|
| **Issue ID** | [40092965](https://issues.chromium.org/issues/40092965) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>WebAPKs, UI>Browser>Permissions>Prompts |
| **Platforms** | Android |
| **Reporter** | us...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2018-11-06 |
| **Bounty** | $2,000.00 |

## Description

Dear Chrome team and Android security team,

We're a security research group at Indiana University. Recently we studied Progressive Web App (PWA) on Android and discovered a critical clickjacking-style security flaw in its permission authorization affecting both the latest version of Chrome (v70.0.3538.80) and Android 9. On exploiting the flaw, a malicious PWA can access the private and sensitive information and resources (e.g., camera, microphone, location) of PWA users bypassing Chrome’s permission authorization [1]. Besides, a malicious Android native app can stealthily get such sensitive information and resources of PWA users without requiring any related Android Permissions [5], such as android.permission.ACCESS\_COARSE\_LOCATION. This problem breaks the security of both the Android OS and Chrome.

## **VULNERABILITY DETAILS**

Please refer to the attached report for more details.

## **VERSION**

Chrome Version: v70.0.3538.80 installed from Google Play  

Operating System: Android 9

## **REPRODUCTION CASE**

We made 2 demo videos for the security flaws we mentioned in the report.

Security Flaw 1 Demo Video: <https://drive.google.com/open?id=1U3T_c44eFMWWqtA9Lq3kWRcLoKiBS9Xk>

Security Flaw 2 Demo Video, <https://drive.google.com/open?id=18IjtY2XcYGHiXEwO8lPi0yz343etPJOF>

Here is the source code of the MalAPK we used for the demo. Please make sure to grant the "System\_Alert\_Window" before you run the demo or it may crush.  

<https://drive.google.com/file/d/1KlPutHRyj52qz0FuGiaoY1TfL7gMcNpT/view?usp=sharing>

Haoran Lu, Yifan Zhang, Luyi Xing, Xiaojing Liao  

Indiana University Bloomington  

11/4/2018

## Attachments

- [PWA Overlay Bug Report.pdf](attachments/PWA Overlay Bug Report.pdf) (application/pdf, 164.1 KB)
- [filter_touch.mp4](attachments/filter_touch.mp4) (video/mp4, 887.0 KB)
- [not_filter_touch.mp4](attachments/not_filter_touch.mp4) (video/mp4, 978.4 KB)

## Timeline

### ke...@chromium.org (2018-11-06)

+rsesek for comment.

### rs...@chromium.org (2018-11-06)

Thanks for the report - this is an interesting demonstration of coordination between a PWA and malicious APK. As you note in your report, the SYSTEM_ALERT_WINDOW permission is powerful and Android are restricting its automatic grant on newer targetSdks.

I think a potential mitigation in Chrome/WebAPKs would be to protect the permission prompt UI. While third-party apps cannot use the signature|installer permission HIDE_NON_SYSTEM_OVERLAY_WINDOWS, there are ways to detect overlays. I think setting View.setFilterTouchesWhenObscured(true) on the prompt might be sufficient, but we can also implement our own security policy with View.onFilterTouchEventForSecurity().

I'm going to tentatively label this as Severity-Medium because of the mitigating factor of needing a coordinated malicious app installed.

N.B. This was cross-reported to Android at b/119096141.

[Monorail components: Mobile>WebAPKs UI>Browser>Permissions>Prompts]

### yf...@chromium.org (2018-11-06)

+dominick to comment on permissions side
+ted for UI options if there are any as Robert is alluding to

I'm not sure why this would be webapk specific - please help clarify? Peter points out that it may be extra confusing to users since Webapks don't show android permissions in settings but that's arguably orthogonal. It seems like the critical bit is that when chrome prompts for a permission request it can be overlaid.


### ke...@chromium.org (2018-11-06)

It isn't specific to WebAPKs, I believe the suggestion is just that Chrome has the ability to prevent this behavior and it might be worth doing so.

### yf...@chromium.org (2018-11-06)

Cool, thanks. So we're on the same page.

From a brief amount of codesearching, I agree with rsesek that it seems like the right fix. Interestingly, I don't see other usages of this API in our code. Presumably we have other surfaces that should have similar checks? Not sure it makes sense for pkotwicz to run with all of this or to have someone from security audit?

### te...@chromium.org (2018-11-06)

+huayinz

Permissions use ModalDialogManager right?  Can use use setFilterTouchesWhenObscured for all buttons or potentially all dialogs we show in Chrome (or at least permissions dialogs)?

### do...@chromium.org (2018-11-06)

#6's approach sounds ideal here. :)

### hu...@chromium.org (2018-11-06)

No... Only permission dialog in VR uses the ModalDialogManager, see https://cs.chromium.org/chromium/src/chrome/android/java/src/org/chromium/chrome/browser/permissions/PermissionDialogView.java?q=PermissionDialogView&sq=package:chromium&dr=CSs&l=22

But we can definitely change it.

### sh...@chromium.org (2018-11-07)

[Empty comment from Monorail migration]

### yf...@chromium.org (2018-11-07)

Probably makes sense then for Becky to run with this?

### hu...@chromium.org (2018-11-07)

Let's fix it for the permission dialog buttons using setFilterTouchesWhenObscured first so that it can be merged to M71. The migration to ModalDialogManager can happen later.

### bu...@chromium.org (2018-11-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0d7b74a398de964f71cf79eb216de001e0a9a3d5

commit 0d7b74a398de964f71cf79eb216de001e0a9a3d5
Author: Becky Zhou <huayinz@chromium.org>
Date: Wed Nov 07 23:38:05 2018

Filter focus for buttons when there are overlays on top

Bug: 902427
Change-Id: Ida893cf41478976f4d3784091a79385db69ef1f0
Reviewed-on: https://chromium-review.googlesource.com/c/1324450
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Commit-Queue: Becky Zhou <huayinz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#606212}
[modify] https://crrev.com/0d7b74a398de964f71cf79eb216de001e0a9a3d5/chrome/android/java/src/org/chromium/chrome/browser/permissions/PermissionDialogView.java
[modify] https://crrev.com/0d7b74a398de964f71cf79eb216de001e0a9a3d5/ui/android/java/res/values-v17/styles.xml


### hu...@chromium.org (2018-11-08)

Requesting a merge to M71 on a small change on the permission dialog button that prevents this security issue. Will only merge part of the above CL to lower risk, see https://chromium-review.googlesource.com/c/chromium/src/+/1324876/2

### sh...@chromium.org (2018-11-08)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-11-08)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@chromium.org (2018-11-08)

Approved for merge to 71, branch 3578.

### bu...@chromium.org (2018-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c8c00c99d84547c5203b522493359cf20f87cd3c

commit c8c00c99d84547c5203b522493359cf20f87cd3c
Author: Becky Zhou <huayinz@chromium.org>
Date: Fri Nov 09 00:40:41 2018

Filter focus for buttons when there are overlays on top

TBR=tedchoc@chromium.org

Bug: 902427
Change-Id: Ida893cf41478976f4d3784091a79385db69ef1f0
Reviewed-on: https://chromium-review.googlesource.com/c/1324876
Reviewed-by: Becky Zhou <huayinz@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#596}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/c8c00c99d84547c5203b522493359cf20f87cd3c/chrome/android/java/src/org/chromium/chrome/browser/permissions/PermissionDialogView.java


### cr...@appspot.gserviceaccount.com (2018-11-09)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/c8c00c99d84547c5203b522493359cf20f87cd3c

Commit: c8c00c99d84547c5203b522493359cf20f87cd3c
Author: huayinz@chromium.org
Commiter: huayinz@chromium.org
Date: 2018-11-09 00:40:41 +0000 UTC

Filter focus for buttons when there are overlays on top

TBR=tedchoc@chromium.org

Bug: 902427
Change-Id: Ida893cf41478976f4d3784091a79385db69ef1f0
Reviewed-on: https://chromium-review.googlesource.com/c/1324876
Reviewed-by: Becky Zhou <huayinz@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#596}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### sh...@chromium.org (2018-11-09)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-11-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### us...@gmail.com (2018-11-12)

Dear Chrome team:

We carefully inspected your fix at [1] and think that the it won’t solve the problem as expected. In your fix [1], the method “setFilterTouchesWhenObscured()” [2] is applied to the two buttons in the authorization window. Although this is suggested mitigation by the official Android documentation [3], however, we find that it will not well solve the security problem. Indeed, to bypass the fix in [1], an attacker can still use an overlay to hide the text of the authorization window as long as he/she leaves the button not covered (or not wholly covered). 

The reason is, the method “seFilterTouchesWhenObscured()” depends on the “FLAG_WINDOW_IS_OBSCURED” flag [4] and discard a touch event only if this flag is set to true. However, during our experiment, we find that this flag will not be set if the touch event did not directly pass through the obscured area, and this behavior is different from what is officially documented [4], as quote below:

“This flag indicates that the window that received this motion event is partly or wholly obscured by another visible window above it.  This flag is set to true even if the event did not directly pass through the obscured area. A security sensitive application can check this flag to identify situations in which a malicious application may have covered up part of its content for the purpose of misleading the user or hijacking touches.  An appropriate response might be to drop the suspect touches or to take additional precautions to confirm the user's actual intent.”

Additionally, we find that although the flag “FLAG_WINDOW_IS_OBSCURED” does not work as documented, another flag “FLAG_WINDOW_IS_PARTIALLY_OBSCURED” may help us temporarily mitigate the problem. Specifically, the flag “FLAG_WINDOW_IS_PARTIALLY_OBSCURED” will be set to true even if the touch event did not directly pass through the obscured area. One can use the two flags together to mitigate the clickjacking attacks that we reported in this thread

We also looked at why the flag “FLAG_WINDOW_IS_OBSCURED” does not work as publicly documented and found the cause in the source code of ASOP. According to the current implementation [6][8], the “FLAG_WINDOW_IS_OBSCURED” flag is set only when the touch event’s coordinates fall inside the overlay [7]. “FLAG_WINDOW_IS_PARTIALLY_OBSCURED” flag was added later to deal with the situation when the view/window is at least partly obscured.  However, we find that this newer flag was considered a temporal workaround and therefore not exposed to the public. The related commit can be viewed at [5].
 
Reference:
[1] Code Commit, https://chromium-review.googlesource.com/c/chromium/src/+/1324876/4/chrome/android/java/src/org/chromium/chrome/browser/permissions/PermissionDialogView.java#b65

[2] Security API, https://developer.android.com/reference/android/view/View.html#setFilterTouchesWhenObscured(boolean)

[3] Android View Security, https://developer.android.com/reference/android/view/View#Security

[4] FLAG_WINDOW_IS_OBSCURED, https://developer.android.com/reference/android/view/MotionEvent#FLAG_WINDOW_IS_OBSCURED

[5] Related Commit, https://android.googlesource.com/platform/frameworks/native/+/cdcd8f2b25a4bf32bb7506fc98ba541d274c9a31%5E%21/#F0

[6] ASOP Source Code, line1303-1307,
https://android.googlesource.com/platform/frameworks/native/+/master/services/inputflinger/InputDispatcher.cpp#1303

[7] Checking Conditions, line 38-41, https://android.googlesource.com/platform/frameworks/native/+/master/services/inputflinger/InputWindow.cpp#38

[8] ASOP Source Code, line 1657-1696,
https://android.googlesource.com/platform/frameworks/native/+/master/services/inputflinger/InputDispatcher.cpp#1657


### hu...@chromium.org (2018-11-12)

Thanks for the detailed investigation! I checked the case you've described when the overlay window is not covering the buttons. Indeed, setFilterTouchesWhenObscured doesn't filter the case where the view is partially obscured, or not obscured.

I can totally see the clickjacking could still happen if the attacker just covers the content on the permission dialog, but not the buttons.

If that's the case, we might need to override onFilterTouchEventForSecurity(MotionEvent) to workaround. However, I worry that this might affect the overall usability. If a friendly overlay window is shown (e.g. data saving info bubble), we could block touch events without letting the user know what exactly is going on.

### hu...@chromium.org (2018-11-12)

I did a little more investigation, but sadly I don't find any good way to work around this issue.

The field FLAG_WINDOW_IS_PARTIALLY_OBSCURED mentioned in https://crbug.com/chromium/902427#c22 seems to be only introduced in M+, so will not cover all the versions we support. Another bigger issue is that on my test app, I see that FLAG_WINDOW_IS_PARTIALLY_OBSCURED will also be true even if the overlay window does not intersect with the view, so if using this to filter touch events, we could be introducing usability issue.

rsesek@ - Do you have contacts on the Android side that could comment on this?



### hu...@chromium.org (2018-11-12)

+kdeus@ from Android security.

### rs...@chromium.org (2018-11-15)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-11-29)

Re: #24: FLAG_WINDOW_IS_PARTIALLY_OBSCURED being M+ is better than not having any remediation. My read of the code is that the flag is set when the window containing the view is obscured. In this case, I think that'll just be the permission dialog prompt window, which is desired. Are you observing something different (e.g. z-ordering a UI element above the permission prompt but positioning it such that it does not overlap at all with the permission prompt)?

### sh...@chromium.org (2018-11-29)

huayinz: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2018-12-03)

Re #27, that's right. The flag will be applied to the window that the view is in. For some reason I was thinking that we only want to filter if the view covers the button before, but we definitely need to filter for the entire window. So the flag works ideal.

I wonder if we need to show a toast when the permission dialog is being obscured so that the user knows why the buttons are not working? rsesek@, do you know who could provide this string from a security perspective?

Below is what Android settings used:

"Because an app is obscuring a permission request, Settings can’t verify your response."

### hu...@chromium.org (2018-12-04)

videos after using FLAG_WINDOW_IS_PARTIALLY_OBSCURED.

### rs...@chromium.org (2018-12-04)

I think showing a toast may be useful, and re-using Android's string is probably okay. Maybe dominickn@ has thoughts on that? At the very least, run it by by the Chrome UX team.

If the fix to add FLAG_WINDOW_IS_PARTIALLY_OBSCURED is already done, I'd land that first and then follow-up with the toast.

### tw...@chromium.org (2018-12-04)

We typically do not use hidden APIs or reflection in Chrome since this isn't guaranteed to work across the broad swath of Android devices and versions that we support. I think a fix here is important and that we should proceed despite needing reflection, but I'd like to understand if there is room for improvement.

Does Android plan to add a public API that we can utilize to detect this sort of thing? From reading the comments in this bug, it sounds like FLAG_WINDOW_IS_PARTIALLY_OBSCURED was supposed to be a temporary fix, yet years later it seems to be the only solution.

### rs...@chromium.org (2018-12-04)

I don't know. I can't find any follow-up from the commit (https://android.googlesource.com/platform/frameworks/native/+/cdcd8f2b25a4bf32bb7506fc98ba541d274c9a31) relating to

"""
    We aren't exposing this as API since we plan on making the original
    flag more robust. This is really a workaround for system dialogs
    since we generally know their layout and screen position, and that
    they're unlikely to be overlapped by other applications.
"""

Also note that FLAG_WINDOW_IS_PARTIALLY_OBSCURED does not imply FLAG_WINDOW_IS_OBSCURED so both need to be checked.

### bu...@chromium.org (2018-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/332bf6886f8cb1a826f3dcfe46804bd4528cd434

commit 332bf6886f8cb1a826f3dcfe46804bd4528cd434
Author: Becky Zhou <huayinz@chromium.org>
Date: Wed Dec 05 00:08:51 2018

Filter touch events for permission dialog for security reason

Use MotionEvent.FLAG_WINDOW_IS_PARTIALLY_OBSCURED to filter touch events
on permission dialog buttons when an overlay window overlaps with the
permission dialog window.

Bug: 902427
Change-Id: I6c2ad18e680c9e622ba7cd20aaf0c72d376ad99a
Reviewed-on: https://chromium-review.googlesource.com/c/1359818
Commit-Queue: Becky Zhou <huayinz@chromium.org>
Reviewed-by: Theresa <twellington@chromium.org>
Cr-Commit-Position: refs/heads/master@{#613776}
[modify] https://crrev.com/332bf6886f8cb1a826f3dcfe46804bd4528cd434/chrome/android/java/src/org/chromium/chrome/browser/permissions/PermissionDialogView.java


### hu...@chromium.org (2018-12-07)

Marking this as fixed. Please re-open if there is still issue.


### rs...@chromium.org (2018-12-11)

Should we request merge for #34 too?

### hu...@chromium.org (2018-12-11)

M71 is already on stable I believe, so it maybe too late for a merge.

### rs...@chromium.org (2018-12-11)

What about M72? The CL only made it into 73.

### hu...@chromium.org (2018-12-11)

Oh, sorry. I thought it was landed on 72. Yes, let's try 72:)

Requesting a merge to M72 for the patch at https://crbug.com/chromium/902427#c34 that mitigates a security issue on permission dialog.

### sh...@chromium.org (2018-12-12)

Your change meets the bar and is auto-approved for M72. Please go ahead and merge the CL to branch 3626 manually. Please contact milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-12-12)

(no need to re-open to track merging :-)

### bu...@chromium.org (2018-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dd87331e537ac1816db632e2d1f4081891dd96cd

commit dd87331e537ac1816db632e2d1f4081891dd96cd
Author: Becky Zhou <huayinz@chromium.org>
Date: Wed Dec 12 23:58:20 2018

Filter touch events for permission dialog for security reason

Use MotionEvent.FLAG_WINDOW_IS_PARTIALLY_OBSCURED to filter touch events
on permission dialog buttons when an overlay window overlaps with the
permission dialog window.

Bug: 902427
Change-Id: I6c2ad18e680c9e622ba7cd20aaf0c72d376ad99a
Reviewed-on: https://chromium-review.googlesource.com/c/1359818
Commit-Queue: Becky Zhou <huayinz@chromium.org>
Reviewed-by: Theresa <twellington@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#613776}(cherry picked from commit 332bf6886f8cb1a826f3dcfe46804bd4528cd434)
Reviewed-on: https://chromium-review.googlesource.com/c/1374949
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#316}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/dd87331e537ac1816db632e2d1f4081891dd96cd/chrome/android/java/src/org/chromium/chrome/browser/permissions/PermissionDialogView.java


### te...@chromium.org (2018-12-13)

@#41, that isn't what we've been told about merge request tracking.  We were told to keep it as Started until it was merged to all necessary branches.  Did that policy change recently?

### na...@google.com (2018-12-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-13)

Thanks for your report, the panel has decided to reward $2,000 :) 

### aw...@google.com (2018-12-14)

[Empty comment from Monorail migration]

### cr...@appspot.gserviceaccount.com (2018-12-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/dd87331e537ac1816db632e2d1f4081891dd96cd

Commit: dd87331e537ac1816db632e2d1f4081891dd96cd
Author: huayinz@chromium.org
Commiter: tedchoc@chromium.org
Date: 2018-12-12 23:58:20 +0000 UTC

Filter touch events for permission dialog for security reason

Use MotionEvent.FLAG_WINDOW_IS_PARTIALLY_OBSCURED to filter touch events
on permission dialog buttons when an overlay window overlaps with the
permission dialog window.

Bug: 902427
Change-Id: I6c2ad18e680c9e622ba7cd20aaf0c72d376ad99a
Reviewed-on: https://chromium-review.googlesource.com/c/1359818
Commit-Queue: Becky Zhou <huayinz@chromium.org>
Reviewed-by: Theresa <twellington@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#613776}(cherry picked from commit 332bf6886f8cb1a826f3dcfe46804bd4528cd434)
Reviewed-on: https://chromium-review.googlesource.com/c/1374949
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#316}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/902427?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Mobile>WebAPKs, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092965)*
