# Security: Cross-Page and Cross-Domain Propagation of Click events on Mobile Devices

| Field | Value |
|-------|-------|
| **Issue ID** | [40080545](https://issues.chromium.org/issues/40080545) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input |
| **Reporter** | ma...@westonit.net |
| **Assignee** | la...@chromium.org |
| **Created** | 2014-09-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

On mobile versions of Chrome, under ideal circumstances click events can fire in a context different to where they were initially triggered.

This is achieved by utilizing touch events on a 'trigger' page, and click events on a 'victim' page.

The trigger page utilizes the ontouchstart event handler to redirect to the victim page, where a click event can be fired - either within the same domain, or across domain/same origin boundaries.

This is a similar class of vulnerability to Clickjacking on desktop, however I'd classify this differently as the click event should not be propagating to the next page loaded. I'd describe it as 'Tapjacking'.

This click also fires in the exact same location as the original tap - so you can use this to target specific elements on a victim page.

**VERSION**  

Chrome Version: Chrome 37.0.2062.117  

Operating System: Android 4.4.4 Build KTU84P, Nexus 5

**REPRODUCTION CASE**  

Please find at the foot of this report two HTML Snippets.

Trigger.html - upload this to one location  

Victim.html - upload this to a location on another server, to show cross-domain propagation

This vulnerability relies on the fact that both touch and click events fire on mobile devices. When the user 'taps' a screen, you'll see ontouchstart, ontouchend and a click - this vulnerability relies on the interaction being detected as a 'tap'.

When the div on the Trigger.html tag is tapped, the user is redirected to the victim page (you'll need to update the JS here to point to the URL in your environment)

After the subsequent page has loaded, if conditions are 'just right', you'll see the click handler on Victim.html has fired and displayed an alert. (I found this to be reproducible nearly 100% of the time, but I'm biased. The only instances I found this isn't reproducible is if you tap too fast/slow, or pageload is delayed - so timing is a big factor here.)

Like clickjacking - this could have performed an action on the behalf of a user on another site.

EXPLOITABILITY  

What I've supplied is intentionally not targeted to any specific application. This could be extended to target specific buttons which require only single clicks to perform actions (buy this, post that, email this). The idea would be to utilise the trigger as a deceptive landing page to trigger a typically user initiated event by knowing the location on-screen of the element, and encouraging the user to tap on the location.

I’d be happy to assist in further investigations here.

Kind Regards,  

Matt

Trigger.html

<html>
<head>
<title>Tapjacking - Trigger</title>
<script>
function redirect()
{
window.location = "http://127.0.0.1/victim.html"; // CHANGE ME
}
</script>
</head>
<body>
<div style="width: 100%; height: 100%; background-color:pink;" ontouchstart="redirect();">(tap anywhere in the pink box)</div>
</body>
</html>

Victim.html

<html>
<head>
<title>Tapjacking - Victim</title>
</head>
<body>
<div style="width: 100%; height: 100%; background-color:green;" onclick="alert('At Victim');">&nbsp;</div>
</body>
</html>

## Timeline

### rs...@chromium.org (2014-09-28)

rbyers: Could you take a look at this or help find a better owner?

### cl...@chromium.org (2014-09-28)

[Empty comment from Monorail migration]

### jo...@chromium.org (2014-09-29)

you don't even need to redirect, no? it should be enough to place an iframe over the touched area.

### ma...@westonit.net (2014-09-29)

Hi,

Yes, you could do that - but that is just plain click jacking.

This is different in that normal click jacking mitigation (frame breaking/anti clickjaking headers) are not effective in this case.

This is important in that it allows you to propagate an interaction into the middle of the context of another page.  I'm not aware of any existing mitigation pattern that would prevent this kind of attack.

Cheers,
Matt



### jo...@chromium.org (2014-09-29)

fair enough

### ma...@westonit.net (2014-09-29)

Please let me know if a more complete working example of this would be helpful, I cut it down pretty lean so I could paste it in.

I'm on NZDT (UTC+13), but am happy to help in any way I can. (Unfortunately my development skills are limited to web apps, so I can really only explain myself/provide more test cases)

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### rb...@chromium.org (2014-09-29)

Thanks for the report, I agree this is something we should fix.  The 300ms click delay is almost certainly making this a lot easier to exploit, but presumably we should be trying to prevent this in all cases.  I'm struggling a little to see how high we need to aim the bar here.

Do we have any protection against similar issues with mouse?  Eg. what if a Trigger navigates on mousedown to a site that handles events on mouseup?  click won't fire, but I think mouseup still will.  Or what if the Trigger tried to predict when the user is just about to click based on watching mouse movement (eg. by studying the motion of the mouse as it moves towards a button, you can probably guess somewhat reliably when they're just about to click it).

Off the top of my head, the best option I can see right now is to abort gesture processing when the browser sees a navigation.  I _think_ we can close the race window entirely (for cross-origin navigations that switch the renderer process anyway).

Jared, Alex, WDYT?

### ae...@chromium.org (2014-09-29)

Hmm, my concern is that "aborting gesture processing" may be a bit messy and need special code for each platform.  How about letting the gesture processing go on as normal but ignore the GestureTap if the last seen GestureTapDown was at another URL?

### jd...@chromium.org (2014-09-30)

There is an associated issue here with how touches/gestures are dispatched from the browser. If a page blocks the main thread, say, on handling a touchstart, an arbitrary number of gestures can become queued in the browser (not just the delayed click within the same gesture). With the same bait-and-switch tactics, all such queued gestures could be hijacked.

Hard flushing all browser-side gesture/touch queues does sound appealing, and though some implementation details might be tricky, it's probably a good long term solution. In the meantime, perhaps we could implement the suggestion from aelias@ in #9 that ensures TapDown+Tap share the same target? I believe there's some synthetic click code we'd need to patch up to ensure Taps are always preceded by TapDown, but that's probably something we should do anyhow.

### kl...@chromium.org (2014-09-30)

Shouldn't we flush the queue when the current page changed? This will include both navigation changed like in this bug, or even tab/window changed case.

### rb...@chromium.org (2014-10-02)

I'm not sure the suggestion in #9 will mitigate the problem much.  If the page navigates on touchstart, then it's entirely likely that even the GestureTapDown will go to the new page instead of the old one (though maybe less likely due to tighter timing).

That said, it would be easy to add some 'have seen GestureTapDown' logic to EventHandler::handleGestureTap as Jared suggests.  We'll probably have to fix a bunch of lazy layout tests, but otherwise I don't anticpate any problems with that.  I just don't think we'll be able to mark this bug 'fixed' as a result (especially if a page can rely on prerendering to ensure navigation to the victim happens very quickly).

Perhaps the problem is deeper here.  InputRouter maintains state that depends on the behavior (ACKs) of the target page.  Perhaps we shouldn't be keeping an InputRouter instance between cross-origin navigations at all?  RenderWidgetHostImpl::RendererExited resets the InputRouter to a new instance (to ensure we're not waiting for ACKs that will never arrive).  Why isn't this happening already on cross-origin navigation?  Can we make it?

