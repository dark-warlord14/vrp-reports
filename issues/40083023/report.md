# Possible Location Bar & SSL Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40083023](https://issues.chromium.org/issues/40083023) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | jc...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2010-09-02 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version       : 6.0.472.53

Other browsers tested:
  Add OK or FAIL after other browsers where you have tested this issue:
     Safari 4:FAIL
  Firefox 3.x:FAIL
         IE 7:FAIL
         IE 8:FAIL

What steps will reproduce the problem?
1. Open a new tab and go to https://www.alternativ-testing.fr/chromeSpoof56f4d654fd/index5.php
2. go to https://www.alternativ-testing.fr/chromeSpoof56f4d654fd/index5.php#test
3. Reload and Back

What is the expected result?
The location bar is Spoofed with valid SSL/TLS certificate.

## Attachments

- [spoof.png](attachments/spoof.png) (image/png; charset=binary, 107.6 KB)
- [test-spoof.html](attachments/test-spoof.html) (text/plain; charset=us-ascii, 259 B)
- [spoofing.php](attachments/spoofing.php) (text/x-php; charset=us-ascii, 3.1 KB)
- [google.png](attachments/google.png) (image/png; charset=binary, 80.4 KB)
- [spoofing.php](attachments/spoofing_53343154.php) (text/x-php; charset=us-ascii, 3.0 KB)
- [test-spoof.html](attachments/test-spoof_53343155.html) (text/plain; charset=us-ascii, 195 B)
- [spoofchrome.png](attachments/spoofchrome.png) (image/png; charset=binary, 38.5 KB)

## Timeline

### in...@chromium.org (2010-09-02)

I can reproduce on both v6 and v7 trunk. SSL cert spoofing is bad, but I haven't tested if it is possible to automate this without any user interaction. Marking secseverity for now.

Wan-Teh, can you please take a look.

### in...@chromium.org (2010-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2010-09-02)

jcivelle,finner: can one of you look at this bug?  Thanks.

### jc...@gmail.com (2010-09-02)

[Comment Deleted]

### jc...@gmail.com (2010-09-12)

This PoC works with Internet Explorer as well except that back() don't work .
Can one of you analyse this?

### in...@chromium.org (2010-09-14)

Jay, did you get a chance to take a look at this. 

### jc...@chromium.org (2010-09-14)

@inferno
I am transitioning to another team, so I won't be doing much front-end work.
Unasigning myself.
Finnur has been doing SSL related work recently, may be he would be a good person to look at this.

### js...@chromium.org (2010-09-15)

Bulk move to m7.

### fi...@chromium.org (2010-09-15)

I have very little insight into the Omnibox code and even less in the internals of our SSL handling. Peter is a better candidate for the former and wtc/abarth for the latter.

### pk...@chromium.org (2010-09-15)

This is more wtc/abarth/brettw than me.

### in...@chromium.org (2010-09-16)

Brett, can yu please take a look or help with an owner. this is a ssl cert spoof, looks pretty ugly.

### br...@chromium.org (2010-09-28)

I'm swamped with Pepper/plugin stuff right now.

Jay: you've looked at some related stuff. How does your schedule look?

### jc...@chromium.org (2010-09-28)

I'll take a look.

### jc...@chromium.org (2010-09-28)

The URLs above return a 404 so I cannot repro :-(

### jc...@gmail.com (2010-09-28)

[Comment Deleted]

### jc...@chromium.org (2010-09-28)

Good news, it really looks like a dup of 51680 that I fixed already. (I cannot repro on trunk)
Bad news, I did not merge this to the M7 branch.
Security team, Anthony let me know if you want the patch merged (it is pretty significant and might introduce regressions).

### js...@chromium.org (2010-09-28)

We have that change on the merge list for m7, but decided it was too high risk for m6. One of us can cover the merge, unless you feel particularly inclined to chip in. :)

### jc...@gmail.com (2010-10-20)

This Bug isn't a duplicate...
Tested on Google Chrome 7.0.517.41

### sc...@gmail.com (2010-10-20)

Reopening to make sure it gets reinvestigated.

### jc...@gmail.com (2010-10-20)

[Comment Deleted]

### js...@chromium.org (2010-10-20)

