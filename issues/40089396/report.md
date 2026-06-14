# URL Bar Spoofing using redirection and location.reload();

| Field | Value |
|-------|-------|
| **Issue ID** | [40089396](https://issues.chromium.org/issues/40089396) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | jc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-03-29 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

URL Bar Spoofing using redirection and location.reload()

**VERSION**  

Chrome Version: [10.0.648.204] + [stable, beta, or dev]  

Operating System: [windows 7 and Mac]

**REPRODUCTION CASE**  

<http://www.alternativ-testing.fr/Research/safari/spoof/654gf6598bf95h/>

Click on the button , when you see twitter.com on title of tab , open a new tab , look to the previous tab , the URL Bar show Twitter.com with the previous content.

## Attachments

- [chromespoof.png](attachments/chromespoof.png) (image/png; charset=binary, 43.4 KB)
- [chromeSSLspoof.png](attachments/chromeSSLspoof.png) (image/png; charset=binary, 49.4 KB)
- [index3.php](attachments/index3.php) (text/x-php; charset=us-ascii, 174 B)
- [index.php](attachments/index.php) (text/html; charset=us-ascii, 481 B)
- [index2.php](attachments/index2.php) (text/html; charset=us-ascii, 481 B)

## Timeline

### jc...@gmail.com (2011-03-29)

It's a webkit vulnerability.

### js...@chromium.org (2011-03-29)

This looks very similar to https://crbug.com/chromium/76666.

@creis - You seem to be the one most active in this area. Could you take a look?

### cr...@chromium.org (2011-03-29)

I tested it out, and I can still repro it after the fix for https://crbug.com/chromium/76666.  I can take a closer look to see if it's related, though.

### cr...@chromium.org (2011-03-30)

The problem seems to be related to TabContents::OnDidRedirectProvisionalLoad.

The test page has a button that reloads the page.  The server seems to randomly decide to redirect to twitter.com every few requests, so sometimes the reload ends up being a redirect.  This causes OnDidRedirectProvisionalLoad to update the URL of the current NavigationEntry to twitter.com.

However, the test page uses a JavaScript timer to stop the load before it finishes.  At this point, we don't fix the NavigationEntry, so switching tabs away and back makes us display twitter.com as the URL.

Brett, I think you're more familiar with the NavigationEntry logic than me.  Is there a way we can reset the NavigationEntry's URL if the load aborts?  It looks like we're just forgetting the original URL right now...

### jc...@gmail.com (2011-03-30)

I think the SecSeverity is Medium.

### br...@chromium.org (2011-03-30)

I'm surprised we're modifying the URL on redirects, I don't think this is correct at all.

I checked the provenance of this code, which I imagined was checked in recently by somebody who didn't understand something trying to work around some subtle bug. However, it dates back to the very first open sourcing of Chromium!
http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/web_contents.cc?revision=15&content-type=text%2Fplain&pathrev=14413
(search for DidRedirectProvisionalLoad).

I can't think of a good reason we should be updating the URL when the provisional load is redirected. TabContents shouldn't be doing that kind of computation anyway (it should be the NavigationController), and it seems doing this can only cause Bad Things like this bug.

I think that function should just be deleted. We should also see if we can delete the code that issues that notification (not sure if anybody else is using it). See this change for how it gets called:
http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/renderer_host/resource_dispatcher_host.cc?r1=70292&r2=70291&pathrev=70292

### jc...@gmail.com (2011-03-30)

It's possible to spoof SSL/TLS .

### in...@chromium.org (2011-03-30)

[Empty comment from Monorail migration]

### cr...@chromium.org (2011-03-30)

I can take this one, but I'll be out of town the next two days and probably won't have time to make much progress on it until Monday.  If someone else wants to tackle it before then, feel free.

### in...@chromium.org (2011-03-30)

Monday sounds good. This is a sensitive area and want to leave it in your able hands. It will be bad to break the navigation logic :(

### jc...@gmail.com (2011-04-04)

[Comment Deleted]

### cr...@chromium.org (2011-04-05)

Re: https://crbug.com/chromium/77786#c6: It's not quite as simple as deleting TabContents::OnDidRedirectProvisionalLoad, unfortunately.

First, it turns out the pre-rendering code relies on that method so that it can swap in a pre-rendered page for the redirect.  Thus, we would have to relocate that code if we deleted the method.  Maybe we could have it listen to the RESOURCE_RECEIVED_REDIRECT notification in ResourceDispatcherHost (linked at the end of https://crbug.com/chromium/77786#c6)?

Second, that TabContents method isn't being called directly by the ResourceDispatcherHost logic.  The RDH logic first sends a ResourceMsg_ReceivedRedirect message to the renderer, which winds through a lot of WebKit logic and then sends it back to the browser as a ViewHostMsg_DidRedirectProvisionalLoad message.  There's lots of places in there that we might filter out the redirect before notifying the pre-rendering logic, including in TabContents::OnDidRedirectProvisionalLoad itself.

Timo, I'm cc'ing you so you have the context for the code review I'm about to send out.

### bu...@chromium.org (2011-04-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=80639

------------------------------------------------------------------------
r80639 | creis@chromium.org | Wed Apr 06 09:35:49 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/tab_contents.cc?r1=80639&r2=80638&pathrev=80639

Prevent changes to NavigationEntry's URL for a provisional redirect.

BUG=77786
TEST=Visit a page that redirects on reload, then stop before it finishes.

Review URL: http://codereview.chromium.org/6793029
------------------------------------------------------------------------

### jc...@gmail.com (2011-04-06)

spoofing don't work on google chrome 11.0.696.34 

### cr...@chromium.org (2011-04-06)

I just tested and the bug is still present in 11.0.696.34.  It's fixed in r80639, which hasn't been deployed yet.

### in...@chromium.org (2011-04-06)

Awesome Charlie, 1 down.

### js...@chromium.org (2011-04-06)

We'll need to merge to m11.

### jc...@gmail.com (2011-04-06)

when the reward-panel will discuss about my reward? :)

### jc...@gmail.com (2011-04-06)

[Comment Deleted]

### sc...@gmail.com (2011-04-06)

@jconsultant.chancel: please be patient. The reward-panel will review the full content of this bug report, and may be disappointed if they see impatience.

The bug got fixed just recently, so I'd expect the reward-panel to review the bug in their next batch of reward reviews. That will likely occur within the next week.

### sc...@gmail.com (2011-04-06)

[Empty comment from Monorail migration]

### jc...@gmail.com (2011-04-06)

sorry for my impatience.

### sc...@gmail.com (2011-04-06)

Merged to M11 at: Committed revision 80690

### bu...@chromium.org (2011-04-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=80690

------------------------------------------------------------------------
r80690 | cevans@chromium.org | Wed Apr 06 13:56:55 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/tab_contents/tab_contents.cc?r1=80690&r2=80689&pathrev=80690

Merge 80639 - Prevent changes to NavigationEntry's URL for a provisional redirect.BUG=77786TEST=Visit a page that redirects on reload, then stop before it finishes.Review URL: http://codereview.chromium.org/6793029
TBR=creis@chromium.org
Review URL: http://codereview.chromium.org/6802022
------------------------------------------------------------------------

### jc...@gmail.com (2011-04-13)

Fixed in 11.0.696.43 beta

### sc...@gmail.com (2011-04-14)

Thanks Jordi, I agree this is Medium as per your earlier comment, due to the level of use interaction.
The panel doesn't always reward for Medium bugs, but in this case we're provisionally rewarding $500 as we're happy to be with less spoofs.

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

### jc...@gmail.com (2011-04-15)

thank you very much for this reward.

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### jc...@gmail.com (2011-04-22)

Have you an idea of the release date?

### sc...@gmail.com (2011-04-22)

Hopefully within a week... the predictable 6-week release schedules rock :D

### jc...@gmail.com (2011-04-24)

I think i can reproduce this without user interaction or with just minimal interaction like juste one click. if it's the case this vulnerability is high?

### jc...@gmail.com (2011-04-24)

this vulnerability is high , i can reproduce this without user interaction ...

New Testcase => https://alternativ-testing.fr/Research/safari/spoof/newtestcasenouserinteraction65s465ds4/

### jc...@gmail.com (2011-04-24)

or HTTP://alternativ-testing.fr/Research/safari/spoof/newtestcasenouserinteraction65s465ds4/

### sc...@gmail.com (2011-04-25)

Hard to say. The first time I hit the URL, I go straight to twitter but it behaves more interestingly if I again open your URL in a new tab a 2nd time.

### jc...@gmail.com (2011-04-25)

The test case will redirect half the time to twitter ,please try 2 times , and if the 1frst or the 2nd time the spoofing is well , this is a high spoofing.

I go coded a better testcase.

### jc...@gmail.com (2011-04-25)

Test it !

SecSeverity high?

### sc...@gmail.com (2011-04-25)

Can you host the latest and greatest at some easily clickable URL?

### jc...@gmail.com (2011-04-25)

do you want this ? => http://www.alternativ-testing.fr/Research/Google Chrome/googlechrome%20location%20spoofing/564vf6d4gdf64/



### jc...@gmail.com (2011-04-25)

http://www.alternativ-testing.fr/Research/Google%20Chrome/googlechrome%20location%20spoofing/564vf6d4gdf64/


### sc...@gmail.com (2011-04-25)

We're all getting different results. Perhaps there's a weird timing component to this? Given that the fix is going out really soon and the release notes are already written, I'll just leave them as is.


### jc...@gmail.com (2011-05-01)

Now the fix is released , i think i can write a small blog-post without PoC.
let me know if you want delete of my blog post (without PoC).

### sc...@gmail.com (2011-05-01)

Heya Jordi -- feel free to release the PoC as well. The fix has been out for several days now, so autoupdate should have taken care of matters well enough.

Also, I've started the payout process, in case you were thinking of asking :)

### sc...@gmail.com (2011-05-04)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

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

This issue was migrated from crbug.com/chromium/77786?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089396)*
