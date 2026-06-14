# URL Spoof due to subframes and NavigationEntry corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40084699](https://issues.chromium.org/issues/40084699) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Reporter** | wa...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2016-06-25 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36

Steps to reproduce the problem:
Open the attached HTML file in localhost: http://localhost/attack.html

Steps to reproduce the Spoof:

1-click on the "Attack step 1" button. This step creates a chain of iframes
2-wait till google (the URL to spoof) opens
3-navigate back 1 time
4-click on the "Attack step 2" button
5-click on the "Attack step 3" button
6-navigate back 1 time
7-click on the "Attack step 4" button
8-navigate back 1 time
9-click on the "Attack step 5" button 
10-click on the "Attack step 6" button => spoof

What is the expected behavior?
The URL of the attack.html page should remain locahost/attack.html

What went wrong?
Another URL was shown instead of the attacker's URL. Also, it works with HTTPS wesites. 

Did this work before? N/A 

Chrome version: 51.0.2704.103  Channel: n/a
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 22.0 r0

Since this attack requires the interaction of the victim to succeed, it is using the following social engineering:

It redirects the victim to a URL (the URL that will be spoofed), making it seem like redirecting to a download link, and instructing the victim to navigate back if she sees a dead link.

All the steps, except steps 3,6 and 8, can be done automatically by the attacker, without the interaction of the victim.

## Attachments

- [attack.html](attachments/attack.html) (text/plain, 1.7 KB)
- [opener.html](attachments/opener.html) (text/plain, 533 B)
- [page1.html](attachments/page1.html) (text/plain, 1.6 KB)
- [page2.html](attachments/page2.html) (text/plain, 396 B)

## Timeline

### do...@chromium.org (2016-06-27)

Thanks for your report.

I can reproduce this on Mac on 51.0.2704.103, but it does not reproduce on Canary (the last step does not seem to result in a spoof - it actually navigates to www.google.com/file_blabla).

It's possible that this issue is already fixed. Can you check this in Chrome Canary?

[Monorail components: Security>UX]

### wa...@gmail.com (2016-06-28)

I tried the same attack on 51.0.2704.106 m (windows 7) and it succeeded.


### sh...@chromium.org (2016-06-29)

Thank you for providing more feedback. Adding requester "dominickn@chromium.org" for another review and adding "Needs-Review" label for tracking.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2016-06-29)

