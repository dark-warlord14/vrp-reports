# Security: Modal dialogs overlaying Fullscreen permission dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40083111](https://issues.chromium.org/issues/40083111) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML>Dialog, Blink>WindowDialog, UI>Browser>FullScreen |
| **Reporter** | he...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2015-10-31 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability makes it possible to display a modal dialog in front of the Fullscreen permission dialog, making it "impossible" to the user to know he entered fullscreen mode, enabling the attacker to spoof the URL.

**VERSION**  

Chrome Version: [46.0.2490.80 m] + [stable].

**REPRODUCTION CASE**

1. Click on the link: <http://lherrera.16mb.com/fullscreen.html>
2. Click on the link in the attacker's page to access "google.com".
3. An alert will show up asking you for credentials.

\* Given I use an image to spoof all the page, because of different screen resolution the image maybe in a wrong position. But a dedicated attacker could easily fix this, as he knows the users screen resolution and operational system.

Here is a video simulating the attack:  

<https://www.youtube.com/watch?v=-y-XIbbj9gM>

## Attachments

- [spoof1.png](attachments/spoof1.png) (image/png, 141.8 KB)
- [osx-canary-button-styles.png](attachments/osx-canary-button-styles.png) (image/png, 683.7 KB)

## Timeline

### me...@google.com (2015-11-01)

Once again, thanks for the report! Modal dialogs strike again.

mguica is currently working on the redesign of the fullscreen UI: https://code.google.com/p/chromium/issues/detail?id=352425

Matt, any thoughts? I feel like it was recently being discussed that we should suppress modal dialogs when fullscreen is up? And hopefully the new UI is still going to show the origin (not sure what the latest state is).


### me...@google.com (2015-11-01)

+avi who likes modal dialogs :)

### he...@gmail.com (2015-11-05)

I was doing some tests with this, if the domain is short enough (like ir.ru) it's possible to call a prompt from an iframe that will overlay the fullscreen permission dialog almost completely and won't display an origin (see spoof1.png).

It's possible to do the same thing using the inline extension install too. User clicks on a link that start an inline install, then he enters fullscreen, the inline dialog shows up and overlays the fullscreen permission dialog. The result would be very similar to https://crbug.com/chromium/550047 (maybe better as the attacker could craft his page asking the user to install the extension).

That said, I think the severity should be increased, as the attacker could use this to spoof the omnibox and do one of the attacks mentioned above. What you think?




### mg...@chromium.org (2015-11-05)

#1 The new UI is not going to show any origin (because we do not consider fullscreen to be a serious attack vector, it doesn't matter *which* site is fullscreen, only that you know you are in fullscreen). The new UI is shown at https://code.google.com/p/chromium/issues/detail?id=352425#c95.

So the important part of this bug is not that the origin is hidden underneath the modal dialog, but that the fullscreen bubble itself is hidden, perhaps masking the fact that you have gone fullscreen. That's a little concerning but I still think this is Severity-Low (unless I'm misunderstanding something).

To my knowledge we've never discussed restricting modal dialogs in a fullscreen context.

### he...@gmail.com (2015-11-05)

I was talking about the origin in the prompt dialog (that appears as Javascript), not about the origin in the permission dialog.

The objective of the attack is to mask that you entered fullscreen (as you said), given it would allow the attacker to spoof the omnibox.

That's why I think the severity should be increased, because from my understanding the result isn't so different from any other URL spoof.


### mg...@chromium.org (2015-11-05)

+egm for security.

Right. I think this is somewhat of a concern, but it is less severe than another URL spoof (as the security team has previously discussed regarding fullscreen), because you have to spoof the whole browser UI.

A normal URL spoof looks exactly like the user's browser: themes, bookmarks bar, currently open tabs, OS theming, etc. With the fullscreen attack, the website has to "guess" what the user's desktop looks like and approximate it. That makes it less convincing. But I'm sure it can still fool people.

