# Security: Chrome on Android Keyboard Able to Overlap Fullscreen Notification Toast

| Field | Value |
|-------|-------|
| **Issue ID** | [40061657](https://issues.chromium.org/issues/40061657) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2022-11-08 |
| **Bounty** | $7,500.00 |

## Description

On Chrome on Android after patch [crrev.com/c/3990410](https://crrev.com/c/3990410) the fullscreen notification toast is now displayed in bottom instead of top position, if shown in the bottom position I found that Android keyboard able to overlap fullscreen notification toast, so user will not see the fullscreen toast.

**VERSION**

- Chrome Dev 109.0.5394.4 on Android 13; Android Emulator; Pixel\_2\_API\_33
- Chrome Dev 109.0.5394.3 on Android 11; Mi 9T

**REPRODUCTION CASE**

1. Visit attached testcase-spoof.html
2. Tap "requestFullscreen" button
3. Fullscreen notification toast overlapped by Android Keyboard

**CREDIT INFORMATION**  

Reporter: Irvan Kurniawan (sourc7)

## Attachments

- [testcase-spoof.html](attachments/testcase-spoof.html) (text/plain, 59.1 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [testcase-spoof-gsignin.html](attachments/testcase-spoof-gsignin.html) (text/plain, 863.8 KB)
- [Chrome on Android - Keyboard Overlap Fullscreen Toast + Impersonate Google Sign In Page.mp4](attachments/Chrome on Android - Keyboard Overlap Fullscreen Toast + Impersonate Google Sign In Page.mp4) (video/mp4, 2.6 MB)
- [fs-k01.png](attachments/fs-k01.png) (image/png, 308.2 KB)
- [fs-k02.png](attachments/fs-k02.png) (image/png, 313.1 KB)
- [fs-k03.png](attachments/fs-k03.png) (image/png, 319.3 KB)
- [1382484-fs01.png](attachments/1382484-fs01.png) (image/png, 123.6 KB)

## Timeline

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### su...@gmail.com (2022-11-08)

PoC video captured on Chrome Dev 109.0.5394.3 on Android 11; Mi 9T


### wf...@chromium.org (2022-11-08)

Thank you for your report. I'm assigning this to the developer who changed this behavior to take a look.

[Monorail components: Blink>Fullscreen UI>Browser>FullScreen]

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### su...@gmail.com (2022-11-09)

On Firefox for Android, the full screen notification will be pushed to the top of android keyboard, so user able to see the fullscreen notification.

### su...@gmail.com (2022-11-09)

Here the updated testcase that impersonate Google sign in page

### [Deleted User] (2022-11-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2022-11-09)

Thanks for reporting. This is a side effect of moving the fullscreen toast to the bottom https://crbug.com/chromium/1356987

cc'ing more people for inputs. Will see if I can suppress the OSK when entering fullscreen, but there might be a hack to work around it again.

### tw...@chromium.org (2022-11-09)

> Will see if I can suppress the OSK when entering fullscreen, but there might be a hack to work around it again.

I think dismissing the keyboard / temporarily suppressing is reasonable, although not sure if there are valid cases for this.


Jinsuk, given the number of security issues introduced with switching to a custom View instead of a system Toast, I wonder if need to explore different solutions. For example, we'd talked about using OS level Toast but adding rate limiting in Chrome to ensure that e.g. copy toasts didn't DoS fullscreen toasts.

### ji...@chromium.org (2022-11-09)

Thanks for the suggestion. From https://bugs.chromium.org/p/chromium/issues/detail?id=1311683, I think rate-limiting is required not only among OS toasts but also against Messages or any other modal/modeless UI provide by Chrome. Will do some research for different approaches. 

### tw...@chromium.org (2022-11-10)

Thanks Jinsuk,

In the interim, if there's not a quick solution for this keyboard issue we might want to revert the change in  https://crbug.com/chromium/1356987 depending on which scenario is easier to reproduce / has higher security impact. 

### tw...@chromium.org (2022-11-11)

Jinsuk, another idea here  -- can we get the height of the keyboard and position the toast above the keyboard? 

We should also spend some time brainstorming other Chrome/OS UI that might conflict with the in-product bubble we're using currently.

### ji...@chromium.org (2022-11-11)

> Jinsuk, another idea here  -- can we get the height of the keyboard and position the toast above the keyboard? 

I have a CL WIP that exactly does that. Will tidy it up and send it up for review.

### tw...@chromium.org (2022-11-11)

Thanks Jinsuk!

### ji...@chromium.org (2022-11-11)

https://chromium-review.googlesource.com/c/chromium/src/+/4021894 up for review. Attached screenshots show how it moves up the toast above the keyboard (1) and moves it back down once the keyboard is gone (2)

### tw...@chromium.org (2022-11-11)

one other edge case to check jinsuk is overlap w/ our autofill keyboard accessory to make sure z-index for the fullscreen notification is higher

> fs-k02.png

Can we position above the OS nav bar? 

### tw...@chromium.org (2022-11-11)

[Empty comment from Monorail migration]

### ji...@chromium.org (2022-11-11)

> Can we position above the OS nav bar?

Just to clarify:

1. We care about the nav bar when there's no keyboard only, right? i.e. not when the keyboard is present (attached screenshot fs-k03.png). 
2. Do we reposition the toast if the nav bar disappears? It is a transient one that briefly comes and goes. In fact I'm not sure if it is possible to know when it appears and disappears. 


### tw...@chromium.org (2022-11-11)

 1) fs-k03.png looks good to me.  More it just looks like a bug for our toast to be beneath the nav bar buttons as in  fs-k02.png

 2) I don't think we have to reposition in that case... if it's easier (not sure it is since the WindowInset APIs have some inconsistencies across OS versions / OEMs, will fwd you a recent discussion on this) we could always position above nav bar height.

### ji...@chromium.org (2022-11-11)

2-1 Do we reposition the toast if the nav bar appears, or do you mean that we position the toast further up in the first place to avoid overlapping?

### tw...@chromium.org (2022-11-11)

> do you mean that we position the toast further up in the first place to avoid overlapping?

I think this is easier / less movement if we can 

but if not, then yes, would reposition the toast if the nav bar appears so they don't overlap

### ji...@chromium.org (2022-11-11)

Ah didn't see https://crbug.com/chromium/1382484#c20 before posting another one https://crbug.com/chromium/1382484#c21. Sounds like you meant to see the toast where it would never overlap with the nav bar in the first place.

### tw...@chromium.org (2022-11-11)

Yes, exactly

### tw...@chromium.org (2022-11-14)

Jinsuk, on the in-flight CL we're using 

https://docs.google.com/spreadsheets/d/1zr9n9H8rclE-PJf46fLiq9W4yUmJQbE0-2DNaLGK0x0/edit#gid=1261706443

getInsets(WindowInsets.Type.navigationBars()).bottom;


It'd be good to confirm what that returns on API 32 / Tangor with task bar since those were flagged in this spreadsheet: https://docs.google.com/spreadsheets/d/1zr9n9H8rclE-PJf46fLiq9W4yUmJQbE0-2DNaLGK0x0/edit#gid=1261706443


### ji...@chromium.org (2022-11-14)

Yes I verified that it works on both cases as expected.

### tw...@chromium.org (2022-11-14)

Great, thanks!

### gi...@appspot.gserviceaccount.com (2022-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/69def735e986429cc3c78911d8ca59a38c24c20f

commit 69def735e986429cc3c78911d8ca59a38c24c20f
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Wed Nov 16 23:31:42 2022

Android: Repositions fullscreen toast upon window layout change

Repositions the fullscreen notification toast when window layout
changes. This keeps the toast from being obscured by decreased window
height.

Bug: 1382484
Change-Id: Ib24e0df6d5c9dd024b50203d1f35330411e5c887
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4021894
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1072510}

