# Security: Cast UI hides Full-screen warning

| Field | Value |
|-------|-------|
| **Issue ID** | [40090516](https://issues.chromium.org/issues/40090516) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Cast>UI, UI>Browser |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2018-02-15 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 66.0.3348.0  

Operating System: Mac

**REPRODUCTION CASE**  

Presentation API can show up over the fullscreen notification on (Unable to repro on Windows).

1. Set up a local webserver to host testcase.html
2. Click on 'click here please'
3. Observe

## Attachments

- [Screen Shot 2018-02-15 at 20.34.00.png](attachments/Screen Shot 2018-02-15 at 20.34.00.png) (image/png, 165.0 KB)
- [testcase.html](attachments/testcase.html) (text/plain, 3.7 KB)

## Timeline

### el...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-15)

This is yet another case where there's a spoof against the already-subtle "By the way, you're in full-screen now whether you like it or not" notice.

[Monorail components: Blink>Fullscreen Internals>Cast>UI]

### ea...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Fullscreen]

### oc...@chromium.org (2018-02-15)

mfoltz: could you please help take a look at this, or help get this assigned to the right person?

### mf...@chromium.org (2018-02-15)

I can't repro this on Linux.  It seems like a Mac browser UI issue - does it show the fullscreen notification in a different way?  Trent what do you think?

[Monorail components: UI>Browser]

### ch...@gmail.com (2018-02-15)

re C#5 - Cast UI overlay the fullscreen notification (This is similar to https://crbug.com/chromium/752003).

### oc...@chromium.org (2018-02-15)

+avi who owns a similar macOS-only bug (https://crbug.com/chromium/812060).

### av...@chromium.org (2018-02-15)

I solved this with JS dialogs and popups by dropping fullscreen in those cases. Do we want to make that a more general policy for all dialogs?

### sh...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### mf...@chromium.org (2018-02-16)

johnpallett@ may have some feedback about dropping out of fullscreen when activating the Media Router dialog.  It's a common use case to cast fullscreen video.

Is there a way we can tell when the notification is showing so we can drop out of fullscreen selectively?


### av...@chromium.org (2018-02-16)

There's no easy way of knowing if the notification is showing, plus that means uncertainty for the author of the page as to why showing the media router dialog sometimes kicks you out of fullscreen but sometimes it doesn't.

If you do that, do it all the time.

### ta...@chromium.org (2018-02-19)

I hit some dead-ends playing around with window levels and key-value observers. But I found a thing that seems to help: https://chromium-review.googlesource.com/c/chromium/src/+/923227

### ch...@gmail.com (2018-02-26)

[Comment Deleted]

### ch...@gmail.com (2018-02-26)

[Comment Deleted]

### ta...@chromium.org (2018-03-06)

I've merged https://crbug.com/chromium/813815 and https://crbug.com/chromium/817809 into this. https://crbug.com/chromium/812060 is something different - it doesn't actually show a fullscreen notification so there's nothing to obscure.

### ta...@chromium.org (2018-07-24)

per https://chromium-review.googlesource.com/c/chromium/src/+/923227#message-79972ff4162f078a3e21572af8e972292e9363b3 I think avi's looking at a cross-platform answer for this.

### ke...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3d41e77125f3de8d722b6d8303599abaf2a91667

commit 3d41e77125f3de8d722b6d8303599abaf2a91667
Author: Avi Drissman <avi@chromium.org>
Date: Mon Aug 27 21:18:08 2018

If a dialog is shown, drop fullscreen.

BUG=875066, 817809, 792876, 812769, 813815
TEST=included

Change-Id: Ic3d697fa3c4b01f5d7fea77391857177ada660db
Reviewed-on: https://chromium-review.googlesource.com/1185208
Reviewed-by: Sidney San Martín <sdy@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#586418}
[modify] https://crrev.com/3d41e77125f3de8d722b6d8303599abaf2a91667/chrome/browser/ui/browser.cc
[modify] https://crrev.com/3d41e77125f3de8d722b6d8303599abaf2a91667/chrome/browser/ui/browser_browsertest.cc
[modify] https://crrev.com/3d41e77125f3de8d722b6d8303599abaf2a91667/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/3d41e77125f3de8d722b6d8303599abaf2a91667/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/3d41e77125f3de8d722b6d8303599abaf2a91667/content/browser/web_contents/web_contents_impl_browsertest.cc


### av...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-11)

The VRP panel decided to award $500 for this report, thanks as ever!

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1c8c2146c2f99fb7eefb79b170e60f53700f7ab8

commit 1c8c2146c2f99fb7eefb79b170e60f53700f7ab8
Author: Yuri Wiitala <miu@chromium.org>
Date: Wed Sep 19 19:47:42 2018

Dialogs don't drop tab fullscreen when in FullscreenWithinTab mode.

Overrides the default behavior of dropping fullscreen when a tab modal
dialog is opened in the FullscreenWithinTab case. This is because, in
FWT mode, the browser window is in its normal layout (not fullscreened).

Bug: 883535,812769
Change-Id: I1c262954b962d508eb86ef9a8a312bec03ab2332
Reviewed-on: https://chromium-review.googlesource.com/1228976
Commit-Queue: Yuri Wiitala <miu@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#592522}
[modify] https://crrev.com/1c8c2146c2f99fb7eefb79b170e60f53700f7ab8/chrome/browser/ui/browser.cc
[modify] https://crrev.com/1c8c2146c2f99fb7eefb79b170e60f53700f7ab8/chrome/browser/ui/browser_browsertest.cc
[modify] https://crrev.com/1c8c2146c2f99fb7eefb79b170e60f53700f7ab8/chrome/browser/ui/exclusive_access/fullscreen_controller.h


### bu...@chromium.org (2018-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a438e211d0aa6f12eee274b22c4daef442a28eac

commit a438e211d0aa6f12eee274b22c4daef442a28eac
Author: Yuri Wiitala <miu@chromium.org>
Date: Fri Sep 21 20:35:42 2018

Dialogs don't drop tab fullscreen when in FullscreenWithinTab mode.

Overrides the default behavior of dropping fullscreen when a tab modal
dialog is opened in the FullscreenWithinTab case. This is because, in
FWT mode, the browser window is in its normal layout (not fullscreened).

Bug: 883535,812769
Change-Id: I1c262954b962d508eb86ef9a8a312bec03ab2332
Reviewed-on: https://chromium-review.googlesource.com/1228976
Commit-Queue: Yuri Wiitala <miu@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#592522}(cherry picked from commit 1c8c2146c2f99fb7eefb79b170e60f53700f7ab8)
Reviewed-on: https://chromium-review.googlesource.com/1239346
Reviewed-by: Yuri Wiitala <miu@chromium.org>
Cr-Commit-Position: refs/branch-heads/3538@{#565}
Cr-Branched-From: 79f7c91a2b2a2932cd447fa6f865cb6662fa8fa6-refs/heads/master@{#587811}
[modify] https://crrev.com/a438e211d0aa6f12eee274b22c4daef442a28eac/chrome/browser/ui/browser.cc
[modify] https://crrev.com/a438e211d0aa6f12eee274b22c4daef442a28eac/chrome/browser/ui/browser_browsertest.cc
[modify] https://crrev.com/a438e211d0aa6f12eee274b22c4daef442a28eac/chrome/browser/ui/exclusive_access/fullscreen_controller.h


### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/812769?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Cast>UI, UI>Browser]
[Monorail mergedwith: crbug.com/chromium/812770, crbug.com/chromium/813815, crbug.com/chromium/817809, crbug.com/chromium/871021]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090516)*