I tested 7.0.517.41 stable on Mac and Linux. It ends up displaying the Verisign page but with an HTTP URL for the test site. So, there's still a bug, but if you can't spoof the SSL state or the URL while on an attacker controlled site then I don't see a security impact. (Of course, we'll want to verify there's not more to it.)

### jc...@gmail.com (2010-10-20)

[Comment Deleted]

### in...@chromium.org (2010-10-20)

Yeah. the spoof exists and omnibox is showing the wrong url or in other words, url is navigated, but content window is not changed. Tested. http://www.alternativ-testing.fr/Research/Google%20Chrome/Google%20Chrome%20SSL%20Spoofing/TestCase5fd4df654df/

Jay, can you please take a look.

### jc...@gmail.com (2010-10-21)

[Comment Deleted]

### in...@chromium.org (2010-10-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-10-21)

@jordi, I don't see how it could be possible to execute JavaScript in the other domain because the issue here is with when the URL and SSL state updates occur, which shouldn't have any bearing on how and when JavaScript is executed. However, we have no way of confirming your claim without you a demonstration. So, pleaxse provide a proof of concept of what you have found.

### jc...@gmail.com (2010-10-21)

New testcase using location.href and history.forward() 

http://www.alternativ-testing.fr/Research/Google%20Chrome/Google%20Chrome%20SSL%20Spoofing/testcasehighurlspoofing/

SecSeverity as high?

### jc...@gmail.com (2010-10-21)

[Comment Deleted]

### jc...@gmail.com (2010-10-21)

[Comment Deleted]

### js...@chromium.org (2010-10-21)

That image appears to show cookies for your site, not linkedin.com. 

We just checked this with in Chrome 7 on Linux and Windows. The JavaScript is executing in the context of the actual page content (regardless of the omnibox showing an incorrect URL). Results from your PoC, a JavaScript URL in the omnibox, and the console are all consistent. It's a spoof, not a same origin bypass. (This makes sense given that the spoofed state is a bug because it's showing the wrong URL for the current page.)

However, the spoof now does seem to be consistent. Whereas it was very intermittent before.


### jc...@gmail.com (2010-10-21)

[Comment Deleted]

### jc...@gmail.com (2010-10-22)

[Comment Deleted]

### jc...@gmail.com (2010-10-23)

This spoofing use window.open , location.href , location.reload() , history.back() , history.forward() & Redirect and it works with history.back() or/and history.forward().

### jc...@gmail.com (2010-10-23)

I can give you the PoC in a zip folder.

### jc...@gmail.com (2010-10-25)

[Comment Deleted]

### sc...@gmail.com (2010-10-25)

Sounds interesting! Please detail the steps to demo it and/or link a PoC


### jc...@gmail.com (2010-10-25)

New TESTCASE with javascript execution using drag & drop into the location bar.

https://www.alternativ-testing.fr/Research/Google%20Chrome/Google%20Chrome%20SSL%20Spoofing/NEWTESTCASE/

### jc...@gmail.com (2010-10-25)

SecSeverity as High?

### js...@chromium.org (2010-10-25)

No. A high severity vulnerability would be a direct same-origin bypass. This demonstration requires the user to to perform a very specific and unusual action. It's no more effective than putting up a fake login page with the spoofed URL (and it's actually more suspicious).

### jc...@gmail.com (2010-10-27)

I would like know if this issue is valid for a reward?
And can i write a blog post about this ?

### sc...@gmail.com (2010-10-28)

@jordi: I'll send it over to the rewards panel once we have found the right person to work on it and have a code fix. We usually like to do things that way because the panel can then convene with a full understanding of what exactly was wrong in the code.
I don't have an ETA yet, sorry.

In terms of the blog post -- we do encourage people to share their discoveries with the world. However, we ask that people hold off on doing this until we have a patch out to our users. Premature blogging may not be looked on favourably by the rewards panel.

### ke...@chromium.org (2010-10-28)

Is this needed for m8?

### in...@chromium.org (2010-10-28)

Jason, yes, we need an owner here. Brett, can you please help.

### ab...@chromium.org (2010-10-30)

Owner hot potato.

### ab...@chromium.org (2010-10-30)

Let me see if I understand the issue:

