# URL Bar Spoofing using History.back() and History.forward

| Field | Value |
|-------|-------|
| **Issue ID** | [40092028](https://issues.chromium.org/issues/40092028) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | jc...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2011-06-20 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

URL Bar Spoofing using History.back() and History.forward

**VERSION**  

Chrome Version: [12.0.742.100] + [stable, beta, or dev]  

Operating System: [Windows 7]

**REPRODUCTION CASE**  

<https://www.alternativ-testing.fr/Research/Google%20Chrome/Google%20Chrome-Url%20Bar%20Spoof/spoofing.html>

Click on the link , window.open load spoofing.php (page 1) , document.location load spoofing.php (page 2) , reload() => redirect on linkedin.com , history.back() X 2 + history.forward()

Actual Results :  

URL Bar is Spoofed with valid SSL / TLS indicia

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [chrome12spoof.png](attachments/chrome12spoof.png) (image/png; charset=binary, 85.6 KB)
- [ChromeSSLTLSspoof.png](attachments/ChromeSSLTLSspoof.png) (image/png; charset=binary, 68.5 KB)
- [spoofing.php](attachments/spoofing.php) (text/x-php; charset=us-ascii, 3.2 KB)
- [spoofing.html](attachments/spoofing.html) (text/plain; charset=us-ascii, 145 B)
- [spoof-86758-repro.png](attachments/spoof-86758-repro.png) (image/png; charset=binary, 67.6 KB)
- [google spoof6.png](attachments/google spoof6.png) (image/png; charset=binary, 89.7 KB)
- [url-spoof-86758.html](attachments/url-spoof-86758.html) (text/x-c++; charset=us-ascii, 546 B)
- [attacker.html](attachments/attacker.html) (text/plain; charset=us-ascii, 18 B)
- [14.0.835.162.png](attachments/14.0.835.162.png) (image/png; charset=binary, 84.8 KB)

## Timeline

### jc...@gmail.com (2011-06-20)

I've found a way for show the linkedin SSL indicia!

### jc...@gmail.com (2011-06-20)

It's a webkit vulnerability.

### sc...@gmail.com (2011-06-20)

Charlie / Adam, any initial thoughts?
(I'm build sheriff today so I'll triage it tomorrow if no-one else has had a chance to look at it by then)

### ab...@chromium.org (2011-06-20)

The reporter says its an issue in WebKit, but I'd expect the problem to be in the navigation controller, which is a Chrome concept.  We just need to look at it in the debugger to see how we're getting confused.

### js...@chromium.org (2011-06-20)

I can't repro this on stable or canary in Win 7.

### js...@chromium.org (2011-06-20)

Also, from the pictures the spoof appears to be just the SSL state, and not the origin. Given the unreliability and the limited usefulness in an attack I couldn't see this being worse than low severity, assuming we can repro it.

### lc...@gmail.com (2011-06-20)

I couldn't repro either, at first I thought this may be a dupe of 75560.

### jc...@gmail.com (2011-06-20)

I will try to code a better testcase.

### jc...@gmail.com (2011-06-20)

[Comment Deleted]

### jc...@gmail.com (2011-06-20)

[Comment Deleted]

### cr...@chromium.org (2011-06-21)

I haven't been able to reproduce with the link in https://crbug.com/chromium/86758#c10.  The URL bar always reflects the correct page for me.

Tested in Chrome 12 debug (Linux), Chrome 13 (Mac, Linux), Chrome 14 (Mac, Linux, Windows).

### jc...@gmail.com (2011-06-21)

[Comment Deleted]

### jc...@gmail.com (2011-06-21)

[Comment Deleted]

### jc...@gmail.com (2011-06-21)

I will try with Chrome 14

### jc...@gmail.com (2011-06-21)

My PoC works with Chrome 14.0.794.0 on Windows 7.

### jc...@gmail.com (2011-06-21)

If the spoofing don't work the first time, please retry .

### jc...@gmail.com (2011-06-21)

I think know how the Testcase don't work with you.

Test with spoofing.html like :
<a href="javascript:spoof();">Click Me</a> 
<script> 
var a=null;
function spoof() {
  a = window.open('./spoofing.php')
}
</script> 

When Linkedin.com is loaded , use Back(), and the spoofing works !

### jc...@gmail.com (2011-06-21)

This Testcase Works very well ! ( A small error in the last PoC )

Please use this Testcase , Back() when Linkedin.com is loaded and it works ! 

### cr...@chromium.org (2011-06-21)

I think was able to reproduce in Chrome 14.  The important step for me was using "javascript:history.back()" to go back from LinkedIn, and not the back button.  Even then, it's not consistent-- sometimes I get the spoofing.php URL in the location bar, and sometimes I get the LinkedIn URL.

All the times I've observed the bug, the SSL state is not spoofed.  As seen in my attached screenshot, it looks like I'm on the spoofing.php URL, though LinkedIn's page is still showing.  If there's a way to spoof the SSL state, I haven't seen it yet.  Do you have any steps for reproducing that?

### js...@chromium.org (2011-06-22)

So, you were able to get the target pages's content to show with the attacker's URL? Did you ever get it the other way (attacker's page for target URL)? If not, it's not a viable spoof (even though it's definitely a bug).

### jc...@gmail.com (2011-06-22)

I will try it.

### jc...@gmail.com (2011-06-24)

I've found a way for spoof the SSL/TLS and the Page content ! ! ! (view screenshot)

I will try to code a perfect testcase!

### cr...@chromium.org (2011-06-24)

Thanks-- another testcase or a set of repro steps for getting to that state would help.

I've been investigating the problem, and I've found there are two ASSERTs failing in debug builds.  The first is in WebKit's HistoryController.  After going back from LinkedIn, the spoofing.php page triggers a forward navigation and then interrupts it with a same-document fragment navigation.  There's a bug where HistoryController::recursiveUpdateForSameDocumentNavigation commits the provisional item (i.e., LinkedIn) during the fragment navigation.  Also, we aren't stopping the LinkedIn navigation, so when it does commit, there's no provisional item left and we fail an ASSERT in HistoryController::updateForCommit.

If I put in a workaround for that, we still get a second debug crash in Chrome's NavigationController.  Turns out we get a FrameNavigate message for the LinkedIn page, but Chrome somehow has no NavigationEntry for this, so it crashes in ClassifyNavigation (or ignores the navigation in a release build).  Ignoring the navigation is probably what leads to the URL spoof.

I'll have to figure out why Chrome doesn't have an entry for LinkedIn but WebKit does.  I'll file a WebKit bug next week for the HistoryController behavior as well. 

### jc...@gmail.com (2011-06-25)

Like https://crbug.com/chromium/77786 and https://crbug.com/chromium/54262 the SecSeverity of this bug can be high.

I think coded a perfect or more evident testcase soon.

### [Deleted User] (2011-06-27)

The spoof will show the address of the attacking server with the content of a trusted server so I don't see this being more than low severity.

### [Deleted User] (2011-06-27)

[Empty comment from Monorail migration]

### cr...@chromium.org (2011-06-27)

I agree with cdn@ in https://crbug.com/chromium/86758#c25 about the severity unless we're able to find the steps to reproduce the screenshot from https://crbug.com/chromium/86758#c22.  That shows attacker-controlled content with a victim URL.  I still haven't observed that in practice, though.

### jc...@gmail.com (2011-06-28)

wait... I code a better testcase soon for show the https://crbug.com/chromium/86758#c22 result.

### ma...@google.com (2011-06-28)

[Empty comment from Monorail migration]

### cr...@chromium.org (2011-06-29)

It took a while to get to the root cause, but it turns out this is fairly serious.  We have a race condition with history.back() and history.forward() that makes it possible to interrupt them and cause NavigationController to ignore the final commit.

I've coded and attached a much simpler test case that shows an attacker could use this to display content on a URL of his choice.  I'm upgrading the severity to high as a result.  (Security folks, feel free to adjust that as appropriate.)

The basic steps are as follows:
1) Attacker opens a window to victim.com.
2) Attacker navigates it to attacker.com.
3) Attacker runs history.back() and waits for the window to get back to victim.com.
4) Attacker runs history.forward() and immediately follows with document.location="victim.com#foo".