Note: I am not concerned about tricking people into entering text in the modal dialog (since the origin is displayed there --- though I don't understand why it isn't in #3). I am more concerned about the fullscreen bubble disappearing before anyone can see it, due to the modal dialog.

### he...@gmail.com (2015-11-05)

Fair enough.
About the origin in #3, you can check https://crbug.com/chromium/537452.

### eg...@chromium.org (2015-11-05)

Agreed with mgiuca this is low severity. Given the origin is still visible in the alert, users can still reason about where they are inputting their credentials (even if they aren't aware the site is in fullscreen mode). 

### he...@gmail.com (2015-11-05)

#8, that can be avoided, see #3. But as mgiuca said, the attack would be mitigated by other factors he mentioned.

### fe...@chromium.org (2015-12-09)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-12-09)

https://crbug.com/chromium/565760 provides a much better PoC. Check out https://fkp.me/lbhspoofs/ and the video at https://www.youtube.com/watch?v=GV9lKUz2WEE.

The demo is so convincing that I think we should upgrade to either high or medium severity. Tentatively marking as medium-severity.

It's also worth noting that this is now public and not eligible for a reward because it was posted on YouTube.

### fe...@chromium.org (2015-12-09)

I haven't dug too deeply into this yet but my guess is that the convincing PoC is combining multiple bugs to work.

### cl...@chromium.org (2015-12-09)

[Empty comment from Monorail migration]

### he...@gmail.com (2015-12-09)

[Comment Deleted]

### he...@gmail.com (2015-12-09)

#11, The video is marked as unlisted and I just published the link here. I didn't disclose it.

### cl...@chromium.org (2015-12-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-12-10)

Upgrading the severity means you need to find an owner, so back to you for triage. :)

### js...@chromium.org (2015-12-10)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-12-10)

hey palmer, i hear you like bugs.....

### fe...@chromium.org (2015-12-10)

hey palmer, i hear you like bugs.....

### cl...@chromium.org (2016-01-01)

palmer@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-22)

palmer@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-02-13)

palmer@: Uh oh! This issue is still open and hasn't been updated in the last 64 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ra...@chromium.org (2016-02-18)

It seems like the fullscreen bubble should possibly show up on top of the alert box? Or could we move alert boxes when in fullscreen?

### mg...@chromium.org (2016-02-18)

It might be hard to change the stacking order. Perhaps a better solution is to center the alert box vertically when in fullscreen mode?

Note: This doesn't affect mouse lock because the alert box automatically exits from mouselock mode.

### cl...@chromium.org (2016-03-10)

mgiuca@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### me...@chromium.org (2016-03-16)

Matt: Does the problem still exist with the new bubble? 

### mg...@chromium.org (2016-03-17)

The link demonstrating the attack is broken:
http://lherrera.16mb.com/fullscreen.html

And there are no other details provided. luan.herrera@hotmail.com: could you put it back or post it here. (Posting an attachment containing the source code to a bug report is better than an external link.)

I can't test it, but I wouldn't imagine the new bubble has fixed it. It is the same code as the old bubble.

### me...@chromium.org (2016-03-17)

I think the POC simply shows an alert after entering fullscreen. This should work:

<html>
<button id="btn">Enter fullscreen</button>
<script>
document.getElementById("btn").onclick = function() {
  document.body.webkitRequestFullScreen(function(){});
  setTimeout(function() {
    alert(0);
  }, 100);
}
</script>
</html>

I can confirm it still works with the new UI.

### mg...@chromium.org (2016-03-17)

Right. What did you think about my #25: to move the alert box to the center of the screen when the browser is in fullscreen mode?

### me...@chromium.org (2016-03-17)

Sounds like a good start.

Can we go one step further and disable modal dialogs in full screen? (--> avi: I think you might like that idea)

### mg...@chromium.org (2016-03-17)

That would be great.

### cl...@chromium.org (2016-04-07)

mgiuca@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-21)

mgiuca: Uh oh! This issue still open and hasn't been updated in the last 35 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-05-06)

mgiuca: Uh oh! This issue still open and hasn't been updated in the last 50 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### np...@chromium.org (2016-05-23)

I confirmed this still repro's on dev channel, with changes that were made to dialogs in the recent past.  I'd vote for disabling dialogs in full screen.

### mg...@chromium.org (2016-05-24)

#37: Do we need security / UX / web standards approval before doing this? It sounds like a potentially controversial change.

### me...@chromium.org (2016-05-24)

You might consider sending a blink intent to deprecate/remove before proceeding.

### mg...@chromium.org (2016-05-25)

I'm not sure I'm the right person to do this. I'm responsible for the fullscreen notification bubble (and that already isn't my main job). I don't have any experience with the modal dialogs. Adding Blink>HTML>Dialog; perhaps someone from there can take a look.