[modify] https://crrev.com/69def735e986429cc3c78911d8ca59a38c24c20f/components/browser_ui/util/android/BUILD.gn
[add] https://crrev.com/69def735e986429cc3c78911d8ca59a38c24c20f/components/browser_ui/util/android/java/src/org/chromium/components/browser_ui/util/DimensionCompat.java
[modify] https://crrev.com/69def735e986429cc3c78911d8ca59a38c24c20f/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/69def735e986429cc3c78911d8ca59a38c24c20f/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### ji...@chromium.org (2022-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-17)

Requesting merge to dev M109 because latest trunk commit (1072510) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-17)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b3ded7622dce0b39d986dd5aded96032e1c3495

commit 5b3ded7622dce0b39d986dd5aded96032e1c3495
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Fri Nov 18 16:26:39 2022

Android: Repositions fullscreen toast upon window layout change

Repositions the fullscreen notification toast when window layout
changes. This keeps the toast from being obscured by decreased window
height.

(cherry picked from commit 69def735e986429cc3c78911d8ca59a38c24c20f)

Bug: 1382484
Change-Id: Ib24e0df6d5c9dd024b50203d1f35330411e5c887
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4021894
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1072510}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4035653
Cr-Commit-Position: refs/branch-heads/5414@{#134}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/5b3ded7622dce0b39d986dd5aded96032e1c3495/components/browser_ui/util/android/BUILD.gn
[add] https://crrev.com/5b3ded7622dce0b39d986dd5aded96032e1c3495/components/browser_ui/util/android/java/src/org/chromium/components/browser_ui/util/DimensionCompat.java
[modify] https://crrev.com/5b3ded7622dce0b39d986dd5aded96032e1c3495/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/5b3ded7622dce0b39d986dd5aded96032e1c3495/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### tw...@chromium.org (2022-11-21)

[Empty comment from Monorail migration]

### kg...@google.com (2022-11-21)

Opening this back up as with this change another issue has been introduced where the Toast is only partially visible at the bottom of the screen when going fullscreen. Screenshot: https://drive.google.com/file/d/19tsotjVIS3zTu99sPFK7upJEyAvOaPKw/view?usp=sharing&resourcekey=0-ANpUv_qO9xhcO3xmczL4-A

Was able to repro the issue both on 110.0.5424.0 and 109.0.5414.12

Jinsuk, please look at reverting/fixing this once you are back next week.



### kg...@google.com (2022-11-21)

[Empty comment from Monorail migration]

### ji...@chromium.org (2022-11-28)

What was the device/OS you could repro the issue on? It works fine on Pixel/PQ1A.191105, XL/RP1A.190417, 4XL/SQ3A.220705 with Canary 110.0.5445.0

### kg...@google.com (2022-11-28)

I can repo on Pixel 6A build UP1A.2208.12.001838289 with 110.0.5424.0 and 109.0.5414.12

### ji...@chromium.org (2022-11-28)

Tested it on a few more OS'es (TQ1A.230105, SG/Android 8.0) and the toast all works fine one them. I suspect the observation  https://crbug.com/chromium/1382484#c36 could be related to a temporary glitch in U still in development. 

### ji...@chromium.org (2022-11-29)

The issue comes from the non-zero offset of Window. On most devices it is zero but for devices like Pixel 6A (or 7), it is a positive value that takes the front camera y position into account. The right way to get the bottom margin[1] is to use |bounds.height()|, not |bounds.bottom|.  

        public void onGlobalLayout() {
            if (mContentViewInFullscreen == null || mNotificationToast == null) return;
            Rect bounds = new Rect();
            mContentViewInFullscreen.getWindowVisibleDisplayFrame(bounds);
            var lp = (ViewGroup.MarginLayoutParams) mNotificationToast.getLayoutParams();
            int bottomMargin = mContentViewInFullscreen.getHeight() - bounds.bottom;  <----------------
            // If positioned at the bottom of the display, shift it up to avoid overlapping
            // with the bottom nav bar when it appears by user gestures.
            if (bottomMargin == 0) bottomMargin = mNavbarHeight;
            lp.setMargins(0, 0, 0, bottomMargin);
            mNotificationToast.requestLayout();
        }

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;l=159

### gi...@appspot.gserviceaccount.com (2022-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5df9af8ed35926e9c2682d30e15b47cc901d9f06

commit 5df9af8ed35926e9c2682d30e15b47cc901d9f06
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Wed Nov 30 15:43:34 2022

Set the fullscreen toast position right

On some device where the Window has non-zero top offset, the
fullscreen toast could be hidden partially. This CL fixes that by
obtaining the right bottom margin to secure for the toast.

Bug: 1382484
Change-Id: I173aabf0b496929efad0f76c140ab5ffd37ac55e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4063099
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1077492}

[modify] https://crrev.com/5df9af8ed35926e9c2682d30e15b47cc901d9f06/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java


### ji...@chromium.org (2022-11-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations, Irvan! The VRP Panel has decided to award you $7500 for this report. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1382484?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

### ji...@chromium.org (2024-11-19)

b/40068581 -> jinsukkim@google.com

### bu...@google.com (2024-11-19)

You can't assign/cc Bugjuggler on closed bugs. You can make Bugjuggler the verifier though (go/bugjuggler#verifier).

### ji...@google.com (2024-11-19)

b/40068581 -> jinsukkim@google.com

### bu...@google.com (2024-11-19)

You can't assign/cc Bugjuggler on closed bugs. You can make Bugjuggler the verifier though (go/bugjuggler#verifier).

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061657)*