We end up showing attacker.com in the tab, with the URL showing victim.com#foo.

The problem is that a history.forward() navigation starts out as a navigation to chrome-back-forward://go/1 in the renderer process, which gets aborted and asynchronously sent over to the browser process.  The browser process later tells the renderer to go to the corresponding (serialized) history item.

However, the renderer has time to complete a full new navigation (e.g., to a fragment) after aborting the chrome-back-forward://go/1 navigation and before hearing back from the browser.  This means it will send a FrameNavigate message for the fragment navigation (at which point NavigationController crops off the forward history), and then it will do the requested forward navigation.  That FrameNavigate message then gets ignored by NavigationController because it has a page ID the browser has forgotten about.  (See the NOTREACHED line in NavigationController::ClassifyNavigation.)

Brett, I'm CC'ing you as a heads up while I try to figure out the right fix.  We may want to find a way to cancel the forward navigation if it has been interrupted, though that may not be easy.  (Maybe RenderView can keep track of it as state?)  I don't think we want to just accept the forward navigation, because the rest of the cropped back/forward history is gone at this point.

### cr...@chromium.org (2011-06-30)

This one is looking non-trivial to fix.  We want to ignore any navigation message from the browser process with a stale HistoryItem, but the renderer doesn't have any list of the current HistoryItems.

