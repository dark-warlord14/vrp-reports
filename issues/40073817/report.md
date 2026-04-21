# Security: Download started notification can suppressed "exit full screen"  notification lead to spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40073817](https://issues.chromium.org/issues/40073817) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, UI>Browser>Downloads, UI>Browser>FullScreen |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2023-09-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

This vulnerability is an address bar spoofing vulnerability in fullscreen mode. When downloading file in full screen mode at the same time a "Press esc to exit full screen and see download" notification will appear. but with several downloads it can suppress "Press esc to exit full screen and see download" and only "Download started, to see it press esc" will appear.

Reproduce the POC may be unstable. You'll have to try a few times before the "Download started, to see it press esc" notification will appear, but it can still be spoofed.

**VERSION**  

Chrome Version 119.0.6034.6 (Official Build) dev (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. open downloadspoof5.html
2. click "click here" button two times or more until enter fullscreen mode and show "Download started, to see it press esc". if cannot show "Download started, to see it press esc", you can exit fullscreen mode and repeat step 1 until show "Download started, to see it press esc".

I attached POC video

**CREDIT INFORMATION**

Reporter credit: Hafiizh (<https://www.linkedin.com/in/hafiizh-7aa6bb31/>)

## Attachments

- [bandicam 2023-09-30 10-11-09-298.mp4](attachments/bandicam 2023-09-30 10-11-09-298.mp4) (video/mp4, 7.5 MB)
- [downloadspoof5.html](attachments/downloadspoof5.html) (text/plain, 89.1 KB)
- [bandicam 2023-09-30 06-37-53-220.mp4](attachments/bandicam 2023-09-30 06-37-53-220.mp4) (video/mp4, 7.7 MB)
- [bandicam 2023-10-05 02-49-53-948.mp4](attachments/bandicam 2023-10-05 02-49-53-948.mp4) (video/mp4, 12.3 MB)

## Timeline

### [Deleted User] (2023-09-30)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-10-01)

Thank you for the report!

@chlily@chromium.org @shrike@chromium.org would you be able to help triage this issue? I'm not 100% sure if this is under Fullscreen or Downloads. Thanks!

[Monorail components: Blink>Fullscreen UI>Browser>Downloads UI>Browser>FullScreen]

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-01)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@chromium.org (2023-10-02)

Hmm I think this is WAI. At the very least I'm not sure it's a security issue?

AFAIK there's a delay between successive shows of the fulscreen banner.[1] There is no such delay for the download banner, which is why you see the download banner alone (without the reference to fullscreen).

Perhaps the delay timer should be reset between separate instances of entering fullscreen? I am not sure who the best person to own this would be. shrike@: You seem more familiar with the fullscreen code; mind triaging?

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/exclusive_access/exclusive_access_bubble.h;l=28-30;drc=325222d306afdafe6eb38858531b2a30874dc3b0

### ch...@chromium.org (2023-10-02)

To elaborate on "At the very least I'm not sure it's a security issue?" It doesn't seem like there's that much potential for abuse because the user already saw the fullscreen banner recently.

### sa...@gmail.com (2023-10-02)

I tried again and even at the beginning the fullscreen banner didn't appear. and I didn't see it at the beginning.

### ch...@chromium.org (2023-10-02)

The behavior seems inconsistent which suggests some sort of race condition

I suspect it's a race with whether the banner is already visible from previous shows. [1] seems to be the relevant code as notify_overridden_ controls which text is shown.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/exclusive_access_bubble_views.cc;l=148-149;drc=641d3b47c0dcd3fc1231ebf0b31722e0a9299b1d

### ch...@chromium.org (2023-10-02)

I am not able to reproduce this on my Windows or Linux machine. It might have to do with downloading a large data URL which I think uses some CPU and may delay the animation.

I think I know what's causing this, though, so I can take a stab at this bug.

### ch...@chromium.org (2023-10-02)

[Empty comment from Monorail migration]

### ch...@chromium.org (2023-10-02)

cc dalecurtis: fyi because I heard your team was taking over fullscreen.

### da...@chromium.org (2023-10-02)

=>mfoltz who's team ended up picking it up.

### mf...@chromium.org (2023-10-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/661124745632183fdfc8633ab55da198ceef6254

commit 661124745632183fdfc8633ab55da198ceef6254
Author: Lily Chen <chlily@chromium.org>
Date: Tue Oct 03 14:46:38 2023

[ExclusiveAccessBubble] notify_overriden_: check if animation is showing

This checks if the animation is showing, not just whether the bubble is
visible. This is a speculative fix for a potential race condition in
setting notify_overridden_.

Bug: 1488157
Change-Id: I3e00d020458ccae4b3567ac0665ef48f4b5ce918
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4903710
Commit-Queue: Lily Chen <chlily@chromium.org>
Reviewed-by: Caroline Rising <corising@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1204642}

[modify] https://crrev.com/661124745632183fdfc8633ab55da198ceef6254/chrome/browser/ui/views/exclusive_access_bubble_views.cc


### sa...@gmail.com (2023-10-04)

Does this fix include fullscreen notifications?

### pb...@google.com (2023-10-04)

[BULK EDIT] M119 Stable RC cut date is just two weeks away i.e., Oct 24th, Please evaluate the releaseblocker and get the needed fix asap. Please consider this as a high priority issue as the Stable promotion is fast approaching.

### ch...@chromium.org (2023-10-04)

> Does this fix include fullscreen notifications?
Yes, though it's a speculative fix as I have been unable to repro it myself.

Canary version 120.0.6046.0 should have this change. Would you mind testing it again?

### sa...@gmail.com (2023-10-04)

I've tried it and it can't be reproduced in canary.

### ch...@chromium.org (2023-10-04)

Thanks for confirming!

### ch...@chromium.org (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

Merge approved: your change passed merge requirements and is auto-approved for M119. Please go ahead and merge the CL to branch 6045 (refs/branch-heads/6045) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d5a6c9d0aa4a909b471c13eaf8a837b3964d77c

commit 6d5a6c9d0aa4a909b471c13eaf8a837b3964d77c
Author: Lily Chen <chlily@chromium.org>
Date: Fri Oct 06 17:06:42 2023

[M119][ExclusiveAccessBubble] notify_overriden_: check if animation is showing

This checks if the animation is showing, not just whether the bubble is
visible. This is a speculative fix for a potential race condition in
setting notify_overridden_.

(cherry picked from commit 661124745632183fdfc8633ab55da198ceef6254)

Bug: 1488157
Change-Id: I3e00d020458ccae4b3567ac0665ef48f4b5ce918
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4903710
Commit-Queue: Lily Chen <chlily@chromium.org>
Reviewed-by: Caroline Rising <corising@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1204642}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4916491
Cr-Commit-Position: refs/branch-heads/6045@{#128}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/6d5a6c9d0aa4a909b471c13eaf8a837b3964d77c/chrome/browser/ui/views/exclusive_access_bubble_views.cc


### sa...@gmail.com (2023-10-13)

Hello any updates? 

### sa...@gmail.com (2023-10-16)

is this eligible for bounty ? because the bot not set the reward-topanel label

### am...@chromium.org (2023-10-16)

This will be evaluated by the VRP panel. There was a bug in the bot that resulted in the label not being added here. 

### sa...@gmail.com (2023-10-16)

thank you amy...

### am...@google.com (2023-10-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-26)

Congratulations Hafiizh! The Chrome VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us. 

### sa...@gmail.com (2023-10-26)

thank you amy

### am...@chromium.org (2023-10-26)

you're welcome :) 

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1488157?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, UI>Browser>Downloads, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073817)*
