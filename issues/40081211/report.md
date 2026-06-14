# Security: Illegal domain name resolving using leading dot creating unexpected behaviour/URL Bar Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40081211](https://issues.chromium.org/issues/40081211) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network>DNS, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Reporter** | [Deleted User] |
| **Assignee** | cr...@chromium.org |
| **Created** | 2015-01-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome on OS X allows and resolves domain names containing a leading dot. You cannot use the omnibar, but by linking to it, Chrome will allow it:

data:text/html,<a href="http://.example2.s3.amazonaws.com/">Test</a>

The problem with this is that alot of cloud services - one example which is widely used, is Amazon S3 - will not match it to the proper domain (without the leading dot) since Chrome sends the Host-header with leading dot, but instead see it as a new endpoint, thus creating the posibility to claim it yourself with a leading dot:

<Error>
<Code>NoSuchBucket</Code>
<Message>The specified bucket does not exist</Message>
<BucketName>.example2</BucketName>

This basically means that all services using S3 in this example are vulnerable to this on Chrome on Mac OS X. This also working with custom subdomains pointing to the external service, which makes alot of high profile websites currently vulnerable to this.

The reason here seems to be that Chrome is resolving the IP of the domain without the leading dot, but will send the Host-header with the leading dot.

Also, by doing a redirect on the leading dot-domain, you will lock the omnibar to the previous URL, thus creating a URL Bar Spoofing, example:

data:text/html,<a href="http://.example.s3.amazonaws.com/login2">TEST</a>

Content of login2:  

<meta http-equiv="refresh" content="0; url=http://example.com/">

PoC-image showing example.com with the amazonaws.com-URL in the omnibar.

This should be resolved by doing the following:  

The redirect from this domain should update the value of the omnibar.  

You should not allow leading dot in domains, it should not resolve to the domain without the leading dot.

Examples of curl and host-requests for leading dot:

$ curl .example.s3.amazonaws.com  

curl: (6) Could not resolve host: .example.s3.amazonaws.com

$ host .example.s3.amazonaws.com  

host: '.example.s3.amazonaws.com' is not a legal name (empty label)

Only Blink-enabled browsers are resolving leading dot, IE, FF and Safari are not affected by this.

**VERSION**  

Chrome Version: 39.0.2171.95 stable / 41.0.2224.3 dev  

Operating System: Mac OS X 10.10 / Mac OS X 10.9.5

## Attachments

- [Screen Shot 2015-01-18 at 12.02.07.png](attachments/Screen Shot 2015-01-18 at 12.02.07.png) (image/png, 172.6 KB)

## Timeline

### mb...@chromium.org (2015-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-01-22)

This seems to be navigation related but I'm not sure if there is an omnibox angle to it as well, so adding both labels.

The bug/feature is that entering http://.example.com in the omnibox initiates a search while navigating to the same url through a link (<a href="http://.example.com">test</a>) ends up at http://.example.com.

### [Deleted User] (2015-01-22)

Correct, but also, if the page at http://.example.com then transfers you to another URL, the omnibox will stay as ".example.com" and not showing the new URL in the omnibox. It will also show a green padlock even though you've been redirected to HTTP (if the ".example" was on HTTPS).





### me...@chromium.org (2015-01-22)

You are right, it seems possible to put the omnibox in all sorts of weird conditions with this bug (e.g. I managed to display a broken lock without the "https://" text). 

Increasing severity to high per our severity guidelines.

### cl...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-01-23)

CC'ing navigation and omnibox experts.

### pk...@chromium.org (2015-01-23)

This isn't actually an omnibox bug per se since the omnibox is simply showing the underlying navigation state reported to it by the navigation controller.

I think the issues here are around the navigation controller and the network stack.

### cl...@chromium.org (2015-01-26)

[Empty comment from Monorail migration]

### sl...@google.com (2015-01-26)

Tagging DNS; even with the Omnibox issues, the Chrome network stack shouldn't be passing this on to the lower layers.

### cl...@chromium.org (2015-02-05)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-02-05)

Charlie, can you please look at this? I don't understand why the omnibar wouldn't get updated after a refresh, but that is particularly concerning. Peter says the navigation controller is still reporting the old domain.

For the first part, we might want to file a separate bug, although I have to admit I don't entirely understand the attack scenario or what is being compromised by sending requests with different domain name resolutions vs host header values.