### rb...@chromium.org (2014-10-03)

To answer my question above: we're not getting a new InputRouter for cross-origin navigations because renderer processes are still re-used in that case.  Site isolation plans on solving that (http://www.chromium.org/developers/design-documents/site-isolation) and so would fix this bug too.

Since that's the long term direction anyway, perhaps shorter term we should apply the same sort of logic by recycling the InputRouter on ever navigation (or at least every cross-origin navigation), even if we're not yet recycling the rest of the RWHI.

### cl...@chromium.org (2014-10-11)

rbyers@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-18)

rbyers@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-26)

rbyers@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-02)

rbyers@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ma...@westonit.net (2014-11-02)

Hi team, 

I've held back on releasing this to various other bug bounties because I don't want to jeapordise the chrome one. At what time would this be appropriate? This would be ramping it up from a proof of concept to a fully attack against a handful of bigname platforms. Is there any indication of an expected release for the fix here? 

Given the massive implications here (for the record: chrome is not the only browser with this exact vulnerability) I want them to be on the front foot with investigating client side mitigations, since this vulnerability will live on long after the fix.

Thanks,
Matt


### jd...@chromium.org (2014-11-03)

Sorry for the lack of response here. I've been toying with a few patches that flush all pending events from the browser using the |WebContentsObserver.DidNavigateMainFrame| hook. This should solve  most of the accidental cases, but probably not the malicious cases, e.g., what if a child iframe is the target and then cross-domain navigates? Ideally any processed touch events would be given a token linking them to a specific domain target, the generated gestures would propagate these tokens and be dropped if their token does not match the domain of the eventual gesture target?

I was hoping to have the simple fix (flushing queued input) in for M40, but again, I'm not sure this is sufficient, and we may need a security person to chime in here.

### rb...@chromium.org (2014-11-06)

Thanks Jared - OK if I reassign to you then?