It also may be worth discussing this with Interventions working group (https://github.com/WICG/interventions). I will file a bug there and see if anyone is interested.

[Monorail components: Blink>HTML>Dialog]

### mg...@chromium.org (2016-05-25)

Actually, since that's public, if we want to have this discussion in public (which would also be the case with sending mail to blink-dev), we need to unrestrict this bug first. meacer@?

### me...@chromium.org (2016-05-25)

I'd be okay with unrestricting this bug if it low severity, but not sure with medium.
mbarbella@: WDYT?

mgiuca@: Maybe you could avoid being specific while describing this case in the interventions bug, and just mention the general idea of disabling dialogs in fullscreen? (that is, if we decide to keep the bug restricted)

### mg...@chromium.org (2016-05-25)

#42 I don't think there is a strong case for doing so without discussing the security implications of this.

### mg...@chromium.org (2016-05-25)

The other thing we can do is just my suggestion in #30 to move it to the center instead of disabling it, and then open a new bug for removing it, and talk with Interventions at that time. (To reiterate, I don't want to be responsible for driving that effort.) I'm curious what avi@ thinks since his name has come up several times on this thread but hasn't commented.

### av...@chromium.org (2016-05-25)

If we can remove alerts for fullscreen pages, that would be awesome. I don't know if we have the political will to do that. Until my dialog work happens, moving the dialog would help on the Views platform (they're already centered on the Mac).

I'd be cool with that, though I hope UX would be OK here.

### me...@chromium.org (2016-05-25)

+1 to moving the dialog to the center. It will also no more overlap browser chrome, which is extra good.

### mg...@chromium.org (2016-05-26)

Dialog is centered on Firefox and Edge as well, so doing that seems fine. Not sure it fully solves the issue since a very tall alert could still cover the fullscreen bubble, but it's going to look a lot more suspicious.

avi@ would you be able to change the dialog to the center? I had a quick look and found:
UpdateModalDialogPosition in constrained_window_views.cc which is what's responsible for setting the position. But it gets the position from ModalDialogHost::GetDialogPosition and that's virtual and I have no idea which class it's using to get the position. (I'm too far out of my knowledge about this system.)

### av...@chromium.org (2016-05-26)

BTW, with the new scheme, the plan is to have centered dialog boxes all the time. Hope I can make that happen soon.

As for making this happen now for fullscreen, I'm a Mac person and don't know Views. Maybe sky@ or pkasting@?

### mg...@chromium.org (2016-05-26)

I think it would be easier to make all dialog boxes always centered, than trying to make a special case for alert boxes in fullscreen. I can probably keep digging to find out how to do that if you think we can make that change globally now.

### av...@chromium.org (2016-05-26)

I tried to get UX to approve a centered dialog style for OldSpice and got pushback, saying that we had enough UI styles already. Ugh.

Maybe this can help change their minds.

### mg...@chromium.org (2016-05-26)

+bbergher, ainslie: Would you be able to comment on this? Can we just make all the modal dialogs centered instead of in the top third of the screen?

(Avoid security problem with overlapping a modal dialog with the fullscreen bubble.)

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### bb...@chromium.org (2016-05-26)

I support making all modal dialogs centered. As far as a very long message still blocking the notification:

