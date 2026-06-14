# getDisplayMedia() prompts from background tab, not obvious who's asking.

| Field | Value |
|-------|-------|
| **Issue ID** | [40093707](https://issues.chromium.org/issues/40093707) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>GetUserMedia, UI>Browser>Permissions>Prompts |
| **Platforms** | Mac |
| **Reporter** | wi...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2019-01-10 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3667.0 Safari/537.36

Steps to reproduce the problem:
1. Open https://jsfiddle.net/jib1/3Ls42nry/
2. Open a new tab, type "google.com" and hit ENTER.
3. Wait 10 seconds.

What is the expected behavior?
Nothing visibly happens, until I click on the jsfiddle tab to reveal a prompt there.

What went wrong?
A prompt pops up over my google.com page asking to share my screen.

In this context a user might assume google.com is asking, even though scrutiny of the dialog reveals it is "jsfiddle.net" asking for access. Not everyone reads dialogs carefully—a subpopulation might reflexively OK the dialog without reading it, trusting Google.

Any site on the drive-by-web can do this at any time, so this seems exploitable.

Users who fall for it end up sharing their entire screen including current tab content with the malicious background tab immediately, as well as all (browsing) activity from that point on, if left undiscovered.

In addition, once they revisit the malicious tab, they become vulnerable to active cross-origin attacks, perhaps targeted based on the browsing observed, as explained in https://blog.mozilla.org/webrtc/share-browser-windows-entire-screen-sites-trust/

Did this work before? Yes 72 (exploit is new with introduction of getDisplayMedia)

Chrome version: 73.0.3667.0  Channel: canary
OS Version: OS X 10.13.6
Flash Version: 

Expected behavior is based on Firefox Nightly.

## Attachments

- [Screenshot from 2019-01-11 14-11-46.png](attachments/Screenshot from 2019-01-11 14-11-46.png) (image/png, 10.6 KB)
- [Screen Shot 2021-09-17 at 14.52.35.png](attachments/Screen Shot 2021-09-17 at 14.52.35.png) (image/png, 107.6 KB)

## Timeline

### dt...@chromium.org (2019-01-10)

[Empty comment from Monorail migration]

[Monorail components: Blink>GetUserMedia]

### rs...@chromium.org (2019-01-11)

cthomp/estark: What do you think of this? I agree that it's fairly easy to miss the origin display in this dialog, but it is presented to the user.

[Monorail components: UI>Browser>Permissions>Prompts]

### ct...@chromium.org (2019-01-11)

+dominickn@ since he and I were driving the getDisplayMedia related reviews.

Also +niklase and emircan who are eng on the getDisplayMedia work.

### do...@chromium.org (2019-01-11)

Is there a reason for getDisplayMedia() to be callable from tabs that aren't focused and in the foreground? I'd strongly advise we apply that restriction (I'm unsure if it wasn't suggested or not implemented).

### es...@chromium.org (2019-01-11)

Changing to Security_Impact-Beta because the API only launched in M72 (currently in beta).

I think this is worth fixing (probably in the way that Dom suggests in #4). We should also check that other choosers (WebUSB, etc.) don't have the same problem.

### ni...@chromium.org (2019-01-11)

This hasn't been brought up before, and changing the behavior as suggest might cause some issues. For example, it's very common that a user would start loading go/present/myMeeting and then immediately flip over to Google Drive to open the document you want to present.

### ct...@chromium.org (2019-01-11)

+engedy@ for thinking about the broader choosers point brought up in #5 (we can maybe split that into a separate bug, but I agree that it would be good to think through and maybe manually check all chooser implementations).

### em...@chromium.org (2019-01-11)

This issue repros only on Mac. In all other platforms, it pops a View in the calling tab and if inactive it adds a blue dot, as seen in the screenshot. I am guessing it is because permission UI is a window on Mac whereas it is a View on every other platform. A very similar problem came up on https://crbug.com/chromium/919456. I am also guessing this works the same way for extensions based API, will verify that.

As far as I know, this divergence in Mac UI shouldn't exist there in the long term. I am going to add some Mac folks for their advice. If we can merge the Mac implementation into Views as well, we would solve all the problems now and possible happening in the future. I will test locally to see how bad Views look.

To address this issue, I can think of these as solutions:
- We don't allow calling getDisplayMedia() from an inactive tab at all. This needs to be added to spec as well. This won't change extensions based APIs behavior though.
- We fix the specific Mac Chrome code and do not allow popping windows from a call in an inactive tab. We keep the Mac specific UI.
- Deprecate the Mac specific UI. 

Last one is the ideal solution, but please let me know what are the blockers on it. 

### em...@chromium.org (2019-01-11)

[Empty comment from Monorail migration]

### qi...@chromium.org (2019-01-11)

I think the best way is to deprecate Mac specific UI, and switch to use chrome UI for picker.

But not sure how difficult it is.
I think with the rollout of material design UI project, we should be able to run the standard picker widget on Mac, Can anyone verify this?

### av...@chromium.org (2019-01-11)

The reason that the Cocoa version of the media picker is used is that the Views version of the picker uses the Views TableView, used only by this picker and by the Task Manager. The Mac still uses the Cocoa Task Manager, and so in the busy process of getting MacViews working, the Views TableView was never fixed up to look good on the Mac and thus the Cocoa version media picker was left as the one we use.

The way forward for this is to switch to the Views version of the media picker dialog and see how bad the TableView looks on the Mac. If we can clean it up to look decent, there should (fingers crossed) be no reason why we couldn't use the Views media picker.

### do...@chromium.org (2019-01-11)

#6: is that flow that common? Switching to a tab with the content you want to present *before* you've seen the prompt to explicit confirm that you want to screenshare? On Views platforms now, it seems to me like you need to switch back to the tab calling getDisplayMedia() anyway to get the confirmation prompt to start screensharing?

Given that M72 has already branched, switching to the Views picker for Mac is a task for M73 at the earliest. That will probably need to go through UI review, and won't feasibly fix the security regression in M72.

For now, I see the following options:

1. Restrict calling getDisplayMedia() to the active foreground tab and merge to M72 (it should be a feasible merge). I think it's a very sensible restriction that shouldn't negatively affect the getDisplayMedia() flow and could easily be added to the spec. Or this restriction can be lifted once Mac's chooser is fixed to only appear when the tab is focused.
2. Punt the launch of getDisplayMedia() from M72 until Mac's chooser is fixed.
3. Do (1) or (2), but for Mac only.

### ni...@chromium.org (2019-01-11)

Since this is a new API 1 should be acceptable initally, a limited functionality is better than none, and it's only needed on OSX.

### do...@chromium.org (2019-01-11)

#13: okay, let's go ahead with restricting getDisplayMedia() to the active foreground tab and merge that to M72 asap.

+cc desktop release manager abdulsyed FYI.

### em...@chromium.org (2019-01-12)

I made a fix so that Mac doesn't pop the picker until page is shown: https://chromium-review.googlesource.com/c/chromium/src/+/1407733 That would make it consistent with Views.

However, it sounds like restricting calling getDisplayMedia() to the active foreground tab is a better solution for the long term, in terms of security. I will work on it as well. dominickn@ WDYT?

### em...@chromium.org (2019-01-12)

Based on the offline feedback, I made a simpler CL that basically fails getDisplayMedia() call if the page is backgrounded on Mac. This will be a temporary case until Mac UI is deprecated and much safer to merge: https://chromium-review.googlesource.com/c/chromium/src/+/1407639

### do...@chromium.org (2019-01-12)

#16: thanks for moving on this so quickly! I agree your second CL looks safer to merge than your first one.

### sh...@chromium.org (2019-01-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4c176e5ffeebf5e1ca80243af53dc63a6218d15e

commit 4c176e5ffeebf5e1ca80243af53dc63a6218d15e
Author: Emircan Uysaler <emircan@chromium.org>
Date: Sun Jan 13 23:10:30 2019

Dont pop gDM() permission UI when page is hidden on Mac

See the bug for details. This is a temporary solution until Mac UI is consistent
with other OSs for getDisplayMedia().

Bug: 920733
Change-Id: I35eac31ed048620f3d7c1cf903827fede02aa0e5
Reviewed-on: https://chromium-review.googlesource.com/c/1407639
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Emircan Uysaler <emircan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#622360}
[modify] https://crrev.com/4c176e5ffeebf5e1ca80243af53dc63a6218d15e/chrome/browser/media/webrtc/display_media_access_handler.cc


### en...@chromium.org (2019-01-14)

[Empty comment from Monorail migration]

### em...@chromium.org (2019-01-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-01-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-15)

[Empty comment from Monorail migration]

### ab...@google.com (2019-01-15)

Thanks emircan@ - how safe is this merge? Are we sure it wont introduce any new regressions?

### em...@chromium.org (2019-01-15)

#26, it is safely disabling the feature for this edge case, also Mac only.

### ab...@google.com (2019-01-15)

branch:3626

### bu...@chromium.org (2019-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4d531e0602005ef0c3718a3a49f4fc674f3b2e77

commit 4d531e0602005ef0c3718a3a49f4fc674f3b2e77
Author: Emircan Uysaler <emircan@chromium.org>
Date: Tue Jan 15 17:56:27 2019

Dont pop gDM() permission UI when page is hidden on Mac

See the bug for details. This is a temporary solution until Mac UI is consistent
with other OSs for getDisplayMedia().

Bug: 920733
Change-Id: I35eac31ed048620f3d7c1cf903827fede02aa0e5
Reviewed-on: https://chromium-review.googlesource.com/c/1407639
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Emircan Uysaler <emircan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#622360}(cherry picked from commit 4c176e5ffeebf5e1ca80243af53dc63a6218d15e)
Reviewed-on: https://chromium-review.googlesource.com/c/1412892
Reviewed-by: Emircan Uysaler <emircan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#690}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/4d531e0602005ef0c3718a3a49f4fc674f3b2e77/chrome/browser/media/webrtc/display_media_access_handler.cc


### cr...@appspot.gserviceaccount.com (2019-01-15)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/4d531e0602005ef0c3718a3a49f4fc674f3b2e77

Commit: 4d531e0602005ef0c3718a3a49f4fc674f3b2e77
Author: emircan@chromium.org
Commiter: emircan@chromium.org
Date: 2019-01-15 17:56:27 +0000 UTC

Dont pop gDM() permission UI when page is hidden on Mac

See the bug for details. This is a temporary solution until Mac UI is consistent
with other OSs for getDisplayMedia().

Bug: 920733
Change-Id: I35eac31ed048620f3d7c1cf903827fede02aa0e5
Reviewed-on: https://chromium-review.googlesource.com/c/1407639
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Emircan Uysaler <emircan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#622360}(cherry picked from commit 4c176e5ffeebf5e1ca80243af53dc63a6218d15e)
Reviewed-on: https://chromium-review.googlesource.com/c/1412892
Reviewed-by: Emircan Uysaler <emircan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#690}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### na...@google.com (2019-01-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-17)

Congrats! The Panel has decided to reward $500 for this report. 

Since you are a new reporter how would you like to be credited in release notes? 



### aw...@google.com (2019-01-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2021-09-17)

IIANM, CL #1407639 only partially solved the issue. Namely, consider the case when the tab that calls getDisplayMedia() is not hidden, but its window is not the active window - either another Chrome window is active, or another native application altogether. Currently, the mostly-obscured-but-not-hidden Chrome window steals focus away from the foreground window, and that's a shame.

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### to...@chromium.org (2021-09-28)

Chatted to Elad, we agreed that the original concern here was addressed.
There's a separate question over whether the behaviour described in #35 where calling getDisplayMedia grabs focus is ok which we're filing a separate bug to track.

### el...@google.com (2021-09-28)

I believe it's definitely not OK, as this allows applications to become disruptive to the user. It bears mentioning that the user could blame the browser when this happens, and the user would be right. I've filed crbug.com/1253932 for this.

### is...@google.com (2021-09-28)

This issue was migrated from crbug.com/chromium/920733?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GetUserMedia, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093707)*
