# Security: Address bar spoof (repro Issue 648117)

| Field | Value |
|-------|-------|
| **Issue ID** | [40088278](https://issues.chromium.org/issues/40088278) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Mac |
| **Reporter** | xi...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2017-07-06 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The <https://crbug.com/chromium/648117> can be reproduced.

**VERSION**  

Chrome Version: 59.0.3071.115 stable (64-bit), 61.0.3150.0 canary (64-bit)  

Operating System: MAC OS 10.12.5/10.13

**REPRODUCTION CASE**

1. Launch chrome and navigate to poc.html
2. Click on the button
3. Click on "Back to safety" which is on the interstitial page and wait
4. Observe

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 402 B)
- [spoof.png](attachments/spoof.png) (image/png, 88.3 KB)

## Timeline

### ji...@chromium.org (2017-07-06)

I am able to reproduce this issue on Mac M59 stable too.
kenrb@, could you take a look since this issue seems very close to crbug.com/648117 ?

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### sh...@chromium.org (2017-07-06)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-07-06)

Charlie, can you offer any thoughts on this? It looks very similar to https://crbug.com/chromium/729105, in that it is Mac-only, and involves going back from the SSL error interstitial. However, it still repros on Canary, and has some minor differences, such as using a javascript URL.

### ji...@chromium.org (2017-07-06)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-07-11)

jialul@: Were you able to repro this on something other than Mac?

### ji...@chromium.org (2017-07-11)

I didn't test Android. It worked on Win and Linux. The "Spoof" text showed up for 2-3 seconds after step 3 on Win and Linux.

Feel free to change the OS label. 

### ke...@chromium.org (2017-07-11)

Ok, the 2-3 seconds is working as intended. There is a timer that is supposed to make a blank page appear if the visible content doesn't match the URL for too long.

On Mac, though, the timer doesn't seem to reliably work on this test case, and sometimes "Spoof" remains visible indefinitely.

### cr...@chromium.org (2017-07-11)

I've only seen a successful spoof on Mac Stable 59.0.3071.115 so far.

I agree with Ken that if it disappears after 2-3 seconds, then Ken's timer is kicking in because no new paints are being generated and we fall back to showing white to prevent the spoof.  That's working as intended.

On Windows Beta 60.0.3112.50 and Canary 61.0.3154.0, the spoof text disappears after a few seconds.  Same on Mac Canary 61.0.3154.0, despite the initial report-- the spoof text disappears.  On Linux 61.0.3141.7, there's no spoof text at all after clicking Back to Safety.

We should probably remove the Windows and Linux labels, but it's worth confirming whether the spoof text sticks around on Windows Stable 59.0.3071.115, and we should also run a bisect on Mac.  It's possible this is an M59-only issue across platforms.

### ke...@chromium.org (2017-07-11)

Charlie: I've repro'd on Mac Canary, although it took a few tries. I'm building trunk on Mac to see if I can make it happen on a debug build.

### cr...@chromium.org (2017-07-11)

Yeah, this doesn't seem reliable enough to run a bisect.  I'm seeing a bunch of cases where Twitter successfully loads in the popup window instead.  I'll leave it to you at this point.

For what it's worth, the spoof text disappeared on Windows M59, so I think it's best to consider this Mac-only.

I did also see some M60 Mac runs where the text disappeared (e.g., 60.0.3083.0), similar to M61.  But given https://crbug.com/chromium/739621#c9, it could be a racy problem on Mac even affecting Canary.

### ke...@chromium.org (2017-07-11)

+ccameron@, because this bug might have something to do with BrowserCompositorMac behavior.

It looks like, on Mac, DelegatedFrameHost::EvictDelegatedFrame() doesn't work when an interstitial is currently being displayed. I have verified that while the interstitial is up, it is called and attempts to set a solid color layer on its DFHClient's layer, but when "Back To Safety" is clicked on to dismiss the interstitial, the original compositor frame is still visible.

This repro doesn't always work because if the timer fires before or after the interstitial is visible, then EvictDelegatedFrame() works correctly, and the "Spoof" text goes away.

On Linux and Windows the graphics are always cleared successfully, whether the interstitial is up or not.

### cc...@chromium.org (2017-07-12)

Yes, Mac is different from Linux and Windows in that it doesn't use Aura, so the logic for how it handles these may differ.

