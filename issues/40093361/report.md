# Security: Permission request UI spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40093361](https://issues.chromium.org/issues/40093361) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2018-12-10 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 73.0.3635.0 (Official Build) canary (64-bit)  

Operating System: Mac

This is similar to <https://crbug.com/chromium/816033>

**REPRODUCTION CASE**

1. Load <http://permission.site>
2. Click on "Fullscreen"
3. Click on "Quota Management"
4. Click on "Popup"

Observe the permission request UI can appears over the popup tab.

## Attachments

- [Screen Shot 2018-12-10 at 03.57.12.png](attachments/Screen Shot 2018-12-10 at 03.57.12.png) (image/png, 1.3 MB)
- [windows.png](attachments/windows.png) (image/png, 16.0 KB)
- [screen.mov](attachments/screen.mov) (video/quicktime, 5.1 MB)
- [Enregistrement #5.mp4](attachments/Enregistrement #5.mp4) (video/mp4, 933.8 KB)

## Timeline

### mm...@chromium.org (2018-12-10)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Permissions>Prompts UI>Notifications]

### pe...@chromium.org (2018-12-10)

-> engedy, this isn't related to notifications

Looks like the permissions dialog isn't tied to a particular browsing window and can be drawn on top of another instead.

[Monorail components: -UI>Notifications]

### sh...@chromium.org (2018-12-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2018-12-12)

I think there isn't anything special about permission bubbles, so this is likely a generic z-ordering weirdness affecting all kinds of bubbles, if not all dialogs, on Mac.

Adding Mike, Dan and Peter (pbos@), who'd be more knowledgeable about this.

### pb...@chromium.org (2018-12-12)

This seems like Mac only, +ellyjones@, +lgrey@, I'm not sure Z ordering differs in Mac view.

I tested on Win / 73.0.3637.0 (Official Build) canary (64-bit) (cohort: Clang-64).

### av...@chromium.org (2018-12-12)

The permission bubble's z-ordering is quite broken. See https://crbug.com/chromium/910533 which IMO is basically the same bug.

### en...@chromium.org (2018-12-13)

Indeed, sounds like the same issue. Avi, do you have the cycles to work on this?

### av...@chromium.org (2018-12-13)

I don't have a ton of knowledge about the child windows and ordering. +sdy too. Is anything obvious jumping out at anyone on the Mac team?

### sh...@chromium.org (2018-12-28)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sd...@chromium.org (2018-12-28)

I can verify this when I'm in front of a debugger, but is it possible that the bubble's NSWindow level is being set and doesn't need to be?

### av...@chromium.org (2019-01-08)

I can't repro this on 73.0.3642.0, nor on ToT 73.0.3665.0.

Does this still repro for people?

### av...@chromium.org (2019-01-08)

(I'm running 10.11, BTW; can someone on 10.13/14/etc try this, as fullscreen has changed?)

### av...@chromium.org (2019-01-08)

Re https://crbug.com/chromium/913314#c10, no level is being set on *any* of the windows. We're purely using parent/child relationships, so it's odd that the WindowServer would interleave windows like that.

I still remain unable to repro, btw. I can repro https://crbug.com/chromium/910533 but I don't see it as more than Pri-3 if not related to this bug.

### av...@chromium.org (2019-01-08)

+Tommy who is helping me here.

### to...@chromium.org (2019-01-08)

I was not able to reproduce this bug either on Mac.

### to...@chromium.org (2019-01-08)

More details: I was not able to reproduce with:
Mac: High Sierra 10.13.6
Chrome: 73.0.3655.0

### av...@chromium.org (2019-01-08)

OP, what version of macOS are you using?

### ch...@gmail.com (2019-01-08)

I'm still able to repro this on canary 73.0.3665.0 on Mac Sierra 10.12.6.

### ch...@gmail.com (2019-01-08)

Note: Before trying to repro with the steps above, do not enter full screen mode with the green maximize button.

### ch...@gmail.com (2019-01-17)

Any update on this bug? Thanks :-)

### sh...@chromium.org (2019-01-23)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2019-01-23)

I've researched this on various versions of macOS, and while it doesn't repro on 10.10, 10.11, 10.13, or 10.14, it does repro on 10.12 (in my case, 10.12.6, 16G1618).

What happens is that on everything but 10.12, when the window comes out of fullscreen the tabbed window is in front with the permission bubble, and the popup is behind it. On 10.12, the popup is in the front, then the popup, then the tabbed window. Any clicks on anything forces the ordering to be correct.

It's not clear to me how the popup window is coming to the front, or why that would differ on 10.12. Fullscreen is a weird thing that changes from release to release, so I wouldn't be surprised if this were a bug that showed up only in 10.12.

My thought is that a worst-case scenario is that I scope a fix for 10.12-only that when we drop out of fullscreen, we try forcing the activation of the window that lost fullscreen. I'm going to see if I can get more debugging info, but I'm not sure how much it's worth digging since this looks like an OS issue from two revs ago.

### av...@chromium.org (2019-01-24)

I'm seeing a slightly different version of the issue compared to the OP. On my Mac on 10.12, the popup window isn't a key window yet lies above the key window, between it and the permission bubble.

In any case, while we're in that state, I see:

(lldb) po [NSApp orderedWindows]
<__NSArrayM 0x1af325610>(
<NativeWidgetMacNSWindow: 0x1b3f1fff0>,    // permission bubble
<NativeWidgetMacNSWindow: 0x1ab79ba20>,    // popup window
<NativeWidgetMacNSWindow: 0x1bc649620>,    // browser window status bubble
<BrowserNativeWidgetWindow: 0x1af778ee0>,  // browser window
<NativeWidgetMacNSWindow: 0x1af394600>     // popup window status bubble
)

Clicking on the browser window yields:
<__NSArrayM 0x1c117f400>(
<NativeWidgetMacNSWindow: 0x1b3f1fff0>,    // permission bubble
<NativeWidgetMacNSWindow: 0x1bc649620>,    // browser window status bubble
<BrowserNativeWidgetWindow: 0x1af778ee0>,  // browser window
<NativeWidgetMacNSWindow: 0x1af394600>,    // popup window status bubble
<NativeWidgetMacNSWindow: 0x1ab79ba20>     // popup window
)

Clicking on the popup yields:
<__NSArrayM 0x1ac083320>(
<NativeWidgetMacNSWindow: 0x1af394600>,   // popup window status bubble
<NativeWidgetMacNSWindow: 0x1ab79ba20>,   // popup window
<NativeWidgetMacNSWindow: 0x1b3f1fff0>,   // permission bubble
<NativeWidgetMacNSWindow: 0x1bc649620>,   // browser window status bubble
<BrowserNativeWidgetWindow: 0x1af778ee0>  // browser window
)

(I've annotated the windows.)

So it's clear that there is a genuine mis-ordering of windows here, to the extent that it's ordering a parent window in front of its child, and that the ordering snaps into place as soon as any ordering event comes in.

Can we issue a pointless window ordering call to make things work?

In experimentation, I'm finding from lldb that:

(lldb) po [[[NSApp orderedWindows] objectAtIndex:0] orderFront:nil]

causes the window ordering to clean up properly when I continue. Let's try that as a patch and see if it works.


### av...@chromium.org (2019-01-24)

That mostly works; doing a performSelector with a delay of 0 pretty reliably works. The popup still has a weird activation look (I was wrong in https://crbug.com/chromium/913314#c23; the switching to the Terminal app for lldb cleared the window) but at least that's just cosmetic.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6879cff00978bfce0801e8ed3107ceb7d8751c33

commit 6879cff00978bfce0801e8ed3107ceb7d8751c33
Author: Avi Drissman <avi@chromium.org>
Date: Fri Jan 25 17:49:23 2019

Fix window activation issue.

BUG=913314

Change-Id: I01de2642638dde55945f41dfa58da41a30b2c095
Reviewed-on: https://chromium-review.googlesource.com/c/1435957
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#626117}


### av...@chromium.org (2019-01-25)

So this should hit for canary 74.0.3685.0. OP, can you verify that it fixes this for you when that comes out?

Thanks!

### ch...@gmail.com (2019-01-25)

This seems like fixed on 74.0.3684.0 (Developer Build).


### av...@chromium.org (2019-01-25)

But 3684 didn't have the fix. 🤔

### ch...@gmail.com (2019-01-25)

Tested on two builds:

Good build: -refs/heads/master@{#626126}
Bad build: -refs/heads/master@{#626013}



### ch...@gmail.com (2019-01-25)

[Empty comment from Monorail migration]

### av...@chromium.org (2019-01-25)

Can you shrink your window a bit to show window ordering?

I'm really stumped here. I had repro-ed it here, so I'm not sure what's going on.

### ch...@gmail.com (2019-01-25)

[Empty comment from Monorail migration]

### av...@chromium.org (2019-01-25)

That's Chromium, though. What rev is that? That looks like exactly the fix that I landed.

### ch...@gmail.com (2019-01-25)

3343618014b5515716a132a70ecaca3c408bf699-refs/heads/master@{#626126}

Oops! I forgot to tell you that. lol :-)

### av...@chromium.org (2019-01-25)

I built my fix on 625790, so that doesn't help narrow your range of 626013-626126. Sigh.

I'm trying to remember the syntax to get a list of revisions on chromium.googlesource.com.

### av...@chromium.org (2019-01-25)

Wait... 626013-626126 has 626117 which is my fix.

In https://crbug.com/chromium/913314#c27, when you said "This seems like fixed on 74.0.3684.0 (Developer Build).", that was 626126 you built, which says it's 3684? My fix won't come out in official builds until 3685 though.

I'll call this fixed, then. If you can confirm this on an official released canary, that'd be great too.

### ch...@gmail.com (2019-01-25)

[Comment Deleted]

### ch...@gmail.com (2019-01-25)

I will verify this tomorrow.

### sh...@chromium.org (2019-01-26)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-01-26)

Double-check.

Tested on 74.0.3684.0 (Official Build) canary (64-bit). Fixed.


### av...@chromium.org (2019-01-26)

Whoo! Thank you.

### na...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-31)

Congrats! The Panel decided to reward $500 for this report :)

### na...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-15)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-02-19)

branch:3683

### aw...@google.com (2019-02-26)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-03-05)

[Security-UX-Sheriff] Checking in: did this end up getting merged to M-73?

### cr...@appspot.gserviceaccount.com (2019-03-08)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/33a1711d2b58cd48946cd31694897c86071a1bef

Commit: 33a1711d2b58cd48946cd31694897c86071a1bef
Author: avi@chromium.org
Commiter: avi@chromium.org
Date: 2019-03-08 16:19:32 +0000 UTC

Fix window activation issue.

BUG=913314

Change-Id: I01de2642638dde55945f41dfa58da41a30b2c095
Reviewed-on: https://chromium-review.googlesource.com/c/1435957
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#626117}(cherry picked from commit 6879cff00978bfce0801e8ed3107ceb7d8751c33)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1511915
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/branch-heads/3683@{#787}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### sh...@chromium.org (2019-05-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-05-04)

This issue was migrated from crbug.com/chromium/913314?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093361)*