What do you think of my suggestion in #13 to recycle the InputRouter on every navigation (or every cross-origin navigation)?  It sounds like site isolation will eventually cause that to happen anyway (as part of recycling the RWHI).  We should avoid adding extra complexity that won't be necessary long-term if we can...

### jd...@chromium.org (2014-11-06)

The simple change I was working on does recycle the router, but only for main frame navigations. Somebody else would have to comment as to whether that's sufficient.

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-11-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d47c1e4b6bb7e9b485f6dfede0236ddd5c823878

commit d47c1e4b6bb7e9b485f6dfede0236ddd5c823878
Author: jdduke <jdduke@chromium.org>
Date: Tue Nov 11 23:47:12 2014

[Android] Thoroughly reset gesture detection upon page navigation

The current gesture reset logic on Android uses a cancellation event
synthesized from the active touch sequence. However, this fails to reset
detection for timeout-based events, e.g. delayed tap and double-tap,
just after the pointer has just been released. Expose an explicit gesture
detection reset hook on the GestureProvider, called when the main
frame navigates or the window loses focus.

BUG=418402

Review URL: https://codereview.chromium.org/717573004

Cr-Commit-Position: refs/heads/master@{#303749}

[modify] https://chromium.googlesource.com/chromium/src.git/+/d47c1e4b6bb7e9b485f6dfede0236ddd5c823878/content/browser/renderer_host/render_widget_host_view_android.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/d47c1e4b6bb7e9b485f6dfede0236ddd5c823878/ui/events/gesture_detection/filtered_gesture_provider.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/d47c1e4b6bb7e9b485f6dfede0236ddd5c823878/ui/events/gesture_detection/filtered_gesture_provider.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/d47c1e4b6bb7e9b485f6dfede0236ddd5c823878/ui/events/gesture_detection/gesture_provider.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/d47c1e4b6bb7e9b485f6dfede0236ddd5c823878/ui/events/gesture_detection/gesture_provider.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/d47c1e4b6bb7e9b485f6dfede0236ddd5c823878/ui/events/gesture_detection/gesture_provider_unittest.cc


### cl...@chromium.org (2014-11-14)

jdduke@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### jd...@chromium.org (2014-11-14)

The change in #23, r303749, will prevent any delayed taps from firing after main frame navigation. In theory that should make touch-derived taps no worse than, say, mouse clicks (as noted by rbyers@ in #12). I'd still like to hear from security folks whether listening to main frame navigation on Android is sufficient here (i.e., r303749 addresses the sample case posted in #0, but are there simple derivative cases with iframes where we're still vulnerable?)

I have some changes in the works to further tighten the window, hard flushing all pending input on page navigation. However, it might take a bit more time to get it right, making sure the full input pipeline plays nicely with a new event stream after reset.


### bu...@chromium.org (2014-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ed1dafa7db5fcd150a757d1237c83a81666ec47f

commit ed1dafa7db5fcd150a757d1237c83a81666ec47f
Author: jdduke <jdduke@chromium.org>
Date: Tue Nov 18 15:57:03 2014

[Android] Always precede Tap gesture events with TapDown

The gesture detector generates TapDown events before Tap events, but
there there remain cases where synthetic Tap events are not preceded
by such TapDown events. Insert the expected TapDown for these synthetic
cases, also validating this event ordering in the
GestureEventStreamValidator.

A consistent ordering here provides the render process, and any downstream
gesture listener, more context to reason about and react to the gesture
event stream.

BUG=418402

Review URL: https://codereview.chromium.org/724313003

Cr-Commit-Position: refs/heads/master@{#304611}

[modify] https://chromium.googlesource.com/chromium/src.git/+/ed1dafa7db5fcd150a757d1237c83a81666ec47f/content/browser/android/content_view_core_impl.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/ed1dafa7db5fcd150a757d1237c83a81666ec47f/content/common/input/gesture_event_stream_validator.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/ed1dafa7db5fcd150a757d1237c83a81666ec47f/content/common/input/gesture_event_stream_validator_unittest.cc


### rb...@chromium.org (2014-12-03)

Jared, any update on this?  Is there more you think we should be doing?

I assume iframe cases aren't that interesting for clickjacking, right?  I was wondering about a malicious page which listened for touchend and repositioned an iframe so that a target of interest was under the exact location it new a GestureTap was about to happen.   But something similar is possible with mouse clickjacking, and I think our only strong answer is X-Frame-Options for disabling loading a page in an iframe, right?

### rb...@chromium.org (2014-12-03)

If the main set of reproduction cases possible here have been addressed, perhaps we should mark this bug as fixed (rather than leaving a security bug in Limbo) and file another for lower severity remaining cases?

### jd...@chromium.org (2014-12-03)

The only other immediate thought I had (to handle the iframe case after a fashion) was what you already mentioned in #12, adding the 'have seen GestureTapDown' logic to EventHandler::handleGestureTap.

### rb...@chromium.org (2014-12-03)

+kenrb who volunteered to take a look from a security team perspective.  The main questions we have are:

1) What's the known state for this type of attack on desktop (where do we draw the line for issues with mouse we will prevent/mitigate)
2) What state should we get to before calling this bug fixed?