1. We seem to truncate the prompt string after a certain length, still leaving the notification visible
2. Such a long string would probably seem suspicious (though that's obviously not enough to be trusted).

ainslie@ is out, back on Tuesday, so it might be worth waiting for him before taking action.

### me...@chromium.org (2016-05-26)

Just to clarify, modal dialogs here refer to content-initiated modal dialogs, right? Because we still want trusted dialogs to overlap browser chrome.

### av...@chromium.org (2016-05-26)

Absolutely. We need to build a distinction between trusted dialogs that are unspoofable, and untrusted dialogs.

### ai...@chromium.org (2016-06-06)

re: #50 
"I tried to get UX to approve a centered dialog style for OldSpice and got pushback, saying that we had enough UI styles already. Ugh."

To make that anxiety more precise, here's what we are shipping in OSX canary today (attached). We have so much work to do to make Chrome UIs feel deliberate and coherent - and we plan to do that work as a continuation of the MD-Top-Chrome work (which is just focused on tabs and toolbar). 

Instead of creating a new position or style for untrusted dialogs, I'd prefer to explore using the normal trusted position and button style while also doing something extra to make it clear that certain strings are coming from the developer. There are a range of options I can imagine.

Maybe +emilyschechter@ can help us coordinate a time to chat. 


### me...@chromium.org (2016-06-06)

> Instead of creating a new position or style for untrusted dialogs, I'd prefer to explore using the normal trusted position and button style while also doing something extra to make it clear that certain strings are coming from the developer.

I'm not sure how this will be possible without adding even more text and styling. I also disagree that moving untrusted dialogs inside the content area is adding another style. Rather, it's changing the existing style to be more consistent with what a user would expect, that is, page generated content only shows up in page controlled area. From the user's and our perspective, an alert() shouldn't be any different than an HTML generated dialog.

### pa...@chromium.org (2016-06-30)

Have we had this discussion yet? I don't think we should gate fixing this bug on the UX design team; we should try to at least get some kind of mitigation happening that doesn't require new design work. Random ideas:

* Can the full-screen notification always have the highest Z-order?

* We would like to kill window.{alert,prompt,confirm} anyway; maybe block them in fullscreen mode as a first step toward deprecation?

* Ensure that modal dialogs always show the real origin? What's the PoC code for this one, by the way? The obvious thing of just calling window.prompt("foo") and window.location = "javascript:window.prompt('foo')" always causes the real origin to show, so maybe we're already doing that? Would that be mitigation enough for this bug?

### mg...@chromium.org (2016-07-01)

I think removing alerts in fullscreen would be good (but I'm not part of those discussions). If we're going to do that soon, we don't need another mitigation for this bug.

> * Can the full-screen notification always have the highest Z-order?

I've spent most of this week enragedly trying to do this for another bug (https://crbug.com/chromium/623862), pretty much the same issue: a modal dialog covering up the fullscreen. Our widget system is amazingly bad for manually setting z-orders. There are procedural StackBelow / StackAbove commands, but they don't let you set a permanent Z order (so as soon as a new window is created it goes in front). And they aren't implemented on Mac. So there's really no good solution for making sure a particular dialog is on top, on all platforms. :( It's been a sad, sad week.

I'd rather kill alerts in fullscreen.

### pa...@chromium.org (2016-07-01)

avi: This may be relevant to your interests.

### av...@chromium.org (2016-07-01)

mgiuca:
> I think removing alerts in fullscreen would be good (but I'm not part of
> those discussions).

There are discussions? I've seen grumblings about it, but haven't personally seen more. If you think this should happen, you totally should write an intent and push it. I will support you in whatever way I can.

(And if you don't want to be the public face of this, and want me to do it, I'm out next week, so talk to me when I get back on the 11th.)

### mg...@chromium.org (2016-07-01)

#61:

> There are discussions?

I mean the discussions about removing alert() entirely which you seem to have been having for some time.

### av...@chromium.org (2016-07-01)

> I mean the discussions about removing alert() entirely which you seem to have been having for some time.

Oh, right. Yes, but that's not going to happen for a while. If this bug is a good reason to take a small step of killing them in a specific circumstance, we should grab it independently.

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-08-01)

ping - any updates here?

### mg...@chromium.org (2016-08-01)

Hi, (getting harrassed by sheriff) :)

It looks like the decision that was made was to drop alert() boxes when in fullscreen mode. If we're going to do that, then it doesn't really make sense for me to do it since I have no knowledge of that area of the code (nor the time to learn it). Therefore, assigning to avi@.

I can point you in the right direction for "is the browser in fullscreen" checks. Specifically, if you have a Browser* browser, it is:

browser->exclusive_access_manager()->fullscreen_controller()->IsControllerInitiatedFullscreen()

See https://cs.chromium.org/chromium/src/chrome/browser/renderer_context_menu/render_view_context_menu.cc?l=1210 for an example.

### av...@chromium.org (2016-08-01)

Was that the decision that was made? If so, doing that is trivial and I'll get that done by the end of the day.

All alert() boxes? How about prompt() ones, or confirm() ones?

### av...@chromium.org (2016-08-01)

I'm proceeding with the plan of just preventing all JavaScript dialogs. I hope we don't have to suppress onbeforeunload ones too.

Is there still a working repro? It seems like the repros have died of linkrot.

### he...@gmail.com (2016-08-01)

#70:

data:text/html,<html><button id="btn">Enter fullscreen</button><script>document.getElementById("btn").onclick = function() { document.body.webkitRequestFullScreen(function(){});setTimeout(function() { alert(0); }, 100);}</script></html>

### av...@chromium.org (2016-08-01)

Luan: Thanks!

Fix is at https://codereview.chromium.org/2194243002 . Fixing compilation, verifying tests, will send for review soon.

### me...@chromium.org (2016-08-01)

Looks like there hasn't been any discussion outside this bug about the change to remove alert on fullscreen.

I'm going to drop view restrictions if no one objects, so that we can refer people to the bug.



### av...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### mg...@chromium.org (2016-08-02)

I think it makes sense to do as many modal dialogs as are tied together in the same system. I would imagine alert(), prompt() and confirm() are all implemented the same way so hopefully can all be done at the same time. onbeforeunload would be separate so we can think about that later.

### mg...@chromium.org (2016-08-02)

Oh, I see from the CL that it's actually easier to suppress them all at the same time, but you avoid the onbeforeunload because we actually still need it. SGTM. I'll write more on the CL.

### av...@chromium.org (2016-08-02)

Yes. Suppressing the "onbeforeunload" dialog scares me, because it's used to save data. But treating all the others as the same feels good to me.

### np...@chromium.org (2016-08-25)

Discussion of an actual social engineering page that covers the full-screen message with an alert: https://groups.google.com/a/google.com/d/msg/chrome-karma-team/FhCQGe2duC0/D-11O45BBgAJ

So this is being used in the wild now.

### he...@gmail.com (2016-08-25)

Would be possible for me to get access to the discussion? It says my account has no authorization to view it.

### av...@chromium.org (2016-08-25)

Should we put this up as an intent?

### me...@chromium.org (2016-08-25)

I feel like we need a stronger case for the intent at http://go/fullscreen-alert-intent. I can't seem to find another security bug for fullscreen+alerts, and we don't have metrics to cite for the current usage. We can still send it, but I'd expect pushback without those.

mgiuca and I was talking about this yesterday. The obvious and simpler alternative is to simply change the placement of the dialogs, so should we do that instead?

### av...@chromium.org (2016-08-26)

We'd need to talk to UX, and good luck. When I was talking to UX about new UI for OldSpice, I got severe pushback, and that's for a redesign and a rework of functionality.

### me...@chromium.org (2016-08-26)

Do you mean we need to talk to UX for changing the positioning of the alert, or the whole deprecation?

### mg...@chromium.org (2016-08-26)

I can't give you access to that discussion, but the exploit site is:
http://www.mswindowsalert.online

### av...@chromium.org (2016-08-26)

Yes. If we want to move alerts to address this issue, we need to talk to UX.

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2016-10-07)