### cr...@chromium.org (2015-02-06)

Agreed that the redirect behavior is strange.  I'll look into the navigation side of why we aren't updating the last committed URL when the redirect commits.

@rsleevi or @davidben, can you file a bug for the dot-domain aspect of this in the network stack, and mark it as blocking this bug?  That will let us track the two issues separately.

### cr...@chromium.org (2015-02-06)

I dug into the navigation side a bit, and part of the problem seems to be due to virtual URLs on NavigationEntry.

We end up rewriting the initial URL to "fix" it, which causes us to treat the original URL as a virtual URL.  (Virtual URLs are used for things like chrome://settings and view-source:, where the actual URL differs from what we show in the omnibox.)  Because of the way that it was rewritten, we aren't updating the virtual URL after the redirect, so we don't show example.com.  That's very broken.

The code that rewrites the URL is in WillHandleBrowserAboutURL in chrome/browser/browser_about_handler.cc:
*url = url_fixer::FixupURL(url->possibly_invalid_spec(), std::string());

This drops the leading dot, but doesn't set reverse_on_redirect.  I'll need to dig further to understand the intent behind reverse_on_redirect, since it's very confusing.

I also find it interesting that most other cases in url_fixer::FixupURL don't lead to the same bug.  Some cases show the correct URL after a redirect (e.g., http:/foo or http:////foo), while other cases seem to get caught earlier in FilterURL and we show about:blank instead (e.g., http;//foo).

I'll continue to dig into this to understand how the cases differ and what the correct behavior should be.

[This analysis does not cover anything about the network side of this bug.]

### cr...@chromium.org (2015-02-07)

It seems that most of the other cases in url_fixer::FixupURL get fixed before arriving in the browser process anyway, either by Blink or by the IPC system's URL serialization logic.

I'm a bit skeptical of the FixupURL call in browser_about_handler.cc., actually, because the comments claim it's only needed for rewriting about: to chrome:.  It's clearly doing more than that.  For what it's worth, only doing that call if the URL's scheme is about: does prevent the specific spoof we're seeing here, though I'm not sure if it will handle all cases (or if there are other ones).

@msw: Can you check whether that's a sane change, since you have TODO on line 21 of browser_about_handler.cc just above that call?

### ms...@chromium.org (2015-02-07)

Sadly my TODO there can't be resolved as long as we plan to continue supporting about:settings => chrome://settings and similar navigations, but that's hardly related.

Unfortunately, I'm not sure what fixup, if any, WillHandleBrowserAboutURL is expected to perform for non-"about URL" cases. It's probably okay to limit fixup to URLs that appear to have "about:", "chrome:", and possibly "view-source:" schemes.

That said, there are quite a few callers of url_fixer::FixupURL, and I suspect we should fix the underlying defect in fixup rather than avoiding fixup in this one instance.

### rs...@chromium.org (2015-02-07)

[Empty comment from Monorail migration]

### cb...@chromium.org (2015-02-10)

+ttuttle for more context with https://crbug.com/chromium/456391

### cr...@chromium.org (2015-02-11)

@msw: Thanks for the update, though I'm still quite puzzled by the about: rewriting.  It looks like about: URLs get rewritten to chrome: URLs much earlier than NavigationController::CreateNavigationEntry in almost all cases (apart from some tests).  That also explains why the about: prefix doesn't stay in the virtual URL, as it would if CreateNavigationEntry were responsible for that rewriting.

At any rate, it's quite wrong to be calling FixupURL during CreateNavigationEntry if it hasn't been called beforehand.  Any small tweaks it makes to the URL will cause use to track the original URL as a virtual URL, and thus lead to this spoof.

If we do need to call it within WillHandleBrowserAboutURL, then perhaps we can call FixupURL before doing the determination of the virtual URL.  We just don't want that fixup to be something that causes a virtual URL to be used.

I'll keep looking at options here, since it's important but non-trivial to get right.

### ms...@chromium.org (2015-02-11)

Ensuring that FixupURL (or otherwise equivalent/sufficient fix-up) occurs earlier than CreateNavigationEntry could make the call to FixupURL in WillHandleBrowserAboutURL unnecessary, but I can't say if that's the correct change. But still, I wonder if there's an underlying defect in FixupURL that's causing this particular fix-up to occur (maybe those URLs shouldn't be altered, maybe other fixup codepaths should be altering them earlier). Sorry I'm not terribly helpful here, I didn't dig this deep when I cleaned up our about: and chrome: URLs.

### cr...@chromium.org (2015-02-13)

@msw: That's fine; I appreciate your comments so far.  I've investigated a few options and I think I have a preference.  The main observation is that we already rewrite about: to chrome: earlier than CreateNavigationEntry in almost (but not all) cases, such that you'll never see about:foo in the address bar.

Here's the options I considered and my reasoning:

1) Simply remove the FixupURL call from WillHandleBrowserAboutURL.
Most paths in practice seem to call FixupURL before getting there, so it would be nice if it wasn't needed.  We don't call it for URLs from the renderer, but the renderer treats all about: URLs as about:blank already.
Unfortunately, this didn't work (https://codereview.chromium.org/914923002/) because many tests navigate to about: URLs without going through FixupURL.

2) Get all the call sites to call FixupURL, then do (1).
This kind of brute forces the first option, but it's fragile in two ways.  First, any rewriter in the future that adds a FixupURL call might re-introduce the spoof.  Second, any new path that can get to CreateNavigationEntry without calling FixupURL would fail the CHECK in WillHandleBrowserAboutURL.

