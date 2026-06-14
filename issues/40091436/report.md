# Security: Address spoofing in Omnibox

| Field | Value |
|-------|-------|
| **Issue ID** | [40091436](https://issues.chromium.org/issues/40091436) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2018-05-19 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: Version 68.0.3435.0 (Official Build) canary (64-bit)  

Operating System: Mac

**REPRODUCTION CASE**

(repro <https://crbug.com/chromium/672847>)

1. Load the test case
2. Click on the button
3. Observe

## Attachments

- [Screen Shot 2018-05-19 at 20.40.41.png](attachments/Screen Shot 2018-05-19 at 20.40.41.png) (image/png, 47.9 KB)
- [poc.html](attachments/poc.html) (text/plain, 397 B)
- [Screen Shot 2018-05-21 at 11.14.37 AM.png](attachments/Screen Shot 2018-05-21 at 11.14.37 AM.png) (image/png, 47.0 KB)

## Timeline

### ch...@gmail.com (2018-05-19)

MacOS Sierra 10.12.6.

### mm...@google.com (2018-05-21)

Confirmed, I'be able to reproduce this using the Canary build on Mac.

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox UI>Security>UrlFormatting]

### mm...@google.com (2018-05-21)

Note that on Stable build I'm seeing "spoof" text just for a second or less, that the amazon page starts to load and get rendered.

### sh...@chromium.org (2018-05-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-22)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-05-22)

https://crbug.com/chromium/844881#c3: On Canary, I can only repro this if I opt out of the Site Isolation trial. With SI enabled, the Amazon navigation completes successfully overriding the spoof text. That might just be a matter of timing, since I think the PoC assumes the navigation will take more than one second.

I don't believe this is a regression, but rather a somewhat more convincing example of https://crbug.com/chromium/776402. In that one, it repeatedly navigates between the attacker page and a victim page, causing the spoof page to remain visible but the URL in the omnibox flickers. This is similar, repeatedly navigating to reset the spoof timer, but it goes to a page that responds with an HTTP 204 (No Content), which prevents the URL from updating at all.

Maybe we need to do something like not reset the timer on the navigation in that case?

### sh...@chromium.org (2018-05-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2018-05-23)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-05-25)

My assessment in https://crbug.com/chromium/844881#c6 is wrong, and this might be a regression (although it's hard to test for certain).

The timer is firing for the page but the surface is not getting cleared. There has been a fair amount of refactoring around this code lately, but so far I haven't been able to find any changes that fix the bug when I revert them.

I'm trying to figure out if the surface isn't getting cleared properly, or if maybe the compositor is locked so the frame eviction isn't followed by a commit.

Fady, I wonder if we could figure out if there is a way to write better regression tests for the timeout mechanism. Right now there are some unit tests but nothing that actually verifies there are only white pixels on the screen after the timer fires.

### ch...@gmail.com (2018-05-27)

I can only repro this on Mac. 

### ke...@chromium.org (2018-05-28)

I have been able to repro it on Mac, Linux and Windows. A fix is in progress.

### pa...@chromium.org (2018-06-11)

#12: Any news? :)

### sh...@chromium.org (2018-06-12)

kenrb: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2018-06-12)

I uploaded a fix for this a while ago, but writing a good test to cover it is more difficult and I have been sidetracked by site isolation bugs.

I hope to be getting back to this soon.

https://chromium-review.googlesource.com/c/chromium/src/+/1075512

### ch...@gmail.com (2018-07-13)

Any update on this bug?

### mm...@chromium.org (2018-08-07)

kenrb@, friendly ping from the security sheriff. I see you've mentioned a fix in c#12, did you upload it for a review / landed?

### ke...@chromium.org (2018-08-16)

We think this was likely fixed by r577029, which would be on Canary and Dev channels now.

Unfortunately I haven't been able to immediately verify, because recent releases all seem to complete the navigation to amazon.com when I try the repro case provided. In that case the timer doesn't fire, so we can't observe the changed eviction code.

If anyone is able to verify on Dev or Canary I'd appreciate it -- we would want to see the spoof text appear for ~4 seconds and then disappear. If the Amazon navigation completes then it neither affirms nor refutes that the problem is fixed.

### ch...@gmail.com (2018-08-17)

I'm still able to repro this on Canary 70.0.3525.0 on Mac.

