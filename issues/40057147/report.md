# Security: Compromised renderer can set custom cursor up to 1024px over browser UI and other windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40057147](https://issues.chromium.org/issues/40057147) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input |
| **Platforms** | Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2021-09-02 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

A compromised renderer can render large custom cursors over browser UI and other windows.

Mitigations for these issues were implemented in the renderer only, therefore a compromised renderer can bypass them:  

<https://crbug.com/chromium/1099276>  

<https://crbug.com/chromium/880863>  

<https://crbug.com/chromium/640227>

Specifically, these mitigations can be bypassed:  

\* Limit custom cursor size to 128x128px:  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/input/event_handler.cc;l=594;drc=289a8d63ffde8000d54fc338d9de25a0f12cd5c5>

\* Fallback to default cursor if custom cursor (32x32px or larger) renders outside page:  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/input/event_handler.cc;l=619;drc=289a8d63ffde8000d54fc338d9de25a0f12cd5c5>

The only notable browser-side enforcement is a 1024px custom cursor size enforcement:  

<https://source.chromium.org/chromium/chromium/src/+/main:content/common/cursors/webcursor.cc;l=25;drc=8bcc3b52806612784b034560bfff2c8bd8576a7a>

Enforcing these mitigations in the browser side, especially the custom cursor size, would result in effective protections. This comment also points out the same thing:  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/input/event_handler.cc;l=603;drc=289a8d63ffde8000d54fc338d9de25a0f12cd5c5>

> // TODO(csharrison): Consider sending a fallback cursor in the IPC to the  
> 
> // browser process so we can do that calculation there instead, this would  
> 
> // ensure even a compromised renderer could not obscure browser UI with a  
> 
> // large cursor. [...]

The PoC provided is basic and only demonstrates a cursor rendering over browser UI. An improved PoC likely could overlay the omnibar and other security surfaces regardless of cursor position using the largest cursor possible (similar to <https://jameshfisher.github.io/cursory-hack/> but with more flexibility on cursor position due to larger cursor size limit).

Screen recording note: The cursor rendering lag is more apparent in the recording than when viewed directly on screen. It's also a local build, so it may have more lag than production builds.

**VERSION**  

Chrome Version:  

Should repro on Stable: 92.0.4515.159 (Official Build) (64-bit) (cohort: Stable)  

Verified repro on patched local build (~Aug 6th checkout): 94.0.4600.0 Revision e53e18d4b512d8ebaf1bcb591c3058af98d7ad18-refs/heads/master@{#909170}  

Operating System: Windows 10 OS Version 2009 (Build 19042.1110)

Nothing of relevance has changed since my ~Aug 6th checkout, so should still repro on ToT.

**REPRODUCTION CASE**  

Setup:

1. Apply renderer.patch and rebuild Chromium to simulate compromised renderer with disabled mitigations.

Basic PoC:  

Prerequsite: Compromised/patched renderer.

1. Navigate to <https://alesandroortiz.com/security/chromium/cursor-large.html>
2. Move cursor around page to observe behavior near window borders and near browser UI at top of window.

Observed: Large cursor is allowed to render over browser UI and outside browser window due to limited browser-side enforcement.  

Expected: Large cursor is unable to render over browser UI or outside browser window because of browser-side enforcement.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [cursor-large.html](attachments/cursor-large.html) (text/plain, 970 B)
- [cursor-images.zip](attachments/cursor-images.zip) (application/octet-stream, 28.7 KB)
- [renderer.patch](attachments/renderer.patch) (text/plain, 2.9 KB)
- [large-cursor.mp4](attachments/large-cursor.mp4) (video/mp4, 1.9 MB)

## Timeline

### al...@alesandroortiz.com (2021-09-02)

Repro steps addendum:
3. Append ?cursor=1024 for the largest cursor size (see page for other available sizes).

Note that 1200px size is a demonstration that cursor size above 1024px is prevented by browser-side enforcement.

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### ct...@chromium.org (2021-09-03)

Thanks for the detailed report (and for the video :D)! Setting this as Severity-Medium (as this can allow partial spoofing of trusted browser UI, but does not seem usable for complete control of the Omnibox that a Sev-High would entail), and FoundIn-86 (per blame on the linked code this dates to at least M-86, although that was the addition of more renderer-side checks so this likely goes back further).

Per the linked TODO, csharisson@ could you take this bug or find someone who could work on adding browser-side enforcement?

[Monorail components: Blink>Input]

### [Deleted User] (2021-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-17)

csharrison: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2021-09-22)

cthomp@ or current sheriff: Current owner is OOO until Sep 27, up to you if you want to reassign or wait. I'm okay waiting since it requires a compromised renderer, so it's not a casual attack.

### [Deleted User] (2021-10-01)

csharrison: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2021-11-11)