Can you try the attack on Chrome Canary (https://www.google.com/chrome/browser/canary.html)? Chrome 51 is Stable; Canary is the nightly build of the most recent version of the source code. We think perhaps the bug has been fixed. Thank you!

### pa...@chromium.org (2016-06-30)

+ Site Isolation folks as navigation experts. 

[Monorail components: UI>Browser>Navigation]

### wa...@gmail.com (2016-06-30)

I tested the attack on Canary and windows 7, it doesn't work anymore.
In versions 51 and canary, "attack step 3" behaves differently. In version 51 the iframe is removed before the "alert" is executed, whereas in canary the iframe is removed after its execution.

I think that the attack might still be possible if there is a way to remove the iframe before the execution of the "alert". 

### na...@chromium.org (2016-07-01)

I did some bisecting to see what has changed through time. There are two changes that impact this after stable:

* A fix by creis@ (https://crrev.com/392666) which actually prevents the spoof and kills the renderer process attempting it.

* A change by changwan@ (https://crrev.com/394883) which removes the nested message loop in JS dialogs. This results in the change of behavior seen with iframe being removed while the dialog is up or not.

I'll poke a bit more to see what exactly is the sequence of IPCs that lead to the spoof, as there might be a variation still possible.

### na...@chromium.org (2016-07-01)

wadih.matar@, have you been able to reproduce this with a site different than eurosport.fr? I'm trying to minimize the repro steps, but replacing eurosport.fr with any other simpler site (whether it has iframes or not) does not seem to work. On the back navigation in 3 (back from the chain of iframe navigations), without eurosport.fr I get the actual page loaded in the iframe, otherwise we load about:blank.

### wa...@gmail.com (2016-07-02)

[Comment Deleted]

### wa...@gmail.com (2016-07-02)

Yes it works with other websites. You can try this code in the createiframeschain() function:

var v=document.getElementById('1');
v.src='http://planetf1.com';

and leave the rest of the function like it is. The attack will work and https://www.google.com/file_blabla will be spoofed.

There is a way to see that the corruption is created without requiring "about:blank" to replace another address in the iframe, and that the "about:blank" iframe bug is just a way to achieve exploitation.

Replace the code of the createiframeschain() function with the following:


var v=document.getElementById('1');
//I think any address will work here
v.src='http://localhost';

setTimeout(function(){ v.src='https://fr.wikipedia.org';}, 4000);

setTimeout(function(){ v.src='http://localhost';}, 8000);

setTimeout(function(){ v.src='https://fr.wikipedia.org';}, 12000);

setTimeout(function(){ v.src='http://localhost';}, 16000);

//https://www.google.com instead of https://www.google.com/file_blabla. 
setTimeout(function(){ window.location="https://www.google.com"}, 20000);


After completing the attack (see steps in https://crbug.com/chromium/623319#c0), there will be 2 https://www.google.com pages in the navigation chain. in the first one, execute in the URL: javascript:window.history.forward();window.history.forward();
There will be a spoof and no "about:blank" iframe was loaded in the iframe. 
This will not work with https://www.google.com/file_blabla instead of https://www.google.com.


I think this shows that the "about:blank" iframes replacing other addresses is not the cause of the corruption, it is just used for the exploitation to work. It also shows that the corruption might be related to the caching since there is a difference in behavior between https://www.google.com/file_blabla (404) and https://www.google.com.


### wa...@gmail.com (2016-07-05)

There might be a way to succeed this attack without the victim's interaction, increasing its severity. I think window.open() can make this possible. I am working on it.

### wa...@gmail.com (2016-07-05)

This variant of the attack is more dangerous (doesn't require the victim's interaction).

Demo (tested on version 51):

*open http://localhost/opener.html
*click on the steps shown in the pages

NOTE: It seems that this attack can only spoof pages containing an iframe.

### cr...@chromium.org (2016-07-06)

Nasko and I looked through the original attack on Friday, and I'm helping to investigate while he's out of town.  Some of our findings are below.

To recap what was stated earlier, this only affects M51.  In M52, it's blocked by the NC_AUTO_SUBFRAME kill (added in r392666, 52.0.2733.0) and the removal of a nested message loop for alert (r394883, 52.0.2743.0).  We could consider merging r392666 to M51 as a defense if needed.

It's possible to continue investigating it on trunk if you revert both of those CLs, which is worthwhile for understanding the history corruption bugs that made the spoof possible.  (These two CLs don't fix the underlying problems, but they do disrupt the attack.)  In particular, I'm hopeful that this will shed some light on https://crbug.com/chromium/613732, where we're seeing other NC_AUTO_SUBFRAME kills in practice.

A few observations from the original version of attack.html:

Attack step 1:
 - Make sure that each iframe has time to complete loading before doing each navigation.  I had to extend this to 7 seconds each for debug builds.
 - When the user goes back from the 404 page to attack.html, we end up loading about:blank in the iframe instead of Eurosport.  This is because the earlier loads of Eurosport change window.name of the iframe, which breaks back/forward navigation in iframes (see https://crbug.com/chromium/607205).  I'm not sure yet if this is a necessary part of the attack.

Attack step 2:
 - When going back, we keep the iframe on about:blank for the same reason as above.  (This actually triggers a main frame reload as well since HistoryController falls back to loading the main frame if no frames look like they need to change.  That's probably not important for the attack.)

Attack step 3:
 - The combination of removing the iframe, going forward twice, and showing an alert (with a nested message loop) somehow has the effect of clearing the nav_entry_id (and likely the rest of the pending_navigation_params_) in the renderer process.  This results in a commit of the Google 404 page with nav_entry_id 0 and did_create_new_entry=false, which makes NavigationControllerImpl::RendererDidNavigateToExistingPage incorrectly consider it a replaceState, reload, or client-side redirect.  As a result, we apply the change to the last committed NavigationEntry rather than the intended entry.
 - As far as I can tell, this doesn't yet create enough corruption for the attack, because the NavigationEntry has the Google 404 page in both GetURL() and GetPageState().  It's a bug we should fix, but it doesn't seem too bad yet.
 - The user now goes back again from the 404 page to attack.html.

Attack step 4:
 - Interestingly, this appears to be where the real damage occurs.  Despite being identical to step 5 (i.e., just going forward twice), steps 4 and 5 cause different results.
 - In step 4, we first see a subframe commit for about:blank, as if we've skipped the first forward() and committed the second forward().
 - Strangely, we later see a commit for the Google 404 page's URL, with PageState from attack.html (!).  This is the critical part of the attack, which gives the NavigationEntry inconsistent data in GetURL() and GetPageState().  I'm not yet sure why this is happening.

Here, it turns out steps 5 and 6 are unnecessary.  After step 4, you can just go forward once to cause the spoof to occur.  (No need to go forward twice and back once.)

I'll continue investigating steps 3 and 4 and trying to boil them down into a minimal repro.

### cr...@chromium.org (2016-07-07)

Good news!  I've narrowed this down into two independent bugs.  Only step 4 is needed for the spoof.

--- Bug from Step 3 ---

Step 3 is unnecessary for the spoof and can be split out.  It causes a back/forward entry to be committed in place of the current entry, which is wrong but apparently not dangerous.  (There's no URL/PageState mismatch, which is needed for this type of spoof.)  It happens because we have a ScopedPageLoadDeferrer during nested message loops, and that defers the session history navigation until later, after the pending_navigation_params_ in RenderFrameImpl have been reset.  As a result, we don't remember the nav_entry_id when the deferred navigation commits, so it commits in place of the current entry.

While we don't use a nested message loop for alerts anymore, we do still use one for other things, like window.print().  That means it's still a problem.  Also, it looks like removing the iframe and doing the two consecutive forward navigations is unnecessary for this, so step 3 can be simplified to just "history.go(2); print();".

I'll file this part as a separate non-security issue with the following repro steps:
1) Visit https://csreis.github.io/tests
2) Click "simple.html"
3) Go back.
4) In DevTools: history.forward();print();
5) Cancel printing.

Now both navigation entries point to simple.html.


--- Bug from Step 4 ---

The key problem here is that HistoryController::UpdateForCommit has an early return for back/forward navigations if there is no provisional_entry_.  That almost guarantees a mismatch between the URL and PageState in the NavigationEntry if we trigger that condition.

We get to it with the consecutive history.forward() calls because the first call is for the main frame and the second call is (only) for the iframe.  The second one must have the same item sequence number for the main frame as the current page for that to happen.  Step 3 sets that up, but so would location.replace (as shown in the simpler repro steps below).

The interesting thing is that the second history.forward() doesn't cancel the first history.forward(), because they target different frames.  However, the second history.forward() replaces the provisional_entry_ of the first history.forward() in HistoryController (and commits its own, since it also happens to be faster).  That means that when the first history.forward() for the main frame commits at a later time, there's no provisional_entry_ to commit.

As a result, the DidCommitProvisionalLoad IPC message sends the Google 404 page as the URL, but HistoryController::GetCurrentEntry() is stale and gives us the PageState of the attack.html page.  With this mismatch in place, it's easy to go back and then forward again to get a URL spoof in M51 or a NC_AUTO_SUBFRAME kill in M52.

Simpler repro steps for this bug:
1) Visit http://csreis.github.io/tests/cross-site-iframe.html
2) In DevTools (top frame): navFrame("simple.html");
3) In DevTools: navFrame("about:blank");
4) Go back.
5) In DevTools: location.replace("https://www.chromium.org");
6) Go back.
7) In DevTools: history.forward();history.forward();
   (Should be on chromium.org now.)