3) Change FixupURL to remove the leading dot rewriting.
@msw: You've suggested that this bug may be a flaw in FixupURL itself, but I don't see any evidence for that.  Removing leading dots seems reasonable to me, and any of the other cleanup actions it takes could equally lead to a URL spoof.  (So far, I haven't discovered any other attacks because either Blink or our IPC system happens to do the same URL cleanup before it gets to the browser process.  There's no guarantee that won't change, though.)

4) Have CreateNavigationEntry call FixupURL before doing the rewriting.
This lets the cleanup occur without forcing us to have a virtual URL.  In other words, the minor changes from FixupURL will be shown in the address bar, rather than what the user typed.  For all practical purposes, this doesn't change anything, since the omnibox code calls FixupURL early already.  Only tests seem to be affected.

I like (4) because any BrowserURLHandler rewriters can then safely call FixupURL without introducing the spoof, and because we also don't care whether callers CreateNavigationEntry call FixupURL first.

Caveats:
a) We need to punt to chrome/ to make the url_fixer::FixupURL call, since it's in a component and not in content/.
b) It would still be nice to remove the FixupURL call from WillHandleBrowserAboutURL, but I won't be able to do that.  (There are still lots of other callers of RewriteURLIfNecessary that don't guarantee it will be called first.)

Running try jobs with this idea here:
https://codereview.chromium.org/923183003/

### ms...@chromium.org (2015-02-13)

Could the other (yet unnamed) url-fixup that runs earlier also remove leading dots?
I wonder why the other url-fixup doesn't cover everything that FixupURL does.
We should have a single comprehensive url-fixup function, not piece-meal fixes.

Still, you might need somethinkg like (4) to cover other non-test codepaths.
But WillHandleBrowserAboutURL could possibly run the other/unified fixup.
Maybe WillHandleBrowserAboutURL could expect that arg URLs are already fixed?

### cr...@chromium.org (2015-02-13)

Even if we added leading-dot removal to Blink or IPC code, there's no guarantee that url_fixer::FixupURL will have identical behavior.  Some other difference might sneak through and cause a spoof.  With (4), we're guaranteed not to let those cleanup changes cause a virtual URL.