Friendly ping: Any updates on this issue? No notable crbug activity since report creation in early September and don't see an open CL.

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### cs...@chromium.org (2021-11-18)

Hey sorry for the delay on this. FWIW this is not a regression. Cursor size attacks have always been possible in the renderer and our only protection was always the max size enforced on the browser.

I am probably not the right owner to implement the browser-side protections. But it seems pretty reasonable to make the browser-side enforcement match the blink max size of 128 px. +msw and bsep, do you see this change regressing any other features? Would one of you be willing to take ownership of this bug?

### al...@alesandroortiz.com (2022-01-14)

Friendly ping: Any updates on this issue? Last comment was looking for a new owner.

### cs...@chromium.org (2022-01-20)

Moving myself to cc and adding a couple more folks that seem relevant.

### ms...@google.com (2022-01-20)

Sorry for the lack of followup; I'm not aware of any valid use cases for such large custom cursor sizes offhand.
I couldn't find any original reasoning for Blink's 128px maximum in particular; it may have been added here:
  https://src.chromium.org/viewvc/blink/trunk/Source/WebCore/page/EventHandler.cpp?annotate=136919&pathrev=136919
Still, making WebCursor's 1024px size from https://codereview.chromium.org/147193 match Blink's 128 from third_party/blink/renderer/core/input/event_handler.cc sgtm.
I'll see if I can write up a quick patch.

### ms...@google.com (2022-01-22)

Hmm, even with that patch applied, I can't repro on ToT 100.0.4845.0 (Developer Build) (64-bit).
The cursor appears to be smaller than 128px, regardless of what query I use on the page.
I'll look closer next week.

### hf...@igalia.com (2022-01-24)

msw: just in case, this bug doesn't affect Linux at the moment, since there's a bug in which the maximum cursor size is always 64px: https://crbug.com/1204322.

### ms...@google.com (2022-01-24)

Thanks for that info! afaict, linux-chromeos also doesn't repro (likely for the same reason), but neither does Windows over Chrome Remote Desktop from Linux.
I'll try building on my local Windows or Mac devices soon.

### hf...@igalia.com (2022-01-25)

linux-chromeos should reproduce unless the hardware doesn't support those cursors, which is unlikely. I'm not sure if CRD imposes any limitations to the cursor though.

### ms...@chromium.org (2022-01-25)

I was able to repro on a local Windows machine. I have a CL up for review at https://crrev.com/c/3413912

### gi...@appspot.gserviceaccount.com (2022-01-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/868b44dd8b4a1a3b9698f561ca17f75e4ec78dd2

commit 868b44dd8b4a1a3b9698f561ca17f75e4ec78dd2
Author: Mike Wasserman <msw@chromium.org>
Date: Fri Jan 28 01:49:41 2022

Make web cursor size limits match on browser and renderer

Use NSCursor arrowCursor on Mac for ui::mojom::CursorType::kNull.
(i.e. when WebCursor is constructed with an overly large custom cursor)

Bug: 1246188
Test: Automated unit tests and WPTs
Change-Id: I89627fa13cba96b755b8f80adbc91cfc865b6b1b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413912
Reviewed-by: Henrique Ferreiro <hferreiro@igalia.com>
Reviewed-by: Charlie Harrison <csharrison@chromium.org>
Commit-Queue: Mike Wasserman <msw@chromium.org>
Auto-Submit: Mike Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#964378}

[modify] https://crrev.com/868b44dd8b4a1a3b9698f561ca17f75e4ec78dd2/content/common/cursors/webcursor_mac.mm
[modify] https://crrev.com/868b44dd8b4a1a3b9698f561ca17f75e4ec78dd2/content/common/cursors/webcursor.cc
[modify] https://crrev.com/868b44dd8b4a1a3b9698f561ca17f75e4ec78dd2/content/common/cursors/webcursor_unittest.cc


### ms...@chromium.org (2022-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-01-30)

Thanks for fixing, msw!

### [Deleted User] (2022-01-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/38a8343085e53889eba48fcff78a6c2295927333

commit 38a8343085e53889eba48fcff78a6c2295927333
Author: Mike Wasserman <msw@chromium.org>
Date: Tue Feb 01 01:47:47 2022

Revert "Make web cursor size limits match on browser and renderer"

This reverts commit 868b44dd8b4a1a3b9698f561ca17f75e4ec78dd2.

Reason for revert: https://crbug.com/1292426