8) Go back.
9) Go forward.

Note that this likely explains all the NC_AUTO_SUBFRAME kills we're seeing in https://crbug.com/chromium/613732 as well.

I'll need to think about how to fix this one, and whether we can just stop all frame loads when another one comes in.  Also, this bug doesn't repro in the new navigation path (https://crbug.com/chromium/236848), which we're close to turning on.  We'll still want to fix this for the branches, though.

### cr...@chromium.org (2016-07-08)

A fix is up for review: https://codereview.chromium.org/2134493002/

It should be enough to avoid URL spoofs, while staying easy to merge.  It leaves some subframe cases unaddressed, but those are lower impact and will go away with the new FrameNavigationEntry path that we're switching to in M54.

### cr...@chromium.org (2016-07-08)

Filed https://crbug.com/chromium/626838 for the first bug in https://crbug.com/chromium/623319#c14.  That one isn't security, so we don't need to mark it as blocking this one or restrict it.

### bu...@chromium.org (2016-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ab22bdfc5cb681f2f4dc789171e97618a9657486

commit ab22bdfc5cb681f2f4dc789171e97618a9657486
Author: creis <creis@chromium.org>
Date: Fri Jul 08 23:51:46 2016

Update HistoryController::current_entry_ on all main frame back/forwards.

This fixes a case where it was left stale on a cross-origin commit
because the provisional_entry_ had been cleared by a different commit.

BUG=623319
TEST=See bug https://crbug.com/chromium/623319#c14 for repro steps.
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2134493002
Cr-Commit-Position: refs/heads/master@{#404537}

[modify] https://crrev.com/ab22bdfc5cb681f2f4dc789171e97618a9657486/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/ab22bdfc5cb681f2f4dc789171e97618a9657486/content/renderer/history_controller.cc


### wa...@gmail.com (2016-07-11)

https://crbug.com/chromium/623319#c12 shows a variant of the attack which requires no user interaction and can spoof HTTPS pages. To be consistent with other bug reports, i think that the security severity should be high.

### cr...@chromium.org (2016-07-11)

https://crbug.com/chromium/623319#c18: Yes, I'm taking a closer look at that one now.  It does have an interesting extra building block, when the victim page has an iframe.  That does some unexpected things with which entry is the last committed, which no longer looks equivalent to location.replace.  I'm trying to boil it down to a simpler set of repro steps, but it does look like the attack can be fully scripted.

I'm a bit torn about how to rate this.  There are two mitigating factors, but neither seems to offer much protection:
1) It only works if the victim URL has iframes.  That said, it's not hard to find a victim page with iframes.
2) It does still require the user to dismiss the alert dialog (or print dialog).  The user will naturally do this, though.  It's not as much of a mitigation as requiring them to go back.
Despite the fact that "Medium severity" include "An address bar spoof where only certain URLs can be displayed, or with other mitigating factors" as an example, I think the class of URLs that have iframes is broad enough to consider this a High severity bug.

