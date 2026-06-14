# SameSite cookie bypass via prerender

| Field | Value |
|-------|-------|
| **Issue ID** | [40091073](https://issues.chromium.org/issues/40091073) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader>Preload, Blink>SecurityFeature, Internals>Network>Cookies, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | ry...@chromium.org |
| **Created** | 2018-04-11 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
1. Register SameSite Strict cookie to your site.
2. Host attached file somewhere and change your-site to the site where you registered SameSite Cookie
3. Open hosted page

What is the expected behavior?
SameSite cookie not sent

What went wrong?
SameSite Strict cookie is sent with <link rel="prerender">

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: 10 RS3
Flash Version:

## Attachments

- [bypass.html](attachments/bypass.html) (text/plain, 50 B)

## Timeline

### s....@gmail.com (2018-04-11)

Okay, I have easy repro.

1. Go to https://shhnjk.azurewebsites.net/SameSite.php
2. Now go to https://test.shhnjk.com/samepre.html

You will see "Received Secret". Which is loaded from pre-rendered cache.

### ca...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature Internals>Network>Cookies]

### ca...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

### jo...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>Loader>Preload]

### ts...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-05-22)

I think this is the best bypass I have for SameSite cookie. So I would like to disclose this in November :)

mkwst@, Do you think prerender should send Lax? Or nothing at all? I would like to align this to not to send any SameSite cookie. But your spec seems to have doubt on it. What's your thought here?

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### mk...@chromium.org (2019-02-12)

CCing some folks who might have bandwidth.

### lu...@chromium.org (2019-05-23)

Most likely this is also a Sec-Fetch-Site bypass (since AFAIK both SameSite cookies and Sec-Fetch-Site both rely on network::ResourceRequest::request_initiator).

[Monorail components: Internals>Sandbox>SiteIsolation]

### lu...@chromium.org (2019-05-23)