(I'm not sure I follow your second paragraph.)

### ms...@chromium.org (2015-02-14)

Hmm, Blink/IPC and FixupURL should all be as complete as possible, right?
I guess my second paragraph was just encouraging (2) as a reasonable option.

### cr...@chromium.org (2015-02-14)

Blink and IPC overlap in weird ways that I don't understand.  For example, Blink changes http:///foo to http://foo, but it doesn't touch "http://foo: 8080", which gets rewritten to the empty URL by the IPC system.  There's a long list of differences between them from my basic experiments, and I haven't dug into that code to see where the logic for either lives.

In other words, I think it might be difficult to make sure that they all do the same thing as FixupURL.

### cr...@chromium.org (2015-02-17)

+zea for context on code review.

### cr...@chromium.org (2015-02-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/94a977f6dc4714f49841db1c2d831ab53e557f15

commit 94a977f6dc4714f49841db1c2d831ab53e557f15
Author: creis <creis@chromium.org>
Date: Wed Feb 18 23:51:05 2015

Move URL fixup to a preliminary phase that doesn't affect virtual URLs.

Uses BrowserURLHandler since this depends on components and can't
live in content.

BUG=449829
TEST=See bug for repro steps.

Review URL: https://codereview.chromium.org/923183003

Cr-Commit-Position: refs/heads/master@{#316923}

[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/chrome/browser/browser_about_handler.cc
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/chrome/browser/browser_about_handler.h
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/chrome/browser/browser_about_handler_unittest.cc
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/chrome/browser/chrome_content_browser_client.cc
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/chrome/browser/sessions/session_restore_browsertest.cc
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/chrome/browser/sync/glue/synced_session.cc
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/chrome/browser/sync/test/integration/single_client_sessions_sync_test.cc
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/content/browser/browser_url_handler_impl.cc
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/content/browser/browser_url_handler_impl.h
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/content/browser/frame_host/navigation_controller_impl.cc
[modify] http://crrev.com/94a977f6dc4714f49841db1c2d831ab53e557f15/content/public/browser/browser_url_handler.h


### cr...@chromium.org (2015-02-19)

The URL spoof aspect should be fixed as of r316923.  We should be able to verify on tomorrow's canary.

rsleevi/ttuttle: Are we close to a fix on https://crbug.com/chromium/456391?

### [Deleted User] (2015-02-19)

Just joining in here. Great job! One question, if the https://crbug.com/chromium/456391 is the network part of this issue, would it be possible for me to get access to it aswell?
Thanks,
Frans

### cr...@chromium.org (2015-02-20)

@https://crbug.com/chromium/449829#c30: Yes, sorry about that!

It looks like the spoof is resolved in 42.0.2309.2 (today's Mac Canary).

I'm also having trouble repro'ing the first bug on the canary.  Can you check whether it's still possible (via data:text/html,<a href="http://.example2.s3.amazonaws.com/">Test</a>)?  Perhaps that's fixed as well.

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-25)

creis / frans (hey Frans!)

If/once you're happy with the fix in Canary, can you please mark this as fixed? 

creis: can you also comment on whether this change is one you'd like to push in any potential patch to M-41 or whether letting it roll into M-42 is the more sane option.



### [Deleted User] (2015-02-25)

Hi Tim!
From my end, this is fixed in Canary.
I now get:
Error code: ERR_NAME_NOT_RESOLVED
and before the DNS issue was fixed, I also saw that the omnibar changed when redirected.

Great job guys!

Regards,
Frans

### cr...@chromium.org (2015-02-25)

I'm not sure I understand how the DNS issue was fixed, since https://crbug.com/chromium/456391 is still open and https://codereview.chromium.org/919023003/ hasn't landed.

But I agree that the spoof is fixed and the original steps don't repro, so I'll close this bug.

As for M41, r316923 is a little larger than I'd like for a merge.  I could be convinced it's worth merging, but it seems like there's a mitigating factor: the attacker would need a URL on the victim origin that redirects to the attacker's own URL.  And most redirectors (e.g., goo.gl, bit.ly) will fail if there's a leading dot.  So from that standpoint, it might be ok to wait until M42.

@meacer, your thoughts?

### cl...@chromium.org (2015-02-25)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cr...@chromium.org (2015-02-26)

Note: this doesn't need a merge if it's M42, since it landed before the M42 branch.  Per https://crbug.com/chromium/449829#c35, I'll let @meacer help decide if we need it in M41.

### ti...@google.com (2015-02-26)

Thanks @creis for the detailed background.

@meacer: M41 is cut, so the question is whether or not we would want to ship this in a M41 patch. (I don't have a strong opinion here and okay for this to roll in with M42).

### me...@chromium.org (2015-02-26)

I agree with creis@, we can wait until M42.

### ti...@google.com (2015-03-05)

Good times.

### ti...@google.com (2015-03-05)

... even better times without a typo in the label.

### ti...@google.com (2015-04-09)

Hey Frans - $1000 for this report.

Notes from panel: "Not a full spoof, server also needs to respond to a host header with a leading dot".

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-04)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### ju...@chromium.org (2016-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### is...@google.com (2016-12-09)

This issue was migrated from crbug.com/chromium/449829?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>DNS, UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail blocked-on: crbug.com/chromium/456391]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081211)*