### rb...@chromium.org (2014-12-03)

Re #29: I don't think the 'have seen GestureTapDown' logic will really help with iframe positioning attacks - the attacker could just reposition on touchstart and so guarantee that the GTD would go to the target frame.

Come to think of it, there's no reason to wait for the event to reposition at all, right?  If I have a point I want you to tap in an iframe, I can just put that frame scaled/translated so that the point of interest basically fills the viewport, and stick some content overtop of it in the main frame with pointer-events: none (so all the events pass through it to the target iframe), right?  Then I just need to wait for the user to tap/click anywhere and I've got the click I wanted.  I.e. seems like clickjacking against iframes is probably already known to be unsolvable (although I'm sure there are lots of details I'm missing).

### jd...@chromium.org (2014-12-03)

The TapDown idea is merely to tighten the risk window for delayed taps targeting frames other than the main frame. We've already tightened the risk window for delayed taps on main frame navigation (we prevent the delayed tap entirely), but not for other frame navigations.

### rb...@chromium.org (2014-12-03)

Right.  My point is there's no point worrying about frame navigations.  If the page is allowed in a frame (i.e. doesn't use X-Frame-Options) then it's already really easy to get clicks to go wherever you want there without having a navigation at all.

### jd...@chromium.org (2014-12-03)

Anything timing sensitive will probably need to be sanitized from the Blink side.

### ke...@chromium.org (2014-12-08)

Sorry for this being neglected by security team lately.  Rick is right that X-Frame-Options is the first line defense against clickjacking, and the troubling part about this bug is that it enabled clickjacking against sites that were using it. If we are talking about redirecting input events to content loaded in iframes, then that is not a problem we know how to solve.

For question 1 in https://crbug.com/chromium/418402#c30, I wasn't aware that this was possible before now. Ideally we would want it to be impossible to have input events queued across navigations, but 'very difficult' would be okay for if we are talking about short term. Nice to know that site isolation would solve this problem by preventing reuse of input routers across origins, except that there is no timeline for that on mobile devices. fwiw, I don't think we can do anything about pages trying to anticipate clicks and navigating immediately before that, but I doubt attackers could do that reliably. Navigating between a mouse down and a mouse up sounds like it could be avoidable.

### rb...@chromium.org (2014-12-12)

Thanks Ken.  I've played with a repro (http://jsbin.com/males/1/quiet).  It reproduced on M39 semi-reliably for me - varying between 10% and 30% of my taps.  I tried various things to adjust the timing, but never got it to reproduce more reliably on Android.  Note that I was able to repro with both a desktop and mobile viewport (so the 300ms click delay isn't essential to the repro).