### ke...@chromium.org (2018-08-22)

We really need a way to comprehensively test the timeout behavior. :/

It now appears that the original bug was fixed in r577029, but the behavior was separately regressed by ccameron in r569513.

The spoof text isn't being removed because the timer isn't starting. The timer isn't starting because the top-level RWHV doesn't get a new Surface ID when the Amazon navigation commits, and we return early at https://cs.chromium.org/chromium/src/content/browser/renderer_host/render_widget_host_impl.cc?l=1211&rcl=3ea4abbfded911cb15cc62f93519564983f41faf.

I'm not clear on why that is happening. Possibly because the initial page load is a javascript: URL that doesn't have a navigation commit?

fsamuel and ccameron: I haven't followed all the changes related to surface synchronization. Do either of you have thoughts on the above?

### cc...@chromium.org (2018-08-22)

From the comments in the patch:

The fix is to change RHWI::DidNavigate to only start the timer when
RWHV::DidNavigate changes the surface id. Two reasons:
  - If we didn't change the surface id, it was because this was the
    first navigation, and so we don't need to clear the frame.

So, is that statement about "first navigation" not true?

### ke...@chromium.org (2018-08-22)

That's what I think might be the case. It doesn't appear that loading a javascript: URL causes a navigation commit (which kind of makes sense, since you shouldn't get navigation history from running a bookmarklet, for instance). In this case there is a window.open("javascript://document.write('...')"), so we get a compositor frame from a previously existing document that didn't have a navigation.

Based on that comment I surmise this was an unexpected scenario.

### ch...@gmail.com (2018-08-22)

Kenrb@, it sounds like you can no longer repro this issue on latest Canary?

### ke...@chromium.org (2018-08-23)

I am able to repro this on Mac. The repro case often navigates to amazon.com and then displays the Amazon page, in which case the problem isn't visible. Right now only on Mac with Site Isolation disabled have I been able to make that not happen. As I mentioned, the stale content timer does not start after the Amazon navigation commits, so the spoof text doesn't get cleared.

### bu...@chromium.org (2018-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7da6c3419fd172405bcece1ae4ec6ec8316cd345

commit 7da6c3419fd172405bcece1ae4ec6ec8316cd345
Author: Ken Buchanan <kenrb@chromium.org>
Date: Tue Aug 28 23:05:52 2018

Start rendering timer after first navigation

Currently the new content rendering timer in the browser process,
which clears an old page's contents 4 seconds after a navigation if the
new page doesn't draw in that time, is not set on the first navigation
for a top-level frame.

This is problematic because content can exist before the first
navigation, for instance if it was created by a javascript: URL.

This CL removes the code that skips the timer activation on the first
navigation.

Bug: 844881
Change-Id: I19b3ad1ff62c69ded3a5f7b1c0afde191aaf4584
Reviewed-on: https://chromium-review.googlesource.com/1188589
Reviewed-by: Fady Samuel <fsamuel@chromium.org>
Reviewed-by: ccameron <ccameron@chromium.org>
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#586913}
[modify] https://crrev.com/7da6c3419fd172405bcece1ae4ec6ec8316cd345/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/7da6c3419fd172405bcece1ae4ec6ec8316cd345/content/browser/renderer_host/render_widget_host_view_aura_unittest.cc


### ch...@gmail.com (2018-08-29)

Thanks for the fix :)

### ke...@chromium.org (2018-08-29)

The fix hasn't made it to Canary yet, hopefully it will roll out tomorrow and we can verify it.

### ke...@chromium.org (2018-08-31)

chromium.khalil@: Can you try this out on an updated Canary and see if you can still repro? The behavior looks correct to me right now.

### ch...@gmail.com (2018-08-31)

Double-check.

I’m not able to repro this on thr lastest version of Canary on Mac. Fixed.

### ke...@chromium.org (2018-08-31)

Thanks!

Sorry it took so long to finally resolve this.

### sh...@chromium.org (2018-09-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-11)

Nice spoof! $3,000 for this one!

### mc...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2018-10-26)

Is that a bug in sheriffbot? The fix to this bug doesn't need a merge anywhere.

### aw...@google.com (2018-10-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-08)

This issue was migrated from crbug.com/chromium/844881?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/871844, crbug.com/chromium/893978]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091436)*
