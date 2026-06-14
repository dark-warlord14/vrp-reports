# UI/URL Spoofing by opening popups and putting the background page into fullscreen

| Field | Value |
|-------|-------|
| **Issue ID** | [40091613](https://issues.chromium.org/issues/40091613) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, UI>Browser>FullScreen |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | mu...@chromium.org |
| **Created** | 2018-06-10 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

By opening a popup, putting the background page into fullscreen and opening a subsequent popup over the fullscreen message it's possible to perform UI/URL spoofing.

The exploit works as follows:

1. User accesses attacker's website and clicks on a link.
2. A popup will open asking the user to click on a button.
3. When the user clicks on the button, the script calls window.opener.document.documentElement.webkitRequestFullscreen(), which puts the window in the background into fullscreen. At the same time, another popup is opened and placed directly above the old one (this conceals the message saying the user entered fullscreen).
4. In parallel with step 3, the background page is spoofed (it starts displaying an image of a fake omnibox and a fake Google page.
5. The hidden fullscreen message will disappear after around 5 seconds, and later, when the user eventually closes the popup, the message will be long gone and the page will remain spoofed.

This allows UI/URL spoofing very similar to <https://crbug.com/chromium/550017>. Also, while the popup is open, the taskbar on Windows remains visible (even though the background page is in fullscreen), making the attacker's life easier since he will only need to spoof the omnibox (similar effect to <https://crbug.com/chromium/677716>). This behavior isn't visible on the video because for some reason my screen recorder isn't able to capture that, but I have also attached a picture of it.

**VERSION**  

Versão 67.0.3396.79 (Official Build) Stable (64-bits)  

Versão 69.0.3453.0 (Official Build) Canary (64-bits)

**REPRODUCTION CASE**

1. Open <https://lbherrera.github.io/lab/fullscreen-spoof/index.html>
2. Click on the link.
3. After the popup shows up, click on the "Confirm" button.
4. You should now be seeing a popup faking the Google signin page, as well as a spoofed omnibox and Google page on the background window. If you wait 5 seconds to close this popup you also won't be able to see the message that you entered fullscreen mode.

## Attachments

- [spoof.mp4](attachments/spoof.mp4) (video/mp4, 477.6 KB)
- [taskbar.png](attachments/taskbar.png) (image/png, 219.1 KB)
- [sign.png](attachments/sign.png) (image/png, 63.3 KB)
- [spoof.png](attachments/spoof.png) (image/png, 233.6 KB)
- [index.html](attachments/index.html) (text/plain, 602 B)
- [opener.html](attachments/opener.html) (text/plain, 1.8 KB)

## Timeline

### pa...@chromium.org (2018-06-11)

meacer: Could you please take a look, or pass it to someone? Thanks!

Confirmed on Chrome OS; I'd imagine it works at least on the other desktop platforms but I'll have to check on Monday.

[Monorail components: Blink>Fullscreen UI>Browser>FullScreen]

### es...@chromium.org (2018-06-13)

So the problem here is that a popup can cover the fullscreen bubble? Bah. Avi, I suppose that wouldn't be covered by your show dialog -> lose fullscreen proposal, right? (That's limited to browser native dialogs?)

### av...@chromium.org (2018-06-13)

No, that proposal is about dialogs, not popups.

We are already pretty aggressive about popups. If a page opens a popup it loses fullscreen, and if a page focuses a popup it loses fullscreen. Here, the page that is opening a popup is not the fullscreen page (though it's related to that page).

At what point do we say that *any* opening of *any* popup kicks every page out of fullscreen? I didn't want to do that, as that's mean to the poor victim fullscreen users who genuinely are unrelated to the pages that are showing popups, but at some point I fear we'll have to throw up our hands and give up.

### wf...@chromium.org (2018-06-14)

Here is the source.

### wf...@chromium.org (2018-06-14)

This seems medium to me: the spoof is pretty convincing. I think we should probably make popups cause loss of fullscreen. Who can handle this?

### av...@chromium.org (2018-06-14)

Make any page's popup cause every other page to lose fullscreen?

I'm OOO until the end of next week but I've done this kind of work before. If you file an Intent and get consensus, I'd be happy to do the implementation.

### sh...@chromium.org (2018-06-24)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2018-06-29)

Looking at this spoof again, it strikes me as odd that the same user gesture can cause the background page to go into fullscreen *and* a new popup to open at the same time. Anyone know if that is WAI? Seems like you should need two user gestures to do that.

### he...@gmail.com (2018-06-29)

estark@: There has been some discussion in https://crbug.com/chromium/852645 and https://crbug.com/chromium/729694.

### sh...@chromium.org (2018-07-08)

meacer: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-07-10)

Is there a good reason to allow a background page go fullscreen? Can we block that? (via an blink I2D probably)

### mm...@chromium.org (2018-08-07)

Ping from the security sheriff :)



### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-05)

avi: Could you remind me whether anything has changed in the fullscreen world? Are your comments #3 and #6 still valid?

### me...@chromium.org (2018-10-05)

Also I'm probably not a good owner for this (I already have a bunch of medium severity bugs assigned). Is anyone else from Enamel interested in moving this forward?

### av...@chromium.org (2018-10-05)

Nothing has changed from #3 and #6. If a page shows a popup it loses fullscreen but it's not "any popup causes all pages in fullscreen to lose it".

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-14)

(bulk edit: herrerahlb@gmail.com is the new email address for luan.herrera@hotmail.com)

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### ea...@chromium.org (2019-02-11)

[Empty comment from Monorail migration]

### dt...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-02-21)

This is a duplicate bug.

This no longer reproduces in M72 because of UAv2, which consumes user activation on the browser side so the "background" fullscreen request fails.  I confirmed that disabling chrome://flags/?#user-activation-v2 reproduces the bug again.

Consuming user activation on fullscreen should be the right approach anyway, as discussed in the other bug.


### he...@gmail.com (2019-02-26)

@mustaq: I think this bug should be unduped from https://crbug.com/chromium/852645 and marked as fixed. While the PoC from this issue abused the requestFullscreen function not consuming user activation, it was not the only way to achieve that.

An exemple would be make the popup regain focus using the onbeforeunload dialog (make sure chrome://flags/?#user-activation-v2 is disabled so you can reproduce it): https://lbherrera.github.io/lab/spoof-variation/index.html

So what actually fixed this bug was UAv2. https://crbug.com/chromium/852645 should probably be changed to low severity or even none.

### mu...@chromium.org (2019-02-26)

Yes, you are correct: UAv2 fixed this bug through the restricted visibility of user activation (so the user activation in the opened window is now unavailable to the original window).

### mu...@chromium.org (2019-02-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-27)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-14)

Congrats! The Panel decided to reward $3,000 for this report :) 

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/851302?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, UI>Browser>FullScreen]
[Monorail blocked-on: crbug.com/chromium/696617]
[Monorail mergedinto: crbug.com/chromium/852645]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091613)*