On current dev channel (with Jared's fix) it definitely didn't reproduce as often, but I believe I still saw it once (but maybe I stuttered and tapped twice my accident).  Jared, can you think of any race that may remain?  Eg. what if we've created the gesture event but it's sitting in the InputRouter's event queue?  Should we be flushing the event queue on navigation as well?

Jared's fix was only for Android.  I can still reproduce the problem quite reliably on Aura.  Lan, can you please look into adding Jare'd mitigation to Aura as well (see https://codereview.chromium.org/717573004/diff/40001/content/browser/renderer_host/render_widget_host_view_android.cc).

### rb...@chromium.org (2014-12-16)

Note that Lan is out now until the new year, she'll get to the Aura side of this when she returns.

### rb...@chromium.org (2015-01-16)

Changing in the timing of how I serve from www.rbyers.net has broken the repro on Aura.  Use this version now instead: http://jsbin.com/males/2/quiet (it goes directly to github instead of relying on the redirect from www.rbyers.net I have now).

Lan is now actively working on getting this fixed in Aura.

### rb...@chromium.org (2015-01-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9d343ad2ea6ec395c377a4efa266057155bfa9c1

commit 9d343ad2ea6ec395c377a4efa266057155bfa9c1
Author: lanwei <lanwei@chromium.org>
Date: Wed Feb 11 01:46:00 2015

Reset gesture detection upon page navigation for Aura

In order to stop the gesture events to be generated and sent while navigating
to a different page on the main frame or the window loses focus, we decide
to cancel all the active touch events on the current Aura window before
the touch release event.

BUG=418402

Review URL: https://codereview.chromium.org/868123002

Cr-Commit-Position: refs/heads/master@{#315705}

[modify] http://crrev.com/9d343ad2ea6ec395c377a4efa266057155bfa9c1/content/browser/renderer_host/render_widget_host_view_android.cc
[modify] http://crrev.com/9d343ad2ea6ec395c377a4efa266057155bfa9c1/content/browser/renderer_host/render_widget_host_view_android.h
[modify] http://crrev.com/9d343ad2ea6ec395c377a4efa266057155bfa9c1/content/browser/renderer_host/render_widget_host_view_aura.cc
[modify] http://crrev.com/9d343ad2ea6ec395c377a4efa266057155bfa9c1/content/browser/renderer_host/render_widget_host_view_aura.h
[modify] http://crrev.com/9d343ad2ea6ec395c377a4efa266057155bfa9c1/content/browser/renderer_host/render_widget_host_view_base.cc
[modify] http://crrev.com/9d343ad2ea6ec395c377a4efa266057155bfa9c1/content/browser/renderer_host/render_widget_host_view_base.h
[modify] http://crrev.com/9d343ad2ea6ec395c377a4efa266057155bfa9c1/content/browser/web_contents/web_contents_impl.cc
[modify] http://crrev.com/9d343ad2ea6ec395c377a4efa266057155bfa9c1/content/public/android/java/src/org/chromium/content/browser/ContentViewCore.java


### la...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Merge Requested for M41 (Branch 2272).

AFAIUI, it only includes https://codereview.chromium.org/868123002 as every other CL seems to already be in M41.

Please update this issue if that is incorrect.

### pe...@google.com (2015-02-17)

[Automated comment] Less than 2 weeks to go before stable on M41, manual review required.

### pe...@chromium.org (2015-02-18)

Merge approved for M41 branch 2272.

### pe...@chromium.org (2015-02-20)

Note: M41 stable cut happens in days, and you're approved for merge.  Get it in there!  (Let me know if you need any help, or aren't confident.)

### rb...@chromium.org (2015-02-21)

Are we sure it's worth the (even potentially minor) risk to merge this to 41 at this late stage?  This is a long standing bug that wasn't deemed particularly urgent from a secuity perspective.  The fix for Android is already in stable, so the remaining CL was for taps on touchscreens on desktop/laptop devices only.

I'll defer to the security team experts here, but honestly I was surprised to see this last CL get a merge-request.  I don't think we ever merged the android fix back (and that's where the vast bulk of the value for this fix was IMHO).


### ti...@google.com (2015-02-21)

rbyers: With that context, then no - let's not merge this. I didn't realize that the fix was already in Android stable, which was my main concern for getting it into M41. We can let the last CL roll out in M42.

### rb...@chromium.org (2015-02-21)

SGTM, thanks.  Sorry I didn't chime in sooner with that essential context.

### ti...@google.com (2015-02-23)

No worries at all - thanks for chiming in!

### ti...@google.com (2015-04-14)

Congratulations Matt - our reward panel has voted to award you $1000 for this report!

Someone from our finance area should be in contact in two weeks to collect payment details. Please contact me directly if this doesn't happen.

We'll credit you in our release notes as "matt@westonit.net". Please let me know if you'd like to use another name or handle.

Cheers,
Tim


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ma...@westonit.net (2015-04-14)

Hi,

Can you please credit me and my co-discoverer as:

Phillip Moon and Matt Weston of www.sandfield.co.nz

Many thanks,
Matt

### ti...@google.com (2015-04-14)

No worries - I've listed the credit as "Phillip Moon and Matt Weston of Sandfield Information Systems"  (we don't put URLs in our release notes).

### ma...@westonit.net (2015-04-14)

Hi Tim,

Thank you -  if it's not too late can it please refer to us as 'Phillip Moon and Matt Weston of Sandfield'

Thanks,
Matt

### ti...@google.com (2015-05-06)

#54 - Updated: http://googlechromereleases.blogspot.com/2015/04/stable-channel-update_14.html

### cl...@chromium.org (2015-05-21)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-07-28)

Processing via our e-payment system takes about two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/418402?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080545)*