Original change's description:
> Make web cursor size limits match on browser and renderer
>
> Use NSCursor arrowCursor on Mac for ui::mojom::CursorType::kNull.
> (i.e. when WebCursor is constructed with an overly large custom cursor)
>
> Bug: 1246188
> Test: Automated unit tests and WPTs
> Change-Id: I89627fa13cba96b755b8f80adbc91cfc865b6b1b
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413912
> Reviewed-by: Henrique Ferreiro <hferreiro@igalia.com>
> Reviewed-by: Charlie Harrison <csharrison@chromium.org>
> Commit-Queue: Mike Wasserman <msw@chromium.org>
> Auto-Submit: Mike Wasserman <msw@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#964378}

Bug: 1246188
Change-Id: Id7b3b88e65c012993537ce96c2b5064b7b76646e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3428347
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Mike Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#965475}

[modify] https://crrev.com/38a8343085e53889eba48fcff78a6c2295927333/content/common/cursors/webcursor_mac.mm
[modify] https://crrev.com/38a8343085e53889eba48fcff78a6c2295927333/content/common/cursors/webcursor.cc
[modify] https://crrev.com/38a8343085e53889eba48fcff78a6c2295927333/content/common/cursors/webcursor_unittest.cc


### hf...@igalia.com (2022-02-01)

msw: regarding https://crbug.com/1292426, I think the problem is https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/devtools_eye_dropper.cc;l=196;drc=2759dc1223b322b24ff64d6c96ff3822e0e8851e, where the color picker cursor size is 150 pixels.

### ms...@chromium.org (2022-02-01)

Thanks for the quick diagnosis there, hferreiro! +CC FYI caseq@chromium.org
Simply increasing WebCursor's limit 128->150px keeps DevToolsEyeDropper working.
That seems like an easy fix that still avoids significant abuse by compromised renders.
Please raise any objections to that approach here or on https://crrev.com/c/3428624

### gi...@appspot.gserviceaccount.com (2022-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1665a1d16d46fc39da7bf220a85c4ee38cd99d25

commit 1665a1d16d46fc39da7bf220a85c4ee38cd99d25
Author: msw@chromium.org <msw@chromium.org>
Date: Tue Feb 01 21:16:10 2022

Reland "Make web cursor size limits match on browser and renderer"

This reverts commit 38a8343085e53889eba48fcff78a6c2295927333.

Reason for revert: Fix without regressing https://crbug.com/1292426
(Increased WebCursor limit 128->150px to support DevToolsEyeDropper)

Original change's description:
> Revert "Make web cursor size limits match on browser and renderer"
>
> This reverts commit 868b44dd8b4a1a3b9698f561ca17f75e4ec78dd2.
>
> Reason for revert: https://crbug.com/1292426
>
> Original change's description:
> > Make web cursor size limits match on browser and renderer
> >
> > Use NSCursor arrowCursor on Mac for ui::mojom::CursorType::kNull.
> > (i.e. when WebCursor is constructed with an overly large custom cursor)
> >
> > Bug: 1246188
> > Test: Automated unit tests and WPTs
> > Change-Id: I89627fa13cba96b755b8f80adbc91cfc865b6b1b
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413912
> > Reviewed-by: Henrique Ferreiro <hferreiro@igalia.com>
> > Reviewed-by: Charlie Harrison <csharrison@chromium.org>
> > Commit-Queue: Mike Wasserman <msw@chromium.org>
> > Auto-Submit: Mike Wasserman <msw@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#964378}
>
> Bug: 1246188
> Change-Id: Id7b3b88e65c012993537ce96c2b5064b7b76646e
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3428347
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Commit-Queue: Mike Wasserman <msw@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#965475}

Fixed: 1246188
Bug: 1292426
Change-Id: I5a490603c3e21e17f3136a3d792a18429eb3f633
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3428624
Auto-Submit: Mike Wasserman <msw@chromium.org>
Reviewed-by: Charlie Harrison <csharrison@chromium.org>
Commit-Queue: Mike Wasserman <msw@chromium.org>
Reviewed-by: Henrique Ferreiro <hferreiro@igalia.com>
Cr-Commit-Position: refs/heads/main@{#965857}

[modify] https://crrev.com/1665a1d16d46fc39da7bf220a85c4ee38cd99d25/content/common/cursors/webcursor_mac.mm
[modify] https://crrev.com/1665a1d16d46fc39da7bf220a85c4ee38cd99d25/content/common/cursors/webcursor.cc
[modify] https://crrev.com/1665a1d16d46fc39da7bf220a85c4ee38cd99d25/content/common/cursors/webcursor_unittest.cc


### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations on another one! The VRP Panel has decided to award you $2,000 for this report (which I affectionately refer to as "Mega Cursor"). Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-19)

Not requesting merge to dev (M100) because latest trunk commit (964378) appears to be prior to dev branch point (972766). If this is incorrect, please replace the Merge-NA-100 label with Merge-Request-100. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2022-02-22)

Thanks for the reward and for giving the report a great nickname! :)

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1246188?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057147)*