IIRC we had some issues with modal dialogues and compositor updates in the recent past, +tapted.

### ta...@chromium.org (2017-07-13)

Is this an interstitial rather than a modal dialog?

The only thing that comes to mind is https://crbug.com/chromium/739676. But there's some other work around interstitials for OOPIF.

### ke...@chromium.org (2017-07-13)

It is an interstitial, although I don't know that it is related at all to https://crbug.com/chromium/739676. This isn't OOPIF-related.

We are trying to evict a compositor frame from the page while an interstitial is being displayed, via DelegatedFrameHost::EvictDelegatedFrame(), but on Mac the compositor frame is not discarded as it should be -- it becomes visible again once the interstitial is dismissed. I spent a little bit of time trying to debug this today, and I'm wondering if this has to do with BrowserCompositorMac going into the HasDetachedCompositor state when the interstitial appears.

### ke...@chromium.org (2017-07-13)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-07-13)

ccameron@: I think I understand what is happening, although I don't know the best way to fix it. The problem seems to be that when the interstitial appears, it Hides the page's RenderWidgetHost, which causes the BrowserCompositorMac to suspend the ui::Compositor, as in https://chromium.googlesource.com/chromium/src/+/00e438cd22c5e2f26d003c15c0a1621aa24acd0c.

This means that even though we subsequently discard the delegated frame, the layer tree changes never commit, so the previous content becomes visible again when the interstitial is dismissed and the RenderWidgetHost is again shown.

I don't know if there is a cleaner way to fix this, but potentially BrowserCompositorMac could detect and flag this situation, and try again to evict the frame when it changes state from HasDetachedCompositor to HasAttachedCompositor.

Is there a better way that doesn't require special-casing frame eviction?

### ke...@chromium.org (2017-07-14)

Patch up: https://chromium-review.googlesource.com/c/571421/

### ke...@chromium.org (2017-07-14)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-07-14)

Moving questions for CL review to the bug:

piman asked, "1- the CompositorLock doesn't trigger just because a RWHV goes hidden, it triggers when the (other) RWHV goes visible and doesn't have a frame. On Chrome OS it also prevents UI updates, so you don't see the new URL until the CompositorLock times out / is resolved by the new frame coming. Obviously Mac is different, but there the CompositorLock should be paired with a mechanism that blocks the message loop (see RenderWidgetHostImpl::PauseForPendingResizeOrRepaints called from RenderWidgetHostViewMac::Show) so similarly we should not show the new URL? Or could this be an order-of-operations issue?
2- the CompositorLock times out after 67ms, well before the 2-3s timeout, at which point the clear layer should commit and replace the frame. Is that not happening?"

I think you might be looking at a different CompositorLock. The problematic one here is held by RecyclableCompositorMac::Suspend(), in content/browser/renderer_host/browser_compositor_view_mac.mm. That one does not have a timeout.

### pi...@chromium.org (2017-07-14)

Ok, I was thinking of the lock taken in DelegatedFrameHost::WasShown.

Still, once that lock is released in RecyclableCompositorMac::Unsuspend, shouldn't the solid color layer commit at that point?

### ke...@chromium.org (2017-07-14)

That's a good question, and it was the first thing I was looking at. Since it doesn't commit, and I couldn't find a way to make it commit (I tried to force a full redraw on the LayerTreeHost), I thought that might be by design, and that we would need another update after the lock was removed. Is there something else I should be looking at in cc code?

### pi...@chromium.org (2017-07-14)

+danakj
I'm pretty sure the lock expiring/being canceled (i.e. via LayerTreeHost::SetDeferCommits(false)) is supposed to trigger a commit, if one would have happened while being locked. If that doesn't happen it sounds like a bug in cc.

### da...@chromium.org (2017-07-18)

https://cs.chromium.org/chromium/src/cc/scheduler/scheduler_state_machine.cc?rcl=42a520c163d95e4192a270296e70fff0e925c854&l=894

It doesn't. But the client can SetNeedsCommit when it defers them, and then that commit would go through after.

### da...@chromium.org (2017-07-18)

> is supposed to trigger a commit, if one would have happened while being locked.

Ahhh I should read better. It doesn't do a commit on its own, but it doesn't clear the need for a commit, which would happen when the defer goes away, in ProcessScheduledActions().