RenderView is keeping track of the current history length (or at least, the last length it's heard from the browser), history offset, and the page ID of the current item.  I don't think that's sufficient to fix this-- we could notice if the requested HistoryItem matches the current offset but has a stale page ID, and we could notice if its offset is beyond what we currently think the length is, but we wouldn't notice a problem if the renderer is able to commit multiple navigations before hearing from the browser.

I think we can make it work if the renderer keeps track of a list of page IDs of the same length as the history, rather than just the history length and current page ID.  (We can use -1 for any entries in the list that were rendered by a different process.)  This will let us immediately tell whether any requested navigation is for a stale page ID or an offset that no longer exists, due to a navigation the browser hadn't heard about yet.

I haven't tried implementing this yet, but I think we'll be able to update the state sufficiently in the renderer, since it should always know about all of its own page IDs without having to wait to hear from the browser.

### jc...@gmail.com (2011-07-01)

@creis : thanks for the simpler test !

### cr...@chromium.org (2011-07-07)

Sorry for the delay on this-- there were two additional subtle bugs that were leading to the same crash/spoof, even if the issue described in https://crbug.com/chromium/86758#c31 was fixed.  Turns out there's lots of chances for the renderer and browser to get out of sync with a stale back/forward navigation.  :-/

One bug comes up if the fragment navigation happens after we've started the forward navigation.  In that case, RenderView won't ignore the forward, so FrameLoader needs to abort it (by calling StopAllLoaders) when it decides to do the fragment navigation instead.  That means I'll need a WebKit patch in addition to the Chrome CL.

The other bug happens if a fragment navigation occurs before the original page finishes loading.  In that case, the browser crops the forward history but the renderer doesn't.  As a result, RenderView doesn't realize a forward navigation is stale and lets it through, leading to the same URL spoof.  Instead, NavigationController should be updated to not crop the forward history if an in-page navigation has the same page ID.

I have working fixes for all three issues and I'm putting together tests.  Hoping to send them for review soon.

### cr...@chromium.org (2011-07-09)

The Chrome fixes to RenderView and NavigationController are ready to go:
http://codereview.chromium.org/7327014/

Just putting together the corresponding WebKit patch for FrameLoader, which I should have ready early next week.

### sc...@gmail.com (2011-07-15)

How's this one going?

### cr...@chromium.org (2011-07-15)

The Chrome CL is ready to land, but I want to land the WebKit patch first (or else there will still be a spoof/DCHECK possible).

WebKit patch in progress:
https://bugs.webkit.org/show_bug.cgi?id=64556

I'm trying to figure out why it's causing a crash in an existing layout test at the moment.

### cr...@chromium.org (2011-07-15)

On second thought, I think I'm going to go ahead and land the Chrome CL as a first step.  I'm still trying to get the WebKit patch finished and there will still be a URL spoof possible in the mean time, but this will at least close down one of the ways it's happening and shouldn't make anything worse.

The Chrome part of the fix should also resolve https://crbug.com/chromium/75163, so that's worthwhile to have in place.

### cr...@chromium.org (2011-07-18)

I've landed half of this fix in http://src.chromium.org/viewvc/chrome?view=rev&revision=92748.  That eliminates some but not all of the ways this spoof can happen.

Still working on the WebKit half (https://bugs.webkit.org/show_bug.cgi?id=64556).

### cr...@chromium.org (2011-07-25)

I've just landed a second line of defense for this:
http://src.chromium.org/viewvc/chrome?view=rev&revision=93828

We'll now terminate a renderer process if it navigates to an "existing" entry the browser process no longer knows about, rather than ignoring the navigation (which is how this spoof happened).  As a result, the remaining WebKit issue is no longer a security threat-- it will just result in a sad tab.

I still have the WebKit issue on my plate and will continue trying to fix it, but it's no longer blocking this security bug.  Marking this fixed.

### sc...@gmail.com (2011-07-25)

Thanks Charlie, and thanks for the defense-in-depth.
Good timing, also. This fix will make the Chrome 14 branch point (today), so this issue will be fixed when Chrome 14 goes to stable.

### jc...@gmail.com (2011-07-30)

Google Chrome 14.0.835.8 crash with the testcase.

### cr...@chromium.org (2011-08-01)

It's a sad tab and not a full browser crash, correct?  That's intentional, as described in https://crbug.com/chromium/86758#c39.  We'll still follow up and fix WebKit https://crbug.com/chromium/64556, but it's not security sensitive anymore.

### jc...@gmail.com (2011-08-05)

Yes correct :)

### da...@chromium.org (2011-08-05)

The fix to this bug seems to have caused a pretty major "back"-navigation regression:
http://code.google.com/p/chromium/issues/detail?id=89798

The regression only happens when a page is prerendered.

### da...@chromium.org (2011-08-07)

[Empty comment from Monorail migration]

### cb...@chromium.org (2011-08-07)

This also happens for "instant" for similar reasons as the prerender case. See https://crbug.com/chromium/89798 for more details.

### sc...@gmail.com (2011-08-24)

Thanks for your help and enthusiasm on this bug, Jordi. It really helped Charlie get to the bottom of this. Definitely good for a provisional $500 Chromium Security Reward.

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

### jc...@gmail.com (2011-08-27)

Thank you very much for this Reward !

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### jc...@gmail.com (2011-09-12)

Excuse me but 14.0.835.162 beta don't fixes this issue (Tested on windows 7).

### sc...@gmail.com (2011-09-12)

@jordi: yes, well spotted sir! You have eagle eyes.
We had to revert the patch for now because it caused a regression.
The regression has been fixed and we will make sure to ship the patch in a Chrome 14 patch, or Chrome 15.
The reward, of course, is unaffected :)