It seems we are in a deadlock on this medium severity security bug. Displaying browser chrome when an alert dialog is shown (https://crbug.com/chromium/642568) was considered because we thought it would help with this bug. But per Matt's comments in that bug, doing so still doesn't help unless we move alert dialogs inside content area.

@ainslie: Given that gating on site engagement isn't happening soon either, what is the proposal from the UI team to go forward? Is consistency the main argument against moving alerts inside content area? If so, I'd like to understand it better, because current display style isn't consistent with anything else either. The dialogs are fully controlled by the page, yet they overlap browser chrome. These dialogs are a class of their own, so I don't think we'll be introducing yet another dialog style by fixing their positioning.


### ai...@chromium.org (2016-10-10)

[Comment Deleted]

### ai...@chromium.org (2016-10-10)

I think it'd make more sense to chat in person (with hwi@, rpop@, and emilyschechter@) than to continue the discussion here. 


### em...@chromium.org (2016-10-10)

Thanks, setting up some time now.

### pa...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### em...@chromium.org (2016-10-24)

We discussed and came up with two solutions to investigate:

(1) https://crbug.com/chromium/658900 - Fullscreen bubble should be ordered on top of other dialogs/alerts

(2) https://crbug.com/chromium/642568 - Make all popups in fullscreen temporarily show the browser UI

### mg...@chromium.org (2016-11-27)

[Empty comment from Monorail migration]

### mg...@chromium.org (2016-11-27)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX Blink>HTML>JavaScriptDialog]

### ra...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>JavaScriptDialog Blink>WindowDialog]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### np...@chromium.org (2017-01-20)

emilyschechter / mguica -- which of those two bugs is likely to happen first?  Both are P3s, but this is P1, so we should raise at least one of them.

### mg...@chromium.org (2017-01-23)

I think we decided https://crbug.com/chromium/658900 should happen. I bumped it to P1.

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-02-07)

Now I've gotten confused after meacer@ pinged https://crbug.com/chromium/670135. It looks like we came up with 3 different solutions:

(1) https://crbug.com/chromium/658900 - Fullscreen bubble should be ordered on top of other dialogs/alerts

(2) https://crbug.com/chromium/642568 - Make all modal dialogs in fullscreen temporarily show the browser UI

(3) https://crbug.com/chromium/670135 - Make all modal dialogs in fullscreen just exit fullscreen entirely