https://cs.chromium.org/chromium/src/cc/scheduler/scheduler_state_machine.cc?rcl=42a520c163d95e4192a270296e70fff0e925c854&l=443
https://cs.chromium.org/chromium/src/cc/scheduler/scheduler.cc?rcl=9195b2b71b5f80b084dac791607149b7c9550362&l=605

### ke...@chromium.org (2017-07-26)

Thanks for the comments, and the clarification of expected compositor behavior. Further debugging reveals the following: the issue is that RecyclableCompositorMac is holding a CompositorLock with no timeout, but before it releases that lock it calls DFH::WasShown(), which creates a lock with a 67ms timeout. However, the semantics of Compositor::GetCompositorLock() mean that the timeout is ignored, and the WasShown() lock is held indefinitely.

There are a couple of ways to fix this, one is to do something similar to my first CL in DelegatedFrameHost to work around the overlapping lock case. The second way is to change the behavior of GetCompositorLock().

I've uploaded a CL with the latter approach to see if it passes all the trybots: https://chromium-review.googlesource.com/c/587464/

### bu...@chromium.org (2017-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/aaf6b58123e9bc49391a8f8cfe057b7c3269e9ef

commit aaf6b58123e9bc49391a8f8cfe057b7c3269e9ef
Author: Ken Buchanan <kenrb@chromium.org>
Date: Thu Jul 27 15:46:12 2017

Ensure overlapping compositor locks can time out

With the current logic in Compositor::GetCompositorLock(), if a lock is
being held with no timeout and another lock is being created that has a
timeout value, the second lock will never time out. The lock can be
held indefinitely if the caller was relying on the timeout.

This changes the behavior of GetCompositorLock() so that a lock with
a non-null timeout will override a lock that had a null timeout, causing
them both to timeout. Potentially this could cause unexpected behavior
where a lock without a timeout value is still timing out, but this can
already happen if the locks are taken in the inverse order.

Bug: 739621
Change-Id: I32cfbbbc61adf14db263aa413e4019877b041d70
Reviewed-on: https://chromium-review.googlesource.com/587464
Reviewed-by: danakj <danakj@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#489942}
[modify] https://crrev.com/aaf6b58123e9bc49391a8f8cfe057b7c3269e9ef/ui/compositor/compositor.cc
[modify] https://crrev.com/aaf6b58123e9bc49391a8f8cfe057b7c3269e9ef/ui/compositor/compositor.h
[modify] https://crrev.com/aaf6b58123e9bc49391a8f8cfe057b7c3269e9ef/ui/compositor/compositor_unittest.cc


### ke...@chromium.org (2017-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-28)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-31)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-08-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-06)

+ awhalley@ (Security TPM) for M61 merge review.

### ke...@chromium.org (2017-08-06)

The fix appears to have caused a regression (https://crbug.com/chromium/752566). Given the limited scope of the URL spoof (i.e. it's a non-interactive spoof that can't steal credentials, it's only on Mac, it requires specific user actions to make it work), I wouldn't have flagged it for merge.

### go...@chromium.org (2017-08-06)

Thank you kenrb@ for https://crbug.com/chromium/739621#c34.

awhalley@,sheriffbot requested merge t0 M61 at https://crbug.com/chromium/739621#c31. But pls do see https://crbug.com/chromium/739621#c34 before approving the merge. We can't take the fix in for M61 if it is causing regression. Thank you.

### aw...@chromium.org (2017-08-07)

Removing merge labels, as we certainly shouldn't merge something that introduces regressions.  If there's a simple and regression free fix in time we should re-consider for 61, while it can't be used for credential stealing directly, I could see it being used for phone phishing (e.g. call this number). (Interestingly, it's probably a bigger phishing risk for people who know to look for EV treatment :-)

### aw...@chromium.org (2017-08-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-08-08)

Hi xisigr@ - the VRP panel decided to award $500 for this.  Cheers!

### xi...@gmail.com (2017-08-08)

Thanks. :)

### cc...@chromium.org (2017-08-09)

I think that the calls to DelegatedFrameHost::EvictDelegatedFrame are a red herring here.

That function is not called to remove a frame because it shouldn't be shown. Rather, it is called because a cache of old frames feels that it should clean up -- it isn't always called, and when it is, it depends on timing.