I'll also note that the pages provided in https://crbug.com/chromium/623319#c12 do require the user to click through everything, but I think I see how to piece it all together with some careful timing and perhaps some polling from the opener window.

Another interesting observation about that version of the attack: it continues to hit the NC_AUTO_SUBFRAME renderer kill on 54.0.2793.0 (at least, when I replace alert() with print()).  That's great, because I was surprised to see that we still are getting lots of NC_AUTO_SUBFRAME reports after 54.0.2792.0, when r404537 landed.  I should be able to work out the additional repro steps to come up with a second fix.

### cr...@chromium.org (2016-07-11)

Simplified repro steps for the attack in https://crbug.com/chromium/623319#c12:

0) Start Chrome with --force-fieldtrials='SiteIsolationExtensions/Control' (to make sure we're using the old navigation path on Canary).
1) Visit http://csreis.github.io/tests/window-open.html and click "Open named about:blank window."
2) In top frame of DevTools of opener window: w.location.href = "cross-site-iframe.html"
3) w.navFrame("simple.html")
4) w.navFrame("about:blank")
5) w.location.href = "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe"
6) w.location.href = "simple.html"
7) w.history.go(-3);
8) f = w.document.querySelectorAll("iframe")[0]; f.parentNode.removeChild(f);
9) w.history.forward(); w.history.forward(); w.print();   
   (then switch to the popup tab, cancel the print dialog, and switch back)