I think 3 is much more feasible (and given that we basically want to kill alerts anyway, I don't think a big deal). I will try to do 3.

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### ji...@chromium.org (2017-03-21)

[Empty comment from Monorail migration]

### ai...@chromium.org (2017-03-21)

[Empty comment from Monorail migration]

### ai...@chromium.org (2017-03-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-04-19)

Have we determined which of the three options in https://crbug.com/chromium/550017#c102 we'll implement? Seems like we are leaning towards (3).

### mg...@chromium.org (2017-05-02)

#107: I've decided to go ahead with (3), and closed the other bugs. Let's continue the discussion on https://crbug.com/chromium/670135.

### mg...@chromium.org (2017-05-02)

[Empty comment from Monorail migration]

### av...@chromium.org (2017-05-02)

Matt, can I give this bug to you then? Am willing to help with anything you need.

### mg...@chromium.org (2017-05-03)

Yeah I'll take this (which is now effectively a meta-bug for https://crbug.com/chromium/670135).

Not clear who will do engineering on it but it makes sense for me to own both.

### mm...@google.com (2017-05-04)

Matt, do you have any estimate on when you can get around it?

It's a Security FixIt week, and we are tying to get rid of all stale security issues. I'd be happy to help with this, if I can :)

### mg...@chromium.org (2017-05-04)

mmoroz: See https://bugs.chromium.org/p/chromium/issues/detail?id=670135#c9
(I'm considering this bug a tracking bug for that one; they would both be marked fixed at the same time.)

This is 2nd in my queue (behind another security bug). If you want to take it, go ahead: it isn't actually going to be working in any code I'm familiar with (so I have no state on it aside from what I wrote in https://crbug.com/chromium/550017#c9 there). Otherwise I'll try to get to it tomorrow (but unlikely).

### mm...@google.com (2017-05-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc

commit 0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc
Author: avi <avi@chromium.org>
Date: Tue Jun 13 03:22:13 2017

If JavaScript shows a dialog, cause the page to lose fullscreen.

BUG=670135, 550017, 726761, 728276

Review-Url: https://codereview.chromium.org/2906133004
Cr-Commit-Position: refs/heads/master@{#478884}

[modify] https://crrev.com/0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc/chrome/browser/printing/print_job_worker.cc
[modify] https://crrev.com/0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc/chrome/browser/printing/print_view_manager.cc
[modify] https://crrev.com/0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc/content/public/browser/web_contents.h


### av...@chromium.org (2017-06-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-22)

This bug requires manual review: M60 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-06-23)

Approving merge to M60. 

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-27)

Congratulations luan.herrera@! The VRP panel decided to award you $3,000 for this report. Nice one!



### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-07-10)

Please merge this to M60 ASAP. branch:3112

### ab...@chromium.org (2017-07-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f36b11b74a9d97621a65d466862948b0b8650889

commit f36b11b74a9d97621a65d466862948b0b8650889
Author: Avi Drissman <avi@chromium.org>
Date: Tue Jul 18 23:38:13 2017

If JavaScript shows a dialog, cause the page to lose fullscreen.

BUG=670135, 550017, 726761, 728276
TBR=avi@chromium.org

(cherry picked from commit 0720b02e4f303ea6b114d4ae9453e3a7ff55f8dc)

Review-Url: https://codereview.chromium.org/2906133004
Cr-Original-Commit-Position: refs/heads/master@{#478884}
Change-Id: Id833bfcc88e7faf9129ceb3184e11d37a71c61cc
Reviewed-on: https://chromium-review.googlesource.com/576402
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/branch-heads/3112@{#644}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}
[modify] https://crrev.com/f36b11b74a9d97621a65d466862948b0b8650889/chrome/browser/printing/print_job_worker.cc
[modify] https://crrev.com/f36b11b74a9d97621a65d466862948b0b8650889/chrome/browser/printing/print_view_manager.cc
[modify] https://crrev.com/f36b11b74a9d97621a65d466862948b0b8650889/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/f36b11b74a9d97621a65d466862948b0b8650889/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/f36b11b74a9d97621a65d466862948b0b8650889/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/f36b11b74a9d97621a65d466862948b0b8650889/content/public/browser/web_contents.h


### mg...@chromium.org (2017-07-19)

[Empty comment from Monorail migration]

### bb...@chromium.org (2017-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/550017?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>Dialog, Blink>WindowDialog, UI>Browser>FullScreen]
[Monorail blocked-on: crbug.com/chromium/642568, crbug.com/chromium/658900, crbug.com/chromium/670135]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083111)*