The fact that calling DelegatedFrameHost::EvictDelegatedFrame makes visible content disappear is, IMO, a bug. RenderWidgetHostViewMac::ClearCompositorFrame should not clear a frame that is up as we await content.

Also of note is that the ui::Compositor recycling of BrowserCompositorMac doesn't affect this (when I disable it, the issue persists).

Looking at the RWHVMac code, it is doing exactly what is is supposed to do. The sequence of calls is:

- window is created
- RWHVMac A is created put in the window and draws the "spoof" page
- RWHVMac B is created for the security warning
- RWHVMac B is shown & RWHVMac A is hidden
- [the user presses the "back to safety" button)
- RWHVMac A is shown & RWHVMac B is hidden

The correct thing for the compositor to do in this case is draw whatever content RWHVMac A is supposed to show. There is absolutely no signal that is sent to RWHVMac A to indicate that it should not draw its previous content.

I think that the root bug here is something different. In particular, if we just use the following HTML
  <script>
    function f() {
      w = window.open(
          "javascript:document.write('spoof');location='http://twitter.com'",
          "new","width=500 height=500");
    }
  </script> 
  <a href="#" onclick="f()">Login Twitter</a>
Then we will briefly draw the attached spoof.png, before navigating to Twitter.

That we draw the "spoof" text in the RWHV that is supposed to be used by Twitter, and that we attribute it to Twitter, is the problem (AFAICT, I should mention here that I'm not an expert in that area).

The fact that clicking "Back To Safety" navigates back to that state doesn't seem relevant to me -- it's just re-showing the state that we already showed -- if it was okay the first time around it should be okay the second time around (and if it is bad the second time it should also be bad the first time).

WRT the compositor lock change, I'd prefer to take it out, since it's causing lots of flashing issues on Mac.

### ke...@chromium.org (2017-08-09)

ccameron@: Thanks for the comment. This has been our approach to fixing these bugs for a couple of years now but it could be useful to revisit at a higher level.

The fundamental problem is that there are two things that happen in the renderer process for a navigation:
(a) The navigation commits, which means the new page is loaded and the old page has been unloaded.
(b) The new page paints, sending a compositor frame to the browser process for display.

The URL in the omnibox updates when the renderer notifies the browser process about the commit having happened, (a). The trouble is that it is very hard to get a guarantee that (b) follows after (a). Bug reporters have found several ways of preventing the new page from successfully painting, using script in another tab that has a handle to the new page's window. This causes the effect of the URL having updated while the old content is still displayed. A gap between the URL updating and the content updating is normal, but in typical cases is a matter of milliseconds.

Guaranteeing that the renderer sends a compositor frame after a navigation commit seems impossible, so our approach was to implement a timer in the browser process -- after a new navigation commits, the RenderWidgetHostImpl counts 4 seconds, during which it expects the renderer to submit a compositor frame for the new page. See https://cs.chromium.org/chromium/src/content/browser/renderer_host/render_widget_host_impl.cc?l=1018&rcl=f34edfdd32fd9660fa358ee546d4010f7ce04aa1.

If the timer fires, RenderWidgetHostImpl::ClearDisplayedGraphics() calls RenderWidgetHostView*::ClearCompositorFrame(), which we expect to remove the stale frame.

As noted above, RenderWidgetHostViewMac::ClearCompositorFrame(), prior to my CL, sometimes didn't work if the RWHV is hidden (it works on other platforms), because the CompositorLock taken in DelegatedFrameHost::WasShown never times out even though it provides a 62ms timeout value when it takes the lock.

Apparently this might need a bit more thought, since it has caused a regression, and I'm open to any feedback on the above.

### cc...@chromium.org (2017-08-09)

Ah, I stand corrected in #40. Historically EvictDelegatedFrame was coming from a callback from a cache. Now I see that the 4 second delay is intentional.

Lemme take another stab at this.

### cc...@chromium.org (2017-08-09)

Couple of ideas:

1. Make RenderWidgetHostViewMac::ClearCompositorFrame release the compositor lock. This is probably the simplest fix. This means that we'll potentially draw the wrong stuff for the 4 seconds until we get the call to clear the compositor frame.

2. Make it so that the RWHVMac of the non-interstitial page be removed from the NSView hierarchy. This will blow away the underlying ui::Compositor.

I have a patch for [1] that is fairly simple, so I'll put that up.

### aw...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5788690fb1395dc672ff9b3385dbfb1180ed710a

commit 5788690fb1395dc672ff9b3385dbfb1180ed710a
Author: Christopher Cameron <ccameron@chromium.org>
Date: Thu Aug 10 22:23:44 2017

mac: Make RWHVMac::ClearCompositorFrame clear locks

Ensure that the BrowserCompositorMac not hold on to a compositor lock
when requested to clear its compositor frame. This lock may be held
indefinitely (if the renderer hangs) and so the frame will never be
cleared.

Bug: 739621
Change-Id: I15d0e82bdf632f3379a48e959f198afb8a4ac218
Reviewed-on: https://chromium-review.googlesource.com/608239
Commit-Queue: ccameron chromium <ccameron@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#493563}
[modify] https://crrev.com/5788690fb1395dc672ff9b3385dbfb1180ed710a/content/browser/renderer_host/browser_compositor_view_mac.h
[modify] https://crrev.com/5788690fb1395dc672ff9b3385dbfb1180ed710a/content/browser/renderer_host/browser_compositor_view_mac.mm
[modify] https://crrev.com/5788690fb1395dc672ff9b3385dbfb1180ed710a/content/browser/renderer_host/delegated_frame_host.cc
[modify] https://crrev.com/5788690fb1395dc672ff9b3385dbfb1180ed710a/content/browser/renderer_host/render_widget_host_view_mac.h
[modify] https://crrev.com/5788690fb1395dc672ff9b3385dbfb1180ed710a/content/browser/renderer_host/render_widget_host_view_mac.mm
[modify] https://crrev.com/5788690fb1395dc672ff9b3385dbfb1180ed710a/content/browser/renderer_host/render_widget_host_view_mac_unittest.mm


### bu...@chromium.org (2017-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/28e0a3c183499e50b1b89231d4ed40bafb8883fe

commit 28e0a3c183499e50b1b89231d4ed40bafb8883fe
Author: ccameron chromium <ccameron@chromium.org>
Date: Fri Aug 11 04:59:46 2017

Revert "Ensure overlapping compositor locks can time out"

This reverts commit aaf6b58123e9bc49391a8f8cfe057b7c3269e9ef.

Reason for revert:
This has been subsumed by r493563

It is required that indefinite locks be held indefinitely,
even if a timeout lock is created in the middle. Not doing
so results in flashes, see crbug.com/752566

Original change's description:
> Ensure overlapping compositor locks can time out
> 
> With the current logic in Compositor::GetCompositorLock(), if a lock is
> being held with no timeout and another lock is being created that has a
> timeout value, the second lock will never time out. The lock can be
> held indefinitely if the caller was relying on the timeout.
> 
> This changes the behavior of GetCompositorLock() so that a lock with
> a non-null timeout will override a lock that had a null timeout, causing
> them both to timeout. Potentially this could cause unexpected behavior
> where a lock without a timeout value is still timing out, but this can
> already happen if the locks are taken in the inverse order.
> 
> Bug: 739621
> Change-Id: I32cfbbbc61adf14db263aa413e4019877b041d70
> Reviewed-on: https://chromium-review.googlesource.com/587464
> Reviewed-by: danakj <danakj@chromium.org>
> Reviewed-by: Antoine Labour <piman@chromium.org>
> Commit-Queue: Ken Buchanan <kenrb@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#489942}

TBR=danakj@chromium.org,kenrb@chromium.org,piman@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 739621
Change-Id: Iedfa6b518e3f51195a43f4bc1d4d03634ca8b125
Reviewed-on: https://chromium-review.googlesource.com/611800
Reviewed-by: ccameron chromium <ccameron@chromium.org>
Commit-Queue: ccameron chromium <ccameron@chromium.org>
Cr-Commit-Position: refs/heads/master@{#493671}
[modify] https://crrev.com/28e0a3c183499e50b1b89231d4ed40bafb8883fe/ui/compositor/compositor.cc
[modify] https://crrev.com/28e0a3c183499e50b1b89231d4ed40bafb8883fe/ui/compositor/compositor.h
[modify] https://crrev.com/28e0a3c183499e50b1b89231d4ed40bafb8883fe/ui/compositor/compositor_unittest.cc


### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/739621?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail mergedwith: crbug.com/chromium/750633]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088278)*