1) Tab A creates a new tab B.
2) Tab B navigates itself to a fragment and then reloads itself.
3) The reload triggers a redirect to the victim site.
4) Tab A then navigates tab B back one history item.

### ab...@chromium.org (2010-10-30)

From that sequence, it sounds like the navigation entry created by the fragment navigation is incorrectly modified when processing the reload.

I suspect the confusion is related to the problem that the reload isn't supposed to create a new navigation entry, but with the redirect (which also doesn't create a new navigation entry) takes us to a new location.

### jc...@gmail.com (2010-10-30)

the new testcase using history.forward() 
https://www.alternativ-testing.fr/Research/Google%20Chrome/Google%20Chrome%20SSL%20Spoofing/NEWTESTCASE/

### jc...@gmail.com (2010-10-30)

[Comment Deleted]

### jc...@gmail.com (2010-10-30)

1) Tab A creates a new tab B.
2) Tab B navigates itself to a fragment and then reloads itself.
3) The reload triggers a redirect to the victim site.
4) Tab A then navigates tab B back one history item.
5) Tab A use location.href on tab B.
6) Tab A use history.forward on tab B.


### ab...@chromium.org (2010-10-30)

I have a local repro.  It's seems like the thing that's confusing the navigation controller is the redirect during the reload.

### ab...@chromium.org (2010-10-30)

The fragment navigation appears essential also.

### ab...@chromium.org (2010-10-30)

Looking the debugger (for my reduced test case) the navigation controller seems to have the right understanding about what's going on.  It looks like the problem might be in the rendering engine.

/me => sleep.  Will look more tomorrow.

### ab...@chromium.org (2010-10-30)

The way Safari solves this problem is interesting.  They show the same web page as we do, but they don't update the location bar the way we do.  That might be the least-injury way of fixing this bug.

### ab...@chromium.org (2010-10-31)

I think the issue is that the document sequence number is being re-used during the reload even though we're actually creating a new document.

### ab...@chromium.org (2010-10-31)

I think this patch fixes the issue.  I need to test it to make sure it doesn't break other things though.

Index: WebCore/history/HistoryItem.cpp
===================================================================
--- WebCore/history/HistoryItem.cpp	(revision 70977)
+++ WebCore/history/HistoryItem.cpp	(working copy)
@@ -237,6 +237,8 @@
 void HistoryItem::setURL(const KURL& url)
 {
     pageCache()->remove(this);
+    if (!equalIgnoringFragmentIdentifier(this->url(), url))
+        m_documentSequenceNumber = generateSequenceNumber();
     setURLString(url.string());
     clearDocumentState();
 }


### js...@chromium.org (2010-10-31)

Awesome. Thanks Adam.

### ab...@chromium.org (2010-10-31)

So, that patch passes all the existing tests.  I'm going to write a test and upload it for review.  I'm not overly confident in the patch because this is a complicated area, but we'll see what reviewers think.

### ab...@chromium.org (2010-11-01)

I'm getting distracted by other things I need to work on.  Would it be possible for someone on the security team to take the ball from here?

### js...@chromium.org (2010-11-01)

Sure, but what's left to do?

### ab...@chromium.org (2010-11-01)

Mostly just writing a test.

### js...@chromium.org (2010-11-01)

Gotcha. I'll grab it and take a crack at the layout test. Is there an upstream bug already or will I need to file one?

### ab...@chromium.org (2010-11-01)

No upstream bug yet.

### in...@chromium.org (2010-11-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-11-02)

@jnd - Has graciously volunteered to walk this fix the last mile.

### jc...@gmail.com (2010-11-05)

I've found a way for steal login and password saved . But require complicated step with minimal user interaction .

### jc...@gmail.com (2010-11-05)

1) go to https://www.linkedin.com/secure/login and save your login & password
2) Go to http://www.alternativ-testing.fr/Research/Google%20Chrome/Google%20Chrome%20SSL%20Spoofing/passwordsteal/ and click on the link
3) Try to connect with saved password.
4)Login & Password are sent to ALTERNATIV-TESTING.fr

### jn...@chromium.org (2010-11-12)

I tried to write a layout test to reproduce this bug for the webkit patch, however my test couldn't get the spoof situation in my either chrome build(9.0.580.0 Developer Build 65872) or WebKit build.