tbansal@, would you be able to take a look please?  (since in the recent prerender discussion on chrome-security-owp@ I see that you've volunteered to look into prerender bugs :-)

### tb...@chromium.org (2019-05-28)

[Empty comment from Monorail migration]

### ry...@chromium.org (2019-05-28)

[Empty comment from Monorail migration]

### tb...@chromium.org (2019-05-28)

I'm confused as to why prerender would skip SameSite cookie checks since prerender uses the same code path as an actual page load.

### ry...@chromium.org (2019-05-28)

I was able to repro this inconsistently. I was also able to repro this inconsistently by just having a frame without the prerender and refreshing both tabs to try to get the cache to serve the iframe rather than use the network for the iframe.

The easiest way for me to consistently repro this:
(a) open https://shhnjk.azurewebsites.net/SameSite.php
(b) open a page that has a frame to https://shhnjk.azurewebsites.net/SameSite.php
(c) close page from (b)
(d) refresh page from (a)
(e) tab restore page closed in (c)
(f) Note: "Received Strict!!!" and "Received Lax!" in the frame where "No cookie received" is expected

I am hosting the page in (b) off my file system though (not HTTP or localhost), so this may not actually work on a real page.

This should be fixed by 2 key caching, and I think that is the best approach to fix this, it should just silo the frame in cache and prevent this entirely. NoStatePrefetch uses the main frame host in 2 key caching.

### ry...@chromium.org (2019-05-28)

Confirmed 2 key caching (i.e., --enable-features=SplitCacheByTopFrameOrigin) resolves the repro I described.

### ry...@chromium.org (2019-05-28)

jkarlin, FYI that spltting cache appears to fix this issue.

### s....@gmail.com (2019-05-28)

How does 2 keyed cache fix this issue? 
And getting cache fetched in prerender is not the purpose of this attack. Rather making prerender request with SameSite cookies is the attack (because SameSite cookies is a mitigation of CSRF).

### ry...@chromium.org (2019-05-28)

Using your repro as an example:

With 2 key caching on, a prerender will be put in shhnjk.azurewebsites.net's cache. When the iframe from https://test.shhnjk.com/samepre.html tries to load https://shhnjk.azurewebsites.net/SameSite.php, it will not be in test.shhnjk.com's cache, so it will need to be fetched in the context of test.shhnjk.com. When fetching again, it will use the SameSite cookie rules correctly.

Can you run Chrome with --enable-features=SplitCacheByTopFrameOrigin and see if you can repro this issue?

### s....@gmail.com (2019-05-29)

Yes, I can repro this issue with --enable-features=SplitCacheByTopFrameOrigin. Please use the first repro attachment, and you will see prerender request with SameSite cookie attached.

### ry...@chromium.org (2019-05-29)

I expect all prerender requests to be treated as top level requests (main frame requests), so SameSite cookie should be attached. It is surprising to see that the a sub-frame request on a different origin page would use any resource from the prerender under 2 key caching. All resources from the prerender should be put in the cache of the prerender URL's host, so should be inaccessible to any other host. AFAIK, prerender doesn't have any special ability to use anything other than the disk cache to speed up navigations.

Just to confirm,  SplitCacheByTopFrameOrigin should be available on version 73.*+. Are you on a version of Chrome (chrome://version) that is older than 73.*?

I will continue to look at this tomorrow.

### s....@gmail.com (2019-05-29)

[Comment Deleted]

### s....@gmail.com (2019-05-29)

>I expect all prerender requests to be treated as top level requests (main frame requests), so SameSite cookie should be attached
This is wrong. When prerender is initiated from cross-site, this should surely not attach the SameSite Strict cookie.

>It is surprising to see that the a sub-frame request on a different origin page would use any resource from the prerender under 2 key caching.
You are missing the point. I haven't tested to reuse prerender cache. I just tested that prerender request to cross-site endpoint will attach SameSite Strict cookie. I didn't test if that cache is usable because that's not the point of this bug.

### ry...@chromium.org (2019-05-29)

I believe I understand now the difference between strict and lax. This cookie should not be added to prerender because it should not be added to any navigation originating from any cross origin host. I will look into how the referrer/originator is being set on prerender requests to handle the Strict case (right now it acts like lax).

### ry...@chromium.org (2019-05-29)

Now that I understand the background of the problem more, I can consistently repro this with dev tools to prerender and then window.location change to check the result.

I believe I have a fix.

Specifically, when I prerender and then navigate to your page with the fix, I am only getting the Lax cookie. Whereas, without the fix the same steps get Lax and Strict cookies. That seems correct, but I am not sure I entirely understand Strict vs Lax. Can you confirm this is the correct behavior?

### s....@gmail.com (2019-05-29)

That's correct in main frame navigation (i.e. top-level browsing context), but if cache will be used inside iframe, it shouldn't send a Lax cookie too. And I assume it's almost impossible to fix it as when prerender request is made, there's no information about where this prerender cache will be used (top frame or nested frame). And this is also mentioned in the spec: https://tools.ietf.org/html/draft-ietf-httpbis-cookie-same-site-00#section-4.1.1

### ry...@chromium.org (2019-05-29)

Yes, there are two problems here. Two key cache addresses one and my forthcoming fix addresses the other.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d154e1e7cfe7cb505dff0ac7a985c830309a092c

commit d154e1e7cfe7cb505dff0ac7a985c830309a092c
Author: Ryan Sturm <ryansturm@chromium.org>
Date: Sat Jun 01 01:18:59 2019

Prerender should pass in an origin that initated the prerender

This will allow SameSite cookies that are marked as Strict to behave
consistently with top level navigation behavior and SameSite spec.

The origin is plumbed from blink::Document through the prerender
pipeline, and is passed into LoaderParams.

This CL addresses the <link rel="prerender"> case, but does not
address the Omnibox or other browser initiated navigations.

Bug: 831725
Change-Id: I444186a26955cff241eb5fcd186b3f650753a65b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1635862
Reviewed-by: Lei Zhang <thestig@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Tarun Bansal <tbansal@chromium.org>
Commit-Queue: Ryan Sturm <ryansturm@chromium.org>
Cr-Commit-Position: refs/heads/master@{#665383}

[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/bad_message.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_contents.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_contents.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_link_manager.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_link_manager.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_manager.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_manager.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_message_filter.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_message_filter.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_nostate_prefetch_browsertest.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_test_utils.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_test_utils.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/browser/prerender/prerender_unittest.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/common/prerender_messages.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/chrome/renderer/prerender/prerender_dispatcher.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/third_party/blink/public/platform/web_prerender.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/third_party/blink/renderer/core/loader/private/prerender_handle.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/third_party/blink/renderer/platform/exported/web_prerender.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/third_party/blink/renderer/platform/prerender.cc
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/third_party/blink/renderer/platform/prerender.h
[modify] https://crrev.com/d154e1e7cfe7cb505dff0ac7a985c830309a092c/tools/metrics/histograms/enums.xml


### ry...@chromium.org (2019-06-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-03)

[Empty comment from Monorail migration]

### ry...@chromium.org (2019-06-20)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### aw...@google.com (2019-07-31)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $2,000 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-09-06)

Assuming this affects all the normal platforms.

### sh...@chromium.org (2019-09-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/831725?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader>Preload, Blink>SecurityFeature, Internals>Network>Cookies, Internals>Sandbox>SiteIsolation]
[Monorail blocking: crbug.com/chromium/786673, crbug.com/chromium/843478, crbug.com/chromium/979231]
[Monorail mergedwith: crbug.com/chromium/976525]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091073)*
