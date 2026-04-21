# SameSite cookie bypass via redirect

| Field | Value |
|-------|-------|
| **Issue ID** | [40091031](https://issues.chromium.org/issues/40091031) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies |
| **Platforms** | Mac |
| **Reporter** | s....@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2018-04-06 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
1. Go to https://shhnjk.azurewebsites.net/SameSite.php (Sets SameSite cookie)
2. Copy https://test.shhnjk.com/location.php?url=https://shhnjk.azurewebsites.net/SameSite.php and paste it to new tab

What is the expected behavior?
SameSite cookie not sent

What went wrong?
Redirect from attacker page to victim site doesn't prevent SameSite cookie to be sent.

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: OS X 10.13.4
Flash Version:

## Timeline

### ji...@chromium.org (2018-04-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network>Cookies]

### ji...@chromium.org (2018-04-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### el...@chromium.org (2018-04-09)

Neat!

Do you have a way to reproduce this that does NOT involve the user entering something in the omnibox?

(It's already possible to circumvent same-site with non-default user interactions. For instance, middle-clicking on a link to open in a new tab sends samesite=strict cookies).

### s....@gmail.com (2018-04-09)

>Do you have a way to reproduce this that does NOT
>involve the user entering something in the omnibox?
I don’t know anyway to do it with server side redirect. But I have 2 other variations that I haven’t reported yet. I was thinking to report it after checking the fix because nooperner bug might kill them all. But if you want, I can report them all.

### el...@chromium.org (2018-04-09)

Yes, please do report them all... playing whack-a-mole with fixes is less efficient and leaves users more at risk.

### s....@gmail.com (2018-04-09)

Filed the most interesting one (https://crbug.com/chromium/830799) and least interesting one (https://crbug.com/chromium/830808).
I have some more idea which I will test it later.



### s....@gmail.com (2018-04-12)

>(It's already possible to circumvent same-site with non-default user interactions. For
>instance, middle-clicking on a link to open in a new tab sends samesite=strict cookies)
Interestingly, Firefox Nightly doesn't send SameSite Strict cookie even if you Ctrl + Click the link or Right click + open in a new Tab.

I would love to know what's the correct behavior per spec on this.

### ca...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-04-23)

Re: https://crbug.com/chromium/830101#c3
>Do you have a way to reproduce this that does NOT involve the user entering something in the omnibox?

Redirect within iframe also works.

https://shhnjk.azurewebsites.net/iframer.php?url=https://test.shhnjk.com/location.php?url=https://shhnjk.azurewebsites.net/SameSite.php

### s....@gmail.com (2018-04-27)

Step 3 of Document-based requests (https://tools.ietf.org/html/draft-ietf-httpbis-cookie-same-site-00#section-2.1.1) algorithm says:
`Let "documents" be a list containing "document" and each of "document"'s ancestor browsing contexts' active documents.`

But redirect response doesn't have an active document.

### ts...@chromium.org (2018-05-03)

Mike, are you the person handling these same-site cookie issues?  Thanks.

### sh...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### oc...@chromium.org (2018-06-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-09-13)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### mk...@chromium.org (2019-02-12)

CCing some folks who might have bandwidth.

### rs...@chromium.org (2019-03-02)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-03-04)

Isn't this working as expected?  Lax cookies should be sent for top-level redirects (And I think that's the whole point of the Lax vs Strict distinction?).  Not sure about the iframe case.

### s....@gmail.com (2019-03-06)

Strict cookie is also being sent, which is the issue in this bug.

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### oc...@google.com (2019-07-25)

[Empty comment from Monorail migration]

### oc...@google.com (2019-07-25)

Any updates on this bug? We just got another report in https://crbug.com/chromium/987388

### oc...@google.com (2019-07-26)

[Empty comment from Monorail migration]

### mk...@chromium.org (2019-07-31)

+chlily@: Can you triage this, please?

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ch...@chromium.org (2019-07-31)

The SameSite context is being computed incorrectly because we update the site_for_cookies on the redirect, but the initiator here isn't being set properly (it's still null on the redirect). The initiator check is the only difference between returning strict/lax, so we can't distinguish between strict and lax correctly if the initiator isn't set.

### ch...@chromium.org (2019-08-01)

mkwst: What is the desired behavior for (main frame) cross-site redirects? I'm having a bit of trouble understanding what the spec says about them.

I have a CL in the works that:
* does not send Strict cookies to b for a->b redirects,
* does not send Strict cookies to a (the second time around) for a->b->a redirects,
* does not send Strict cookies on any redirect that has had a cross-origin redirect anywhere along the chain.

Does that match the requirements of the spec?

### ch...@chromium.org (2019-08-01)

On second thought, s/origin/eTLD+1/. So an a.com->sub.a.com redirect would send Strict cookies.

### ch...@chromium.org (2019-08-02)

Huh. Apparently there are WPTs that disagree with me. 

https://cs.chromium.org/chromium/src/third_party/blink/web_tests/external/wpt/cookies/samesite/fetch.html?l=31
  create_test(ORIGIN, redirectTo(CROSS_SITE_ORIGIN, ORIGIN), SameSiteStatus.STRICT, "Cross-site redirecting to same-host fetches are strictly same-site");

Mike, I would appreciate it if you could clarify what is supposed to happen here?

### ch...@chromium.org (2019-08-09)

Ok, after talking with Mike, it seems this is working as intended.

Because the first navigation is initiated from the omnibox, we can consider this a browser-initiated navigation so Strict cookies should be sent.

Thanks for the bug report though! Please let us know if you find any other possible SameSite bugs.

### s....@gmail.com (2019-08-09)

Have you also looked into example of https://crbug.com/chromium/830101#c9?

### ch...@chromium.org (2019-08-09)

I believe the example in https://crbug.com/chromium/830101#c9 is the same case as reported in https://crbug.com/937238 which is also working as intended, apparently.

### s....@gmail.com (2019-08-09)

Redirect inside iframe sends Strict cookie. So AFAICT, you are saying that any website that embed other site has potential SameSite Strict cookie bypass? That's ... great :)

### mm...@chromium.org (2019-08-09)

Suppose you have more control over who you embed than who tries to embed you, but yea, seems surprising to me, too.

### lu...@chromium.org (2019-08-12)

I am not sure how much can be done for browser-initiated navigations (with request_initiator=none).  Some aspects of this are being discussed in https://crbug.com/chromium/946505 and https://crbug.com/chromium/946501 (in context of Sec-Fetch-Site, but I think the outcome should also apply to SameSite cookies by virtue of it also being based on request_initiator).

OTOH, it seems to me that we *can* fix things for website-initiated navigations/requests (including subframe navigations like in https://crbug.com/chromium/830101#c9 here).  I note that Sec-Fetch-Site algorithm specifically considers redirects (e.g. see https://github.com/w3c/webappsec-fetch-metadata/issues/28) to protect itself against this kind of attacks - maybe SameSite-cookie algorithm should also do something similar (although this probably would have to be treated as a breaking change...).  FWIW, I don't see any hits for "redirect" on https://tools.ietf.org/html/draft-west-first-party-cookies-07.

### mm...@chromium.org (2019-08-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### aj...@google.com (2019-10-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### mk...@chromium.org (2020-02-20)

Elsewhere, Anne noted:

"""
We fixed an equivalent bug in https://bugzilla.mozilla.org/show_bug.cgi?id=1453814 but the cookie drafts have changed quite a bit since then and Chrome doesn't follow the old draft at least. And now we're getting compat issues.
"""

### ch...@chromium.org (2020-02-25)

mkwst: I'm happy to make the changes if you tell me what the correct behavior should be.

I believe Chrome's current implementation is correct for this scenario. The spec currently bases the same-site/cross-site calculation (https://tools.ietf.org/html/draft-ietf-httpbis-rfc6265bis-05#section-5.2) on the request's client, and as far as I can tell, the request's client is not updated on a redirect (https://fetch.spec.whatwg.org/#http-redirect-fetch). Please let me know if that's wrong.

IIRC, the last time we spoke about this, the concern was that dropping these cookies would break stuff like companies' internal shortlinks.

### an...@gmail.com (2020-02-25)

I think there's two separate problems as also noted upthread:

1. User-initiated top-level navigation that redirects. I'm inclined to agree that sending cookies there is probably fine.
2. Framed navigation that redirects: https://shhnjk.azurewebsites.net/iframer.php?url=https://test.shhnjk.com/location.php?url=https://shhnjk.azurewebsites.net/SameSite.php. Chrome's cookie sharing here seems rather problematic.

### ch...@chromium.org (2020-02-25)

For 2, that was addressed separately here (https://crbug.com/937238) and the conclusion at the time was that A framing [B->A redirect] should send SameSite cookies on the redirected request to A, as that is an A frame inside of A, which is same-site. I'm still having trouble reading the spec in a way that suggests anything should change on redirects.

My first thought at the time was that it seemed intuitively incorrect to allow SameSite cookies in the framed redirect case, but I was then convinced that it was correct. Willing to be convinced back again... I agree that if we're having compat problems across browsers, we should align on something and update the spec if it's unclear.

### an...@gmail.com (2020-02-25)

Thanks chlily, that's helpful!

My unease with the "Chrome model" is that elsewhere we do try to be "strict" about these kind of redirects as they can theoretically influence the target page in unexpected ways that compromise its security. See also https://github.com/whatwg/fetch/issues/737.

I also have a hard time pinpointing where the specification deals with the source of a request (rather than ancestor documents), but it does claim to care about CSRF and I don't think this adequately defends against CSRF. If instead of doing redirects, B would navigate to A, would the cookies then also be included? The explanatory section suggests that for strict cookies that ought not to work, but the normative algorithm is rather unclear on this to me. And I'm not sure how to distinguish a redirect from B to A from B navigating to A threat-model-wise. Both seem equally bad.

Hope that helps.

### ch...@chromium.org (2020-02-25)

I think it would make sense to treat redirects as if they were navigations. I'm not sure how to work that into the spec in a reasonable way. I'd guess we'd have to define it based on something other than the request's client, which isn't updated on redirects. Maybe it makes sense to also incorporate the request's url list, mirroring the sec-fetch-site definition of "same-site"?

For more SameSite vs redirect fun, see also:
https://github.com/httpwg/http-extensions/issues/593
https://github.com/httpwg/http-extensions/issues/889
https://github.com/httpwg/http-extensions/issues/773

### lu...@chromium.org (2020-02-25)

RE: https://crbug.com/chromium/830101#c55:

I think I agree that it is desirable for strict SameSite cookies to behave consistently with Sec-Fetch-Site (wrt handling of redirects).

OTOH, right now Sec-Fetch-Site does track redirect hops, but the redirecting servers do not replace initiators - instead the initiator is compared with each intermediate target and the safest minimum (cross-site < cross-origin < same-origin) is used [1,2].  AFAIU this is different from what https://crbug.com/chromium/830101#c54 and https://crbug.com/chromium/830101#c55 want - I think they want the intermediate servers to replace the initiator, not the target.

[1] See the std::max usage in https://chromium.googlesource.com/chromium/src/+/1309ed3cd6027d82c3780aae0c42de7704825833/services/network/sec_header_helpers.cc#105
[2] https://www.w3.org/TR/fetch-metadata/#sec-fetch-site-header

### an...@gmail.com (2020-02-26)

[Empty comment from Monorail migration]

### ch...@chromium.org (2020-02-26)

I think I had tried modifying the initiator on redirect hops at one point, but it broke some other stuff that depends on initiator origin. Maybe we just need a separate SameSite-cookie-specific initiator field? It's possible that we could just look at the URLRequest's redirect chain, since it seems that document.cookie doesn't look at the initiator anyway.

### mm...@chromium.org (2020-02-26)

Note that URLRequest doesn't currently have the full redirect chain - extensions (and maybe ServiceWorker - think other things, too) can intercept the request and redirect it, and we lose the entire pre-existing chain when that happens.

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### aj...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### aj...@google.com (2020-04-20)

Marshal ping: any progress on this samesite redirection problem? 

### ch...@chromium.org (2020-04-20)

I don't think anyone is actively working on this, so no.

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ch...@chromium.org (2020-12-29)

There is a spec change that addresses this issue: https://github.com/httpwg/http-extensions/pull/1348

I'm now working on incorporating the redirect chain into the Strict context calculation to align with the spec change.

### ch...@chromium.org (2021-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/306b8fba167a809c5389a58d65bee438ca3bd15d

commit 306b8fba167a809c5389a58d65bee438ca3bd15d
Author: Lily Chen <chlily@chromium.org>
Date: Mon Mar 08 22:31:23 2021

SameSite cookies: Consider redirect chain for same-site requests

The cookie spec is being amended in
https://github.com/httpwg/http-extensions/pull/1348
to consider the redirect chain when computing whether a request is
considered same-site.

This aligns with the new specification by considering a request cross-
site if any URL in the redirect chain was cross-site from the current
request URL.

Bug: 830101
Change-Id: I060026647ccea2a97267e865c8292ac64915e87b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2605504
Commit-Queue: Lily Chen <chlily@chromium.org>
Reviewed-by: Maksim Orlovich <morlovich@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#860890}

[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/content/browser/devtools/devtools_url_loader_interceptor.cc
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/content/browser/net/http_cookie_browsertest.cc
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/net/cookies/cookie_util.cc
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/net/cookies/cookie_util.h
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/net/cookies/cookie_util_unittest.cc
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/net/url_request/url_request_http_job.cc
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/net/url_request/url_request_unittest.cc
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/third_party/blink/web_tests/external/wpt/cookies/samesite/fetch.https.html
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/third_party/blink/web_tests/external/wpt/cookies/samesite/form-get-blank.https.html
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/third_party/blink/web_tests/external/wpt/cookies/samesite/form-post-blank.https.html
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/third_party/blink/web_tests/external/wpt/cookies/samesite/img.https.html
[modify] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/third_party/blink/web_tests/external/wpt/cookies/samesite/multiple-samesite-attributes.https.html
[add] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/third_party/blink/web_tests/http/tests/inspector-protocol/fetch/fetch-samesite-cookies-expected.txt
[add] https://crrev.com/306b8fba167a809c5389a58d65bee438ca3bd15d/third_party/blink/web_tests/http/tests/inspector-protocol/fetch/fetch-samesite-cookies.js


### ad...@google.com (2021-03-10)

chlily@ thanks for working on this really long-standing security bug. Yay! Do you consider https://crbug.com/chromium/830101#c75 to be a complete fix? If so please mark the bug as fixed so we can start the processes to credit and/or reward the reporter properly.

### ch...@chromium.org (2021-03-10)

It's like 95% of a fix (the remainder is that, if the page is reloaded by the browser following a cross-site redirect, we're suppose to treat it as cross-site, but since we lose the redirect chain at that point there's no easy way to do that. I don't have any plans to tackle this issue at this time, since it seems edge-casey.)

I would also be cautious about this causing lots of web breakage, especially around logins and payments. We may end up having to revert it and/or roll out out slowly/add a finch kill-switch due to the potential for web incompatibility.

Tl;dr: I would keep this open at this time.
(Feel free to reward the reporter though. I don't really know how that process works.)

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ch...@chromium.org (2021-03-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-06)

chlily@ thanks. It's fine with me to keep this open, though we'll only send it to the VRP panel when the bug is finally marked fixed. The alternative is to mark this as Fixed and raise a new crbug for the edge-case.

### ch...@chromium.org (2021-04-13)

[Empty comment from Monorail migration]

### ch...@chromium.org (2021-04-13)

I filed https://crbug.com/1198620 for the refresh case.

### [Deleted User] (2021-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-29)

Congratulations! The VRP Panel has decided to award you $3000 for this report. Nice job! 

### s....@gmail.com (2021-04-29)

Thanks!

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/830101?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Internals>Network>Cookies]
[Monorail mergedwith: crbug.com/chromium/1012942, crbug.com/chromium/855360, crbug.com/chromium/883661, crbug.com/chromium/896483, crbug.com/chromium/937271, crbug.com/chromium/987388, crbug.com/chromium/995117]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091031)*