@jconsultant.chancel, could you test a look at my test and point where I were wrong. 

### in...@chromium.org (2010-11-12)

Johnny, can you please test against v8 beta (552) branch. It does reproduce there, if you can please make a testcase on that, then we should still check in the webkit fix from Adam alognwith your layouttest.

### jc...@gmail.com (2010-11-13)

Try redirect('https://www.linkedin.com/secure/login', 302); because spoofing google.com don't work (dont't know why).

### jc...@gmail.com (2010-11-13)

your testcase works on google chrome 8.0.552.200

### in...@chromium.org (2010-11-15)

+cc creis.

This might be fixed in https://bugs.webkit.org/show_bug.cgi?id=48809, http://trac.webkit.org/changeset/71437. Charlie, does it seem related ? This bug is not reproducing on trunk, but does reproduce on 552. So, it does look related to your history fix. We have a planned beta pretty soon, and if this is the one :), then we would probably want to merge this (or wait for the follow up patch).

### in...@chromium.org (2010-11-15)

Lets wait for Charlie's followup patch before merging the fix. See last comment in http://code.google.com/p/chromium/issues/detail?id=62156.

https://crbug.com/chromium/54262#c9 by project member creis@chromium.org, Nov 11 (3 days ago)

I think this is higher priority, and I'm actively working on it.  Right now, back/forward is broken in Chrome and test_shell for any fragment navigations (page.html#foo).

I have a draft of a fix at https://bugs.webkit.org/show_bug.cgi?id=48809, but I'm figuring out why it's interfering with popstate at the moment.


### jn...@chromium.org (2010-11-15)