### mi...@chromium.org (2011-09-16)

The fix has landed upstream at http://trac.webkit.org/changeset/95259. It looks like the revert (r100049) for Charlie's change to kill the renderer only landed on the 835 branch. I assume the plan of action is:
1. Let the fix get rolled into a few canary builds to make sure it's stable and actually fixes the problem
2. If it looks good, merge the fix into the M15 (874) branch
3. If it looks good there, revert the revert (r100049) in the M14 (835) branch and merge the fix in

We could presumably revert r100049 now since the cause of too many renderers getting killed was fixed, but I'll leave that up the security people and release driver.

### sc...@gmail.com (2011-09-16)

Yep, we'll target re-enabling Charlie's renderer killer in the M14 security patch if all else looks good on M15.

### in...@chromium.org (2011-09-19)

Do we want to merge this to m15, we have time till 7 pm today for merging this.

### in...@chromium.org (2011-09-19)

merged to m15 in r95473.

### ke...@chromium.org (2011-09-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-26)

Not merging to m14 because looks a little risky after discussion.

### sc...@gmail.com (2011-10-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### jc...@gmail.com (2011-10-12)

[Comment Deleted]

### jc...@gmail.com (2011-10-12)

[Comment Deleted]

### jc...@gmail.com (2011-10-12)

[Comment Deleted]

### js...@chromium.org (2011-10-12)

Jordi, not all changes have or can be merged to the beta (as is evident from the comments in the respective bugs). As such, your attempts to test against beta are simply producing correct results. Now, please stop spamming this tracker and being generally disruptive.

### jc...@gmail.com (2011-10-13)

sorry for the inconvenience ...

### jc...@gmail.com (2011-10-27)

I would like thank Google for this reward !
Thank you very much!

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5cad491f0f70c951e42823affb83140d05709adf

commit 5cad491f0f70c951e42823affb83140d05709adf
Author: avi <avi@chromium.org>
Date: Fri Jun 19 05:25:44 2015

Rather than dropping stale navigations, resurrect the navigation entry that they were going to.

This reverts r307614 (which drops navigations) and solves the problem with resurrection.

BUG=501515, 458361, 500576, 86758, 102408, 145969
TEST=covered by tests, as well as it shouldn't regress the original https://crbug.com/chromium/86758

Review URL: https://codereview.chromium.org/1183143006

Cr-Commit-Position: refs/heads/master@{#335212}

[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/browser/frame_host/navigation_controller_impl.cc
[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/browser/frame_host/navigation_controller_impl_unittest.cc
[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/common/view_messages.h
[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/renderer/render_frame_impl.cc
[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/renderer/render_frame_impl.h
[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/renderer/render_thread_impl.cc
[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/renderer/render_thread_impl.h
[modify] http://crrev.com/5cad491f0f70c951e42823affb83140d05709adf/content/renderer/render_view_browsertest.cc


### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/86758?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/96932]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092028)*
