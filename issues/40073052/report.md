# Touch events allow cross-origin access

| Field | Value |
|-------|-------|
| **Issue ID** | [40073052](https://issues.chromium.org/issues/40073052) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals, Internals>Input>Touch>Screen |
| **Platforms** | Android, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2012-09-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Touching in two different iframes gives both documents accesses to touches in each other. Not only can the page access the touches in the second document, but they can use the target's of these touches to access and modify the DOM of the other document.

**VERSION**  

Chrome Version: 18.0.1025.166  

Operating System: Android

**REPRODUCTION CASE**  

<http://dl.dropbox.com/u/72157/iframetest.html>

## Timeline

### pa...@chromium.org (2012-09-12)

If I understand correctly, when I touch in *either* iframe, the function logTouch should run in *both* iframes, right? I'm not seeing that. Instead. I only see messages appended to the DOMs of the touched iframe.

Note that I am running on Chrome version 18.0.1025306, an internal pre-release build. What version of Android are you running? I have 4.1.1.

### pa...@chromium.org (2012-09-12)

FWIW, on Chrome for iOS, I can't get the red frame to report touch events at all. Same behavior in Safari. And in neither browser do I see a cross-origin problem.

### ho...@gmail.com (2012-09-12)

The issue is with multi finger input. I think the "correct" behaviour here is that touches in each frame only show up in their respective frame. If you touch in both frames and "move" your finger in one, you should see events logged in that frame and not the other. Events in that frame should have changedTouches.length == 1, targetTouches.length ==1, touches.length == 1 (except for touchend where touches.length == 0). I'll modify the test to output that as well.

Currently in Relase Chrome (Nexus 7) I see events in both frames when I move my finger in one. Those events have changedTouches.length == 2 and touches.length == 2. The test page will log events in both frames when you move your finger (which it shouldn't). The bigger security issue is that I can access the targets and use them to modify the document:

event.changesTouches[i].target.ownerDocument.innerHTML = "Hello world"

Firefox also shows the touches in each frame, but trying to access ownerDocument (or any properties on the target) throws an access exception. iOS Webkit is just screwed up and ignores the second frame entirely, which is also wrong (but not a security risk).


### pa...@chromium.org (2012-09-12)

Success! I get any cross-origin events only if I do exactly what you say in https://crbug.com/chromium/148567#c3. Thanks. I haven't yet found another combination of events that causes a problem.

CCing some Chrome on Android friends, and removing Chrome on iOS friends. Grace and Srikanth, who's a good person to assign this to?

### ab...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2012-09-13)

[Empty comment from Monorail migration]

### ol...@gmail.com (2012-09-13)

Since both Gecko and Webkit have similar issues about where to dispatch the events, 
we should coordinate how to fix that (and hopefully get the behavior documented in the
W3C touch event spec, at least as a non-normative information).


### qi...@chromium.org (2012-09-14)

I think we need a better spec/definition for event.changedTouches. Here is how this is currently defined:

"readonly attribute TouchList changedTouches
a list of Touches for every point of contact which contributed to the event.
For the touchstart event this must be a list of the touch points that just became active with the current event. For the touchmove event this must be a list of the touch points that have moved since the last event. For the touchend and touchcancel events this must be a list of the touch points that have just been removed from the surface. For the touchenter and touchleave events, this must be a list of the touch points that have just entered or left the target element."


So event.changedTouches will include touch events to all touch targets if the current touch event is not stationary.
However, event.targetTouches will only include events that targets the particular node.
So if we want to fix this cross-origin access, we have to redefine event.changedTouches.


### qi...@chromium.org (2012-09-14)

An alternative we can do is that in event.changedTouches, we set the target to NULL for all the touches.

### ol...@gmail.com (2012-09-14)

One option is to limit touch sessions to one document only;
if you do touchdown on document A, the touchdown for the second finger would be
also dispatched only in document A. If the second touchdown would happen somewhere 
outside the document (like over document B), target could be the document element
of document A.

Or we could limit things to same origin, but it would be somewhat odd to specify that
event targeting depends on origin checks.

### ol...@gmail.com (2012-09-14)

[Comment Deleted]

### ol...@gmail.com (2012-09-14)

[Comment Deleted]

### [Deleted User] (2012-09-16)

[Empty comment from Monorail migration]

### ab...@chromium.org (2012-09-18)

[Empty comment from Monorail migration]

### rb...@chromium.org (2012-09-18)

[Empty comment from Monorail migration]

### rb...@chromium.org (2012-09-18)

Note that Chrome M22 (which is about to go to stable) enables touch events on Win7 by default.  I.e. we may start to see more websites taking advantage of the current implementation details (especially as Win8 touch devices enter the market).

Regarding #8: this isn't just about changedTouches, but also 'touches', right?  It's only targetTouches that is currrently safe.

Personally, I'd rather not change the semantics of touches/changedTouches - I can imagine scenarios where it would be useful to know where the other touch points are on the window.  For example, imagine a site like Google+ that wants to implement it's own app-wide multi-finger gesture (say 3 finger swipe left/right to switch streams or something).  If one of the fingers happens to start on top of a frame (say a youtube video), it shouldn't prevent the site from being able to detect the gesture. 

I like the Firefox approach described above (target gives back a neutered object when it's from another frame) - anyone see any disadvantage to matching Firefox here?


### ol...@gmail.com (2012-09-18)

We see Gecko behavior as a security bug and will change the behavior.

### ol...@gmail.com (2012-09-18)

...it is just not clear yet whether we'll (A) force all the touch events
during a touch session (from the first touch down to last touch up) to go to
one document, or whether to (B) support per-document touch sessions or (C) let
same origin documents to share the same touch session.
I personally prefer A.

### rb...@chromium.org (2012-09-18)

Olli, can you elaborate on why you see the Gecko behavior as a security bug?  I thought the only problem was with exposing the 'target' to a frame other than where it came from?

I believe all three of your solutions in #18 could break the scenario I described in #16 (unless, perhaps, we have some heuristic for deciding when to target the main frame).

### rb...@chromium.org (2012-09-20)

After reading the Mozilla bug, I see why their current behavior isn't sufficient (the node isn't completely neutered, you can still get access to things like innerHTML, just not ownerDocument, etc.).  I suggest that we simply ensure 'target' is null (or otherwise completely neutered - such as pointing to the iframe element) whenever the current target belongs to a different frame.

Note this is an issue on Windows (starting in M22) and ChromeOS (starting in M23) too.
 
qinmin@are you actively driving this for Android?

Are we sure this is SecSeverity-Medium and not High?  Some mitigating factors from my experiments on desktop Chrome:
 - The page being attacked must have something that enables touch events (eg. a touchevent listener, or something that implicitly listens like <input type=range>).
 - A multi-finger gesture is required (with one finger in each frame) - it may not be easy to trick the user into doing that 
 - Of course the page being attacked can always use X-FrameOptions to prevent the attack (i.e. many google sites are already protected)

### ol...@gmail.com (2012-09-20)

target should never be null. That would be an odd and inconsistent API.

Did you check how Safari works on iOS?



### qi...@chromium.org (2012-09-20)

In Safari, 2nd touch on the other frame is ignored. 

@rbyers: I worked on touch events for android and I can make the change once we have a unanimous solution here.

### ol...@gmail.com (2012-09-20)

Does Safari dispatch events to different iframes if they are in same domain, or
does it always limit touch events to one document only.
(I don't have any iOS devices, so can't test.)

### rb...@chromium.org (2012-09-25)

Safari appears to dispatch events only to a single frame (whichever frame the first touch point started in).  Talking about this with rjkroege@ we think it's probably the best approach in the short-term (a lot of value to being consistent more-or-less with iOS, and keeping it simple).

Effectively there is only ever one document receiving touch events, and that's determined by the first touch point.  For secondary events starting over top of iframes, the event goes only to the document being targeted and the 'target' is, of course, the iframe element.

Admittedly this won't quite solve my Facebook/Google+ scenario, but it'll get pretty close in practice (as long as first finger starts outside an iframe).  It also avoids the  confusion of having multi-touch gestures split across frames.

Once we have the security hole plugged, we could have a more open discussion about how to completely solve the facebook/google+ scenario I described - but it's not urgent given that it's pretty broken today anyway.

Any objections to making this basic approach the POR?

### pa...@chromium.org (2012-09-25)

rbyers: Yes, SecSeverity-Medium due to the requirement of user interaction. We believe that mitigates the problem.

And yes, your approach makes sense to me.

### qi...@chromium.org (2012-09-25)

What if the first touch is on a frame without any touch handlers? and the 2nd touch happens to be on a frame with touch handlers? 
We should do nothing in this case?

### ol...@gmail.com (2012-09-25)

Whether or not some window/document/element has listeners shouldn't affect to where
the events are dispatched.

### qi...@chromium.org (2012-09-26)

hmm... If i mistakenly have a finger(or any body part) somewhere in one iframe, and I tried to touch another iframe that has a touch handler, nothing would happen.
Because of the thin bezels of mobile devices, i think the case would become pretty common if people use their left hand to hold the device, and the right hand to perform touch.


### rb...@chromium.org (2012-09-26)

But the scenario of an extra accidental touch is already something we don't try to work around - eg. if you have a thumb down on the side, then scrolling or tapping with another finger won't do what you expect.  Why should the iframe case try to be any more robust?



### rb...@chromium.org (2012-09-26)

[Empty comment from Monorail migration]

### qi...@chromium.org (2012-09-26)

I am wondering whether safari actually dispatches events to the left frame. The behavior on safari seems that it ignores all the touch events on the right iframe.

For example, touch on the right iframe will not cause any text to be displayed. And if I perform a scroll gesture in the right iframe, it will scroll the whole page. 

If I put one finger on the left iframe first, and then put another finger on the right iframe, nothing would happen for the 2nd touchstart. The number of touches and the number of changed touches is always 1 however I manipulate both of fingers.

To follow what safari does, a simple way is in EventHander::handleTouchEvent(), we can just record the document of the first touchstart target, and do nothing on all the following touchpoints whose document is not equal to the recorded document. Does that sounds a reasonable approach?

### rb...@chromium.org (2012-09-28)

iOS's behavior seems more complicated than that.  What you describe is the behavior for two sibling iframes, but if one of the iframes is a parent of the other then the behavior is different.  Eg. use this test case: http://dl.dropbox.com/u/72157/iframetest4.html

I think what we want is something like:
 - on first touch, record the document (as you suggest) 
 - for all subsequent touches, do the hit test only in the context of that document (so if it's on a child iframe, we dispatch it to the IFrameElement, not to the frame itself)


### ol...@gmail.com (2012-09-28)

yes, that is how I understood iOS behavior, and that is what I expect to be
implemented in Gecko.
Also note, if new subsequent touches happen outside the current context document,
they don't cause any events. 

### qi...@chromium.org (2012-09-30)

https://bugs.webkit.org/show_bug.cgi?id=97973 created and a change is uploaded for review.

### ol...@gmail.com (2012-10-01)

Note, the webkit bug isn't marked security sensitive for some reason.

### in...@chromium.org (2012-10-01)

Olli, thanks! i marked webkit bug as a security bug now.

### [Deleted User] (2012-10-08)

[Empty comment from Monorail migration]

### rb...@chromium.org (2012-10-09)

Just to double check - are we really OK not merging the fix for this back to M23 or earlier?  At some point we need to update the TouchEvents standard to cover the behavior here - when can we feel free to talk more openly about this issue?

### ol...@gmail.com (2012-10-09)

Be careful before releasing any information about this.
I guess quite some mobile browsers are affected and assuming they don't have
better security checks when accessing DOM objects from different domains, this
is rather critical xss.

### pa...@chromium.org (2012-10-10)

Although XSS is bad, we reserve "critical" (SecSeverity-Critical) for bugs that could take over the browser process, for example. (See http://www.chromium.org/developers/severity-guidelines.) I think this bug is correctly triaged as SecSeverity-Medium, especially since it requires (complex) user interaction to trigger. That stops it from being a mass malware vector.

Backporting this fix to the Chrome we are shipping is probably not feasible, and it doesn't meet our severity standards for backports anyway. Eventually, Chrome for Android will be merged with current upstream Chrome and the issue will be resolved then.

I don't know what Windows with touch wants to do; adding ananta to see what he thinks.

rbyers: I think you can and should go ahead and update the TouchEvents standard to specify the good behavior. Don't publicize exact details of this bug and how some version of Chrome or other is or is not affected, but do go ahead and do the right thing, standards- and implementation-wise.

### rb...@chromium.org (2012-10-15)

Thanks for the guidance!  Glad to hear we don't need to wait to update the standard.

### rb...@chromium.org (2012-10-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-11-09)

Any progress?

### [Deleted User] (2012-11-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-11-15)

[Empty comment from Monorail migration]

### ke...@google.com (2012-11-15)

Not a dev blocker for 25.  Let's make sure we have this ASAP, but we won't hold releases to anywhere but stable for this.

### la...@google.com (2012-11-27)

[Empty comment from Monorail migration]

### qi...@chromium.org (2012-12-13)

Webkit patch landed. Closing this now.

### rb...@chromium.org (2012-12-18)

Security team: just wanted to let you know that FF18 is expected to be released around Jan 7, and their release notes will mention that they've fixed the equivalent (but less severe) issue there.  

I'll still avoid mentioning anything around this issue and Chrome/WebKit, but let me know ASAP if you think we need to ask FireFox to be unusually quiet about their fix as a result of the outstanding WebKit issue in deployed browsers.


### ol...@gmail.com (2012-12-18)

I might say "release notes may mention". But please let us (Mozilla) know if this issue shouldn't be mentioned at all.

### sc...@gmail.com (2012-12-18)

Feel free to mention it!

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2012-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-26)

@holden101: thanks for the report! This report qualifies for a $500 Chromium Security Reward -- Happy New Year :)

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### [Deleted User] (2013-02-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### la...@google.com (2013-03-15)

[Empty comment from Monorail migration]

### la...@google.com (2013-03-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### rb...@chromium.org (2013-04-04)

[Empty comment from Monorail migration]

### rb...@chromium.org (2013-10-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/148567?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Internals>Input>Touch>Screen]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073052)*