According to my analysis, When reloading the same page, due to some reasons, like cookie or server intended behavior, the returned contents might be different than the result we just got before reloading the same page.
In webkit, the historyItem created by fragment change (spoofing.php#123) shared same document documentSequenceNumber with previous one (spoofing.php), after the historyItem(spoofing.php#123) was reloaded, the url of that historyItem(spoofing.php#123) was replaced to new one (like linedin.com), so the documentSequenceNumber of historyItem(spoofing.php#123) was as same as the documentSequenceNumber of historyItem(linkedin.com), that is why the url bar was changed, but the contents did not.

Adam already had right analysis on #54, and his patch on #55 did fix this issue.

The attached files are a more simple test case (redirect to google.com) and resultant result.
Will file a webkit bug and provide corresponding patch with a layout test-case.

### jc...@gmail.com (2010-11-15)

[Comment Deleted]

### jc...@gmail.com (2010-11-15)

Try redirect('https://www.linkedin.com/secure/login', 302); because google.com spoofing don't work


### jc...@gmail.com (2010-11-15)

[Empty comment from Monorail migration]

### jn...@chromium.org (2010-11-15)

@ jconsultant.chancel, google.com spoofing did work, you can try my test case. It's another type URL spoofing, the URL bar showed "xxx/spoofing.php", but the content was google.com. It can be reproduced on current stable version 7.0.517.44.

### cr...@chromium.org (2010-11-15)

@inferno: I do have a new WebKit patch under review (https://bugs.webkit.org/attachment.cgi?id=73802&action=review) for fixing https://crbug.com/chromium/62156, as you point out.  It does sound like the patch could help with this bug, since it affects fragment navigations and content state updates.  Specifically, it's trying to solve a very related problem in https://crbug.com/chromium/58082, where the content state of NavigationEntries can get swapped.

I haven't verified if it fixes this yet, but I can give it a try to find out.

### cr...@chromium.org (2010-11-15)

FYI, my CL doesn't fix this issue, so don't wait for it.  When visiting http://www.alternativ-testing.fr/Research/Google%20Chrome/Google%20Chrome%20SSL%20Spoofing/TestCase5fd4df654df/, I see the Verisign page with the alternativ-testing.fr URL in the Omnibox.

Adam's patch to HistoryItem does cause the correct URL (sealinfo.verisign.com) to display in the Omnibox, but it looks like things still break if you click Forward and then Back.  Forward adds a #123 fragment to the URL, and Back leads to the original problem-- alternativ-testing.fr showing in the Omnibox but with the Verisign page displayed.  (I have some other changes in my tree, though, so others should see if they can reproduce this.)

### pk...@chromium.org (2010-11-15)

[Empty comment from Monorail migration]

### jn...@chromium.org (2010-11-16)

@creis, the following is my analysis.

#123 fragment in the final URL is because of a logic in URLRequestJob::NotifyHeadersComplete(url_request_job.cc, line 462), it says it moves the reference fragment of the old location to the new one if the new one has none and it duplicates mozilla's behavior.

In the case http://www.alternativ-testing.fr/Research/Google%20Chrome/Google%20Chrome%20SSL%20Spoofing/TestCase5fd4df654df/, the new TabB was from index5.php, changed location to index5.php#123, then reloaded to sealinfoxxx#123, it created two historyItems, index5.php and from sealinfoxxx#123(from index5.php#123)

Af first, the TabA called TabB's history.back, the history change was from sealinfoxxx#123 to index5.php. According to the loadType(FrameLoadTypeIndexedBackForward), the cache policy was ReturnCacheDataElseLoad(FrameLoader::navigateToDifferentDocument), so the cached data for index5.php was used, which redirected from index5.php to sealinfoxxx. In here sealinfoxxx was not a historyItem, it's just a redirection result and navigation entry of historyItem:index5.php.

So when you forwarded, the history change was from index5.php to sealinfoxxx#123, since the current display URL was sealinfoxxx, so you saw the url location from sealinfoxxx to sealinfoxxx#123.

Yes, the next back led to the original problem, it's because another webkit bug. In this previous forward, since the only difference between current doc URL: sealinfoxxx(historyItem:index5.php) and current target URL:sealinfoxxx#123 was the fragment #123, it was consider as navigation in same doc, so historyItem:index5.php was set to same documentState of sealinfoxxx#123, but actually those two historyItems should not be same. then in back operation, changing sealinfoxxx#123 to index5.php was also considered as navigation in same doc, so you saw wrong URL in location URL. 

The solution to fix this issue is to only allow copying the documentState from a historyItem only the two historyItems have same URL with ignoring fragment identifier. Please refer to the following patch.
 PassRefPtr<HistoryItem> HistoryController::createItemTree(Frame* targetFrame, bool clipAtTarget)
 {
     ...
         if (m_previousItem) {
             if (m_frame != targetFrame)
                 bfItem->setItemSequenceNumber(m_previousItem->itemSequenceNumber());
+            if (equalIgnoringFragmentIdentifier(m_previousItem->url(), bfItem->url()))
                 bfItem->setDocumentSequenceNumber(m_previousItem->documentSequenceNumber());
         }
     ...
 }

### jn...@chromium.org (2010-11-17)

created a associated webkit bug: https://bugs.webkit.org/show_bug.cgi?id=49654

### da...@chromium.org (2010-11-17)

[Empty comment from Monorail migration]

### jc...@gmail.com (2010-11-27)

do you have an idea of the release date with this issue ?

### js...@chromium.org (2011-01-08)

Darin grabbed this upstream, so reassigning. Darin, not to nag, but have you got an eta on this? we really want to land a fix before m9 is released?

### jc...@gmail.com (2011-01-09)

[Comment Deleted]

### jc...@gmail.com (2011-01-09)

[Comment Deleted]

### jc...@gmail.com (2011-01-09)

[Comment Deleted]

### jc...@gmail.com (2011-01-09)

[Comment Deleted]

### jc...@gmail.com (2011-01-09)

[Comment Deleted]

### jc...@gmail.com (2011-01-09)

[Comment Deleted]

### jc...@gmail.com (2011-01-09)

[Comment Deleted]

### sc...@gmail.com (2011-01-09)

Oh, dear. It looks like Jordi's PC has malware and someone is abusing it to send spam and/or make Jordi look really bad. I'll send him a personal note.

### jc...@gmail.com (2011-01-09)

password changed ... sorry it was a bad friend who joked ...

### da...@chromium.org (2011-01-20)

Patched upstream with http://trac.webkit.org/changeset/76205

### in...@chromium.org (2011-01-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-20)

@jconsultant.chancel: thanks again for your patience. As you can see, this was a tricky issue to fix properly. We now have a candidate code change to get to users.

The current plan is to ship the fix either in the upcoming Chrome 9, or in a patch shortly after Chrome 9. Not much longer now :)

### jc...@gmail.com (2011-01-21)

This vulnerability can be used for spoof SSL/TLS & URL .
It can be used again to steal saved password & login with just a minimal interaction like a click.

I can give you a PoC for steal the login & the password with a simple click.

### sc...@gmail.com (2011-01-21)

@jconsultant.chancel: yes, it can :) I've updated the severity to SecSeverity-High to reflect this.
As a SecSeverity-High bug, the rewards panel will discuss it once the bug is closer to getting released to users. Thanks for your continued discretion; as you can see, we're now a lot closer to have this resolved. The hard part (complicated code change) has been resolved.