10) w.location.href = "simple.html"
11) w.history.go(-4);
12) w.history.forward(); w.history.forward();
13) w.location.href = "simple.html"
14) w.history.back()
15) w.history.back()

These steps cause a URL spoof on M51, and they cause a NC_AUTO_SUBFRAME renderer kill in step 12 on M52 and M53, including 54.0.2793.0 with my first fix (r404537).  (In M51, there's a reverse URL spoof in step 12, where the attacker's URL is shown over the victim's content.  Steps 13-15 set up the actual spoof.)

It's interesting to note that step 8 (removing the iframe) is necessary in this version, unlike in the version in https://crbug.com/chromium/623319#c14.  I'm working through a few remaining open questions about why it works, and then I'll post an explanation.

### sh...@chromium.org (2016-07-12)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-07-12)

Ok, I think I have a better understanding now.  The key is having an iframe on the victim page, which inherits some stale state and leads to the spoof.

More specific explanations:

The frame removal in step 8 of https://crbug.com/chromium/623319#c20 is unnecessary.  It only prevents the first (subframe) history.forward() in step 9 from winning the race with the second history.forward() (main frame, targeting the Mozilla page), by causing the navigation to target the main frame instead of the subframe.  When we delete the frame, both forward navigations target the main frame, and the second one cancels the first one.  We can simplify this by replacing steps 8 and 9 with "w.history.go(2); w.print();".

From there, we commit the Mozilla page over the current NavigationEntry (due to the ScopedPageLoadDeferrer bug in https://crbug.com/chromium/626838, which caused the main frame's nav_entry_id to be 0).  The interesting part is that the Mozilla page's iframes inherit the pending NavigationParams that were stored on HistoryController despite the ScopedPageLoadDeferrer.  That means the iframe commits actually have the right nav_entry_id and target the original entry, which is why we end up on the second-to-last entry rather than the one was just corrupted.  This makes the attack fully automatable, since we can navigate to simple.html without breaking the cross-site-iframe.html "bookends" on either side of the corrupted entry:
[ (csi, initial), (moz), (csi, blank), *(moz), (simple) ]

In step 12, we do a forward navigation to the Mozilla page, and then a forward navigation in the subframe.  This is a race, and there's an interesting bug in HistoryController::UpdateForCommit if the Mozilla page commits first.  The provisional entry is for the cross-site-iframe / about:blank page, and we'll commit it and overwrite the main frame with the Mozilla URL.  However, we'll leave the about:blank HistoryItem in place for the iframe, which means we'll end up incorrectly loading about:blank into one of the iframes of the Mozilla page.  That's ugly, but it doesn't create a URL spoof.  It also doesn't happen if the race goes the other way and the iframe commits first.

The more important bug happens no matter which navigation wins the race.  The pending NavigationParams on HistoryController (mentioned above) point to the cross-site-iframe / about:blank page, and they don't get cleared until some future back/forward navigation.  As a result, the Mozilla page's iframes will inherit the nav_entry_id from these stale NavigationParams, and will try to commit to the cross-site-iframe / about:blank's NavigationEntry.  That causes the URL spoof (in M51) or NC_AUTO_SUBFRAME kill (in M52 and later), since we're doing a subframe navigation that targets an entry with a cross-site main frame URL.

We should be clearing these NavigationParams from HistoryController between navigations so that they don't get used by iframes in an unrelated navigation.  (I bet there's lots of ways to hit this case, which may explain why we see so many NC_AUTO_SUBFRAME kills.)

### bu...@chromium.org (2016-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4d78d33cb1852e7d487f1d327517c4c4044a3ca3

commit 4d78d33cb1852e7d487f1d327517c4c4044a3ca3
Author: creis <creis@chromium.org>
Date: Wed Jul 13 01:12:49 2016

Clear stale NavigationParams from HistoryController.

This prevents newly created iframes during a back/forward from
targeting the wrong NavigationEntry.

BUG=623319
TEST=See bug https://crbug.com/chromium/623319#c20 for repro steps.
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2144823002
Cr-Commit-Position: refs/heads/master@{#404870}

[modify] https://crrev.com/4d78d33cb1852e7d487f1d327517c4c4044a3ca3/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/4d78d33cb1852e7d487f1d327517c4c4044a3ca3/content/renderer/history_controller.cc
[modify] https://crrev.com/4d78d33cb1852e7d487f1d327517c4c4044a3ca3/content/renderer/history_controller.h


### cr...@chromium.org (2016-07-13)

I'm hopeful that r404870 should fix this.  I'm mainly waiting for the 54.0.2795.0 canary to ship so I can verify it.  Doesn't look like it has shipped yet.

### cr...@chromium.org (2016-07-14)

The attack in https://crbug.com/chromium/623319#c12 and the repro steps in https://crbug.com/chromium/623319#c20 look fixed in 54.0.2795.0.  (That's including the variant of https://crbug.com/chromium/623319#c12 that uses print() instead of alert().)  

I'll consider this fixed, and we should merge both r404537 and r404870 to the branches to prevent NC_AUTO_SUBFRAME kills there.  I'm assuming it's too late for M51, since M52 is about to go stable.

Side note: There are sadly still a few NC_AUTO_SUBFRAME kills in 54.0.2796.2, so some other variant of this may still be possible.  That said, it won't be a URL spoof as of M52, and it will go away when we switch to the new navigation path.  If anyone can find repro steps in 54.0.2796.2 or later, though, I'd be very interested.

### go...@chromium.org (2016-07-14)

+ awhalley@ (Chrome Desktop Security TPM) to make a call whether we need to get both r404537 and r404870 merges in for M52 and M53.

### cr...@chromium.org (2016-07-14)

https://crbug.com/chromium/623319#c26: To be clear, the reason to merge these CLs to M52 and M53 is to reduce the number of NC_AUTO_SUBFRAME renderer kills in https://crbug.com/chromium/613732 (ReleaseBlock-Stable).  They are not security fixes for M52 and M53, though they do fix some ugly behavior beyond just the renderer kills.

They would be security fixes for M51 if we wanted to merge there, but I'm guessing it's too late.

### go...@chromium.org (2016-07-14)

Ok, got it. Thank you for the clarification. Just wanted to double check r404537 and r404870 both merges are safe, correct?


And Yeah, it is too late for M51.



### cr...@chromium.org (2016-07-14)

I'm 100% confident on r404537 being safe, and probably 95% confident on r404870.  (There's a small risk around forgetting subframe URLs on back/forward if something went wrong in the check, but we have some test coverage for that so I'm not concerned.)

### go...@chromium.org (2016-07-14)

r404537 and r404870 - Approving merges to M53 branch 2785 and M52 branch 2743 based on https://crbug.com/chromium/623319#c27, #29 in this bug and https://bugs.chromium.org/p/chromium/issues/detail?id=613732#c39. Please merge ASAP. Thank you.



### bu...@chromium.org (2016-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/117fc6cce4a3fd99f22a7351b19e094b6e64cba1

commit 117fc6cce4a3fd99f22a7351b19e094b6e64cba1
Author: Charles Reis <creis@chromium.org>
Date: Thu Jul 14 20:36:44 2016

Update HistoryController::current_entry_ on all main frame back/forwards.

This fixes a case where it was left stale on a cross-origin commit
because the provisional_entry_ had been cleared by a different commit.

BUG=623319
TEST=See bug https://crbug.com/chromium/623319#c14 for repro steps.
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2134493002
Cr-Commit-Position: refs/heads/master@{#404537}
(cherry picked from commit ab22bdfc5cb681f2f4dc789171e97618a9657486)

Review URL: https://codereview.chromium.org/2150073002 .

Cr-Commit-Position: refs/branch-heads/2785@{#124}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/117fc6cce4a3fd99f22a7351b19e094b6e64cba1/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/117fc6cce4a3fd99f22a7351b19e094b6e64cba1/content/renderer/history_controller.cc


### bu...@chromium.org (2016-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/853590fad2f104bd6b922dcdbaa3b3672a1fafe5

commit 853590fad2f104bd6b922dcdbaa3b3672a1fafe5
Author: Charles Reis <creis@chromium.org>
Date: Thu Jul 14 20:47:49 2016

Clear stale NavigationParams from HistoryController.

This prevents newly created iframes during a back/forward from
targeting the wrong NavigationEntry.

BUG=623319
TEST=See bug https://crbug.com/chromium/623319#c20 for repro steps.
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2144823002
Cr-Commit-Position: refs/heads/master@{#404870}
(cherry picked from commit 4d78d33cb1852e7d487f1d327517c4c4044a3ca3)

Review URL: https://codereview.chromium.org/2155443002 .

Cr-Commit-Position: refs/branch-heads/2785@{#125}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/853590fad2f104bd6b922dcdbaa3b3672a1fafe5/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/853590fad2f104bd6b922dcdbaa3b3672a1fafe5/content/renderer/history_controller.cc
[modify] https://crrev.com/853590fad2f104bd6b922dcdbaa3b3672a1fafe5/content/renderer/history_controller.h


### bu...@chromium.org (2016-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ee471f56c04351e46c360722ad813a141dba79fb

commit ee471f56c04351e46c360722ad813a141dba79fb
Author: Charles Reis <creis@chromium.org>
Date: Thu Jul 14 20:56:11 2016

Update HistoryController::current_entry_ on all main frame back/forwards.

This fixes a case where it was left stale on a cross-origin commit
because the provisional_entry_ had been cleared by a different commit.

BUG=623319
TEST=See bug https://crbug.com/chromium/623319#c14 for repro steps.
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2134493002
Cr-Commit-Position: refs/heads/master@{#404537}
(cherry picked from commit ab22bdfc5cb681f2f4dc789171e97618a9657486)

Review URL: https://codereview.chromium.org/2149203002 .

Cr-Commit-Position: refs/branch-heads/2743@{#629}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/ee471f56c04351e46c360722ad813a141dba79fb/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/ee471f56c04351e46c360722ad813a141dba79fb/content/renderer/history_controller.cc


### bu...@chromium.org (2016-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b59c2a8c8e48cee3b5e59635f4faa9be1dff925f

commit b59c2a8c8e48cee3b5e59635f4faa9be1dff925f
Author: Charles Reis <creis@chromium.org>
Date: Thu Jul 14 21:04:38 2016

Clear stale NavigationParams from HistoryController.

This prevents newly created iframes during a back/forward from
targeting the wrong NavigationEntry.

BUG=623319
TEST=See bug https://crbug.com/chromium/623319#c20 for repro steps.
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2144823002
Cr-Commit-Position: refs/heads/master@{#404870}
(cherry picked from commit 4d78d33cb1852e7d487f1d327517c4c4044a3ca3)

Review URL: https://codereview.chromium.org/2151743004 .

Cr-Commit-Position: refs/branch-heads/2743@{#631}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/b59c2a8c8e48cee3b5e59635f4faa9be1dff925f/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/b59c2a8c8e48cee3b5e59635f4faa9be1dff925f/content/renderer/history_controller.cc
[modify] https://crrev.com/b59c2a8c8e48cee3b5e59635f4faa9be1dff925f/content/renderer/history_controller.h


### sh...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2016-07-16)

Is https://cluster-fuzz.appspot.com/testcase?key=4850444346327040 related to this bug? If not, please file a new bug using CF.

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Congratulations, $2,000 for this report.  Thanks!

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/623319?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084699)*