### jc...@gmail.com (2011-01-24)

when the reward-panel will discuss about this bug?

### sc...@gmail.com (2011-01-24)

@jconsultant.chancel: as per previous message, "the rewards panel will discuss it once the bug is closer to getting released to users". A couple of weeks perhaps?

### ke...@google.com (2011-02-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-03)

@jconsultant.chancel: the rewards panel discussed this bug. We're provisionally rewarding it at the $1000 level. Congratulations!
We're rewarding above the base amount because you were helpful in providing lots of different testcases, and in discussing the severity.
Please refrain from blogging about it until fixed -- we're definitely fixing it in one of the Chrome 9 patches, probably in a couple of weeks.

### ch...@gmail.com (2011-02-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-10)

don't need m10 merge since branched earlier.

m9 merged in r78236 (painfully, had to skip layouttests since there were conflicts and had a small issue in int64_t naming in HistoryItem.h"

### in...@chromium.org (2011-02-10)

[Empty comment from Monorail migration]

### jc...@gmail.com (2011-02-21)

fixed in 10.0.648.82 beta

### sc...@gmail.com (2011-02-21)

Thanks for checking, Jordi. If you can just wait a little longer for us to release it to Stable users via a patch to Chrome 9, that would be awesome. We've already done the merge, just doing some QA.

### jc...@gmail.com (2011-02-21)

Have you an idea of the release date?

### jc...@gmail.com (2011-03-01)

the release is done , where is my reward?

### sc...@gmail.com (2011-03-01)

One step ahead of you Jordi, I started the process about an hour ago :) Might take a couple of weeks; I've no idea why bank wires in 2011 aren't instant, but there you have it...
Thanks! This bug was interesting.

### jc...@gmail.com (2011-03-01)

And now , can i write a blog post about this vulnerability? please reply quickly.

### jc...@gmail.com (2011-03-01)

?

### jc...@gmail.com (2011-03-01)

Now the fix is released , i think i can write a small blog-post without PoC.
let me know if you want delete of my blog post (without PoC).

### sc...@gmail.com (2011-03-01)

Of course. Go right ahead.

### jc...@gmail.com (2011-03-01)

what is the CVE id?

### js...@chromium.org (2011-03-01)

We aren't a CVE assigning authority, so we currently don't provide or track CVEs.

### jc...@gmail.com (2011-03-02)

this spoofing is exploitable on safari.
Have you reported it and credited me?

### sc...@gmail.com (2011-03-02)

Hey Jordi -- Apple are aware and they know who to credit :)

### sc...@gmail.com (2011-03-04)

Invoice finalized; payment is in e-payment system.

### jc...@gmail.com (2011-03-04)

On my last reward , multiple mails was sent for the wire transfer
but i don't have received any mail for this one.

do I have to wait a few weeks to send my IBAN number?

### sc...@gmail.com (2011-03-04)

If the last reward worked in the end, hopefully this one should work too, without the need to give us the IBAN again.

All of the finance systems seem to do things in "batches" so you might get a few days or a week latency here and there.

### jc...@gmail.com (2011-03-10)

I did not receive my reward, 
I think that there was an error in the transfer.

please reply quickly !

### jc...@gmail.com (2011-03-10)

[Comment Deleted]

### sc...@gmail.com (2011-03-10)

Jordi, please be patient. There is nothing I can do to make an international wire transfer go faster. I see no indication that anything has gone wrong at this stage.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### jc...@gmail.com (2011-05-04)

[Comment Deleted]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/54262?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083023)*
