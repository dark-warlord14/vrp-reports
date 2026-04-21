# Unintended Data Leakage Through HTTP Request Headers

| Field | Value |
|-------|-------|
| **Issue ID** | [40051073](https://issues.chromium.org/issues/40051073) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>WebView |
| **Platforms** | Android |
| **Reporter** | sh...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2019-12-27 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

While performing the security review it has been observed that in Chromium-based webviews if a webpage is loaded with some additional headers using loadUrl(String url, Map<String, String> additionalHttpHeaders) then it sends the additional headers to any other requests triggered in the process of loading the URL such as redirects. The behaviour is similar to Chromium Bug(<https://bugs.chromium.org/p/chromium/issues/detail?id=306873>) reported in 2013 which is marked as fixed.

**VERSION**  

Chrome Version: 78.0.3904.108  

Operating System: Android 9, API Level 28

**REPRODUCTION CASE**  

As per the Google Docs Ref: <https://developer.android.com/reference/android/webkit/WebViewClient#shouldOverrideUrlLoading(android.webkit.WebView,%20android.webkit.WebResourceRequest)>

```
Note: Do not call WebView#loadUrl(String) with the request's URL and then return true. This unnecessarily cancels the current load and starts a new load with the same URL. The correct way to continue loading a given URL is to simply return false, without calling WebView#loadUrl(String).  

```

In the scenario wherein the suggested approach is used i.e. shouldOverrideUrlLoading is overridden to simply return false the subsequent request would be having the headers attached to the original request.

It has been also observed that while shouldOverrideUrlLoading is invoked and an attempt to access the request headers is made using WebResourceRequest.getRequestHeaders() method a null pointer is returned. However, if the request is observed using a proxy/webview debugging tools it contains the headers added to the initial request.

Impact  

This would lead to unintended data leakage causing the leakage of sensitive data such as auth tokens sent as a part of HTTP request headers, especially during oAuth flows.

Steps To Reproduce  

The proof of concept code attached to the report is an Android application(Webview POC.zip) that has a webview component. The component loads the webpage with additional header(Authorization). The loaded webpage is expected to return an HTTP-302 redirect response(Use app.py) and you will observe that the Authorization header is also sent to the redirected request. You will also observe 'IsNull' in the Android application logs as a null pointer is returned when an attempt is made to dump the request headers programmatically

**CREDIT INFORMATION**  

Reporter credit: Shiv Sahni, Movnavinothan V and Imdad Mohammed

## Attachments

- [app.py](attachments/app.py) (text/plain, 318 B)
- [Null Pointer While Dumping Request Headers.png](attachments/Null Pointer While Dumping Request Headers.png) (image/png, 343.5 KB)
- [Original Request.png](attachments/Original Request.png) (image/png, 1.0 MB)
- [Redirtect Request.png](attachments/Redirtect Request.png) (image/png, 1.0 MB)
- [Webview POC.zip](attachments/Webview POC.zip) (application/octet-stream, 27.3 MB)
- [Android Webview Security Issue.pdf](attachments/Android Webview Security Issue.pdf) (application/pdf, 713.3 KB)

## Timeline

### ad...@google.com (2019-12-27)

Thanks for the report!

From https://bugs.chromium.org/p/chromium/issues/detail?id=306873#c9 it looks like the extra headers *are* sent through redirects (given the comments in https://bugs.chromium.org/p/chromium/issues/detail?id=306873#c15 that they tried to make the Chromium-based WebView compatible with that older behavior.) At least that's my understanding of the older ticket.

However, I think this will need torne@ to take a look to decide what the correct behavior is.

torne@, I haven't attempted to reproduce this so this remains in "Unconfirmed" state but it would be great to have your comments.

[Monorail components: Mobile>WebView]

### sh...@chromium.org (2019-12-27)

[Empty comment from Monorail migration]

### sh...@gmail.com (2020-01-02)

Hey Ade Taylor,

Any idea by when can we hear from @torne seems he is vacationing until Jan.

### ad...@google.com (2020-01-02)

Hi shivahni2@, thanks again for the report. There are a lot of people out on vacation this week - normal service will resume on Monday. I don't expect we'll get a reply until the first few days of next week.

### to...@chromium.org (2020-01-06)

This is working as intended for compatibility with past versions of WebView, and it's unclear whether we would be able to change this behaviour without breaking applications.

I'll discuss with the team what we want to do here.

### dr...@chromium.org (2020-01-06)

Security sheriff here - if this is currently working as intended, should we drop the security labels?

### sh...@gmail.com (2020-01-07)

Hey Security Sheriff,

Request you to kindly have a look at the report I shared. I think you being security guy will get a better picture about the impact pertaining to the intended functionality. The intended feature would be leading to disclosure of HTTP headers including sensitive auth tokens. I have seen this happening in lots of organisations and I believe this must be fixed at the webview API itself.

As per the official developer guidelines simply returning false is a suggested approach to use shouldOverrideUrlLoading method. Since by default we are sending additional headers to the redirects this causes the webview to send the headers to the redirect_urls. This is causing unintended data leakage to third-parties when a HTTP-302 redirect response is sent especially during oAuth flows. 

Furthermore, when we try to dump the headers from the WebResourceRequest object we get a null pointer whereas the headers are actually sent in the HTTP request which again indicates a buggy behaviour.





### to...@chromium.org (2020-01-07)

This issue is in the (unfortunately rather large) category of "intentional WebView behaviours that result in some app developers introducing security vulnerabilities into their app due to not expecting that behaviour" - it's an API sharp edge that is relevant for security :(

The documentation for this overload of loadUrl states:

"additionalHttpHeaders	Map: the additional headers to be used in the HTTP request for this URL, specified as a map from name to value."

This is misleading at best: it states "for this URL" when the actual behaviour is "for the top level document load beginning at this URL" (i.e. it is used for the duration of the navigation triggered by this loadUrl call, but only for requests to fetch the top level document, not any subresources). However, this has *always* been the behaviour, so it's quite possible that some existing apps depend on this behaviour - https://crbug.com/chromium/306873 describes how the new WebView implemented it intentionally for compatibility with the old one, but doesn't cite any specific app/use case where it was needed.


So, the options here that I can think of would be:

1) Remove this behaviour entirely and only send the headers in the initial request. This would eliminate the data leakage in any app that currently has this problem, but may break compatibility with an unknown set of other applications.

2) Leave the behaviour alone since it's always been like this, and update the documentation to explicitly describe exactly which network requests will carry the added headers and which will not, and add WebView tests verifying all those cases to ensure the implementation continues to match the docs.

3) Change the implementation so that the headers are only sent if the current redirect URL has the same origin as the original URL passed to loadUrl. This should fix the data leakage in the vast majority of cases where it exists, but may still break compatibility with a likely-smaller unknown set of other applications.

It's not really possible to estimate the compatibility risk of either 1 or 3 meaningfully with the information we currently have; we don't record any metrics for how often this overload of loadUrl is used at all, nor how often it encounters one or more (cross-origin or not) redirects. We could add those metrics, but it would take some time for enough data to be collected to be useful, and it still wouldn't tell us how many of these cases would actually break if we changed the behaviour, only the upper bound on how many potentially *could* break.


One question I have here for shivsahni2: you mention OAuth flows as a case where this may be a security issue, and while I understand that OAuth usually involves cross-origin redirects between parties that aren't mutually trusting, I'm not aware of a pattern for implementing OAuth that would rely on an app initiating the request by passing additional headers through loadUrl - in cases where the OAuth flow is being performed via browser-side redirects, it seems to be most common that the authorization server identifies the client via already-existing login cookies, rather than an explicitly-sent access token. I'm totally willing to believe that there are specific app implementations that do rely on this and thus would be vulnerable to this data leakage, but if you're aware of a specific pattern/library/implementation that actually does, I'd like to hear any information you have about it, as it'd help us estimate how widespread this issue is likely to be.


In regards to shouldOverrideUrlLoading: the reason why we strongly discourage applications from implementing shouldOverrideUrlLoading by calling loadUrl(url) is that this causes all renderer-initiated navigations (e.g. redirects, JS location changes, clicking on links, etc) to be converted into browser-initiated navigations (which usually only includes explicit user actions like typing a URL, clicking on a bookmark, etc). This is itself a potential security/privacy risk: browser-initiated navigations are treated differently in various ways in Chromium (e.g. they may be considered to have a user gesture).

So it happens that if you *do* have this incorrect implementation of shouldOverrideUrlLoading then you will end up removing the headers from the requests following a redirect, because you'll be cancelling the original navigation before the redirect is actually followed and instead replacing it with a new navigation that doesn't have any extra headers specified, but that's incidental and apps still shouldn't do it.


In regards to WebResourceRequest.getRequestHeaders(), it has also always been the case that the set of headers returned may not include all the headers that are ultimately sent with the request if the app allows the request to continue as normal; this happens in a number of different cases in both shouldOverrideUrlLoading and shouldInterceptRequest, and is probably unlikely to change. We can't easily guarantee that all headers have been added at the point at which WebView intercepts the navigations/requests to offer them to the application; some are only added later (by the network stack itself, or other non-webview-specific code) once it's been determined that the request is going to proceed through the network stack as usual. The docs should probably mention this caveat. :/

### to...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

### sh...@gmail.com (2020-01-08)

I really appreciate the detailed and granular reply!

I understand that the option 2 appears to be the most feasible and quick option that we have to manage this issue and would definately help the new developers referring the docs. However, the veterans would be still following the same approach without knowing the adverse impact. Moreover, the applications which are already vulnerable would still be leaking the data to the third parties.

The oAuth use case I was referring involves the Android application integrating with other Service Providers/Partners on a single platform. The application opens the service providers sites in webview after sufficient validations. During validation the oAuth is performed and the application's backend verifies the user(auth token) and service provider(client id and redirect url) and only after successful validation it opens the service provider's site in the webview. Unfortunately, there is a very good number of such applications designed in such a way. Based on my observation, I have seen a notable growth in number of applications integrating other services. I would like to highlight that this even includes banking and other payments applications such as wallets which would be affected critically through this bug because of the monetary impact.


Lastly, I would request you to throw some more light on why usage of loadUrl in shouldOverrideUrlLoading causes a security issue. As of now I was considering this to be a workaround to not let the headers sent to the redirect URLs and if this causes security impact I'm afraid if we have any solution as of now to prevent this behaviour

### sh...@gmail.com (2020-01-13)

Hey Folks!

Any updates on this?


### to...@chromium.org (2020-01-13)

Quick update: the plan is to deploy metrics to see how often this is happening in the field and use that to judge the security risk vs compatibility risk. We're working on putting that together.

### mb...@chromium.org (2020-01-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-14)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@gmail.com (2020-01-15)

Hey guys!

I'm still wondering why we considered it to be a low severity issue. The impact of the issue can be serious wherein the auth tokens are leaked to the third-party. Moreover, there is no awareness around it as the official Google dev docs suggest to use the same approach that would trigger this security issue.

Also, I have plans of delivering a security training around Webview Hardening where I would like to include this case as well. Can you please let me know the ETA when I can go for the public disclosure around it?

Lastly, I wanted to know if this report is eligible for any reward?


### to...@chromium.org (2020-01-15)

Can you be more specific about which dev documentation suggests this? Are there examples that use the extra headers for authentication or other sensitive purposes? I couldn't find any.

### sh...@gmail.com (2020-01-16)

I was referring to the links that you already put in your initial reply namely:

https://developer.android.com/reference/android/webkit/WebViewClient#shouldOverrideUrlLoading(android.webkit.WebView,%20android.webkit.WebResourceRequest)

And

the definition of additionalHttpHeaders Map in the docs.

I hope now we are on the same page :)

Also, it would be great if you could provide the responses of the questions mentioned in my last reply.



### to...@chromium.org (2020-01-16)

I've spent a while digging in to the implementation of the extra header passing and the tests that cover its behaviour, and there's a number of general problems here.

The current implementation adds the headers in a number of cases that are surprising (even beyond the issue discussed here), and doesn't add them in other cases where you would most likely expect it to; it's virtually impossible to write a comprehensible description of exactly when they are added and when they aren't. Some of these cases appear to be intentional to match the old implementation's behaviour, but not all of them. So, leaving it exactly as-is and just fixing the documentation to accurately describe the current behaviour doesn't seem like a viable option, because the current behaviour is too complicated and weird.

In addition, the current implementation keeps every set of extra headers it is ever passed around for the lifetime of the process, effectively a memory leak if the URL isn't used again, and there's no straightforward way to fix that either.

There's another very similar feature already implemented in Chrome (extra headers in LoadURLParams), which is the implementation that we intentionally did *not* use when originally implementing this back in https://crbug.com/chromium/306873 because it didn't have the semantics that we wanted; however, those semantics have changed since (or we were mistaken originally), and now the LoadURLParams::extra_headers field does actually work *mostly* the same as our current implementation, but with fewer edge cases. It still has the behaviour that the extra headers persist across a redirect (so this would not in itself address this data leakage), but it has straightforward and easy-to-explain behaviour overall, and frees the headers once history is cleared or the WebView destroyed, so doesn't have the memory leak.

So, I think the current AwURLLoaderThrottle implementation is unsalvageable and should be entirely replaced no matter what. We have two real choices for what to do instead:

1) Just let the extra headers be passed into LoadURLParams as other use cases in Chromium do.
This will *not* directly do anything to address this security issue. We would need to update the docs to describe exactly how the extra headers are used and to caution against using them for any security purpose unless you are certain that the request won't be redirected to an untrusted target; developers of vulnerable apps would then have to act on this advice on their own.

2) Add a new parameter to LoadURLParams to allow passing a different set of extra headers that should only be used if the request hasn't been redirected across origins. Extend NavigationControllerImpl and related code to understand both sets of extra headers and handle them appropriately. Use it to implement WebView.loadUrl.
This would address this security issue in any reasonable case (technically a same-origin redirect *might* still be dangerous but this is rare, and removing the headers on a same-origin redirect would be a much larger compatibility risk). We would still update the docs to clarify exactly under what conditions the headers are used, but in the vast majority of cases, developers of vulnerable apps wouldn't have to do anything other than wait for users to get upgraded to the new version of WebView.

Both of these would simplify the behaviour and fix the memory leak, but obviously introducing a new feature into the navigation system in 2) is a significant change, and would come with some level of application compatibility risk.

To sum up the WebView team's current understanding of the security risk here:

- We're not currently aware of any libraries or common implementation patterns that involve sending sensitive auth tokens via loadUrl extra headers. This is not to say that no app is doing this, just that we have no evidence that it's particularly common. It's not possible to do this in general on the web (browsers don't allow any such thing), so any library/pattern here would have to be WebView-specific.

- XMLHttpRequest has the same behaviour: any custom headers set in the request will be preserved through redirects. The Fetch API also has the same behaviour, though Fetch can be configured to not follow redirects, allowing the app to make the decision about the headers for itself. This means that JS implementations of auth protocols already have to be aware of this risk and take steps to avoid it (either by not relying on sending auth tokens in headers to begin with, or by being cautious with redirects when they do).


Given all of the above, I have a weak preference toward option 1 (i.e. not changing the redirect behaviour and just clarifying what the behaviour actually is), but we'd appreciate a second opinion from the security team. mbarbella, would you be able to comment? (and also to answer the reporter's questions from https://crbug.com/chromium/1038002#c15?)


Longer term, we would support deprecating this variant of loadUrl entirely once we have implemented a more controlled (e.g. explicitly origin-scoped) way for apps to inject extra headers into requests; we've been considering implementing more flexible and safe request modification capabilities for some time now, and this issue is an additional motivator for that.

### sh...@gmail.com (2020-01-22)

Hey mbarbella/torne,

Any updates?

### rs...@chromium.org (2020-01-22)

I think we should do #2 (update the docs) at a minimum. If we wanted to mitigate, I think #3 is probably the safest fix. But could we perhaps do #1, and gate the breaking behavior on a new API level?

### mb...@google.com (2020-01-22)

Sorry I missed that this was assigned to me. Unassigning myself to make it clear that we still need an owner to fix this. The suggestions in c#20 seem reasonable to me.

I triaged this as low severity since the scope is fairly limited, at least when compared to something like an issue that could be triggered when visiting any web page. The guidelines can be found at https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md. I could see some argument for medium if any other security team members wish to change it. Regardless of the severity, the reward panel will take a look after the bug is fixed to decide if the issue will be rewarded.

### sh...@gmail.com (2020-01-23)

I tried to evaluate the severity using CVSS v3(An industrial standard algorithm), considering multiple use cases I always got the score more than 4.0(CVSS:3.0/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:L/E:P/RL:T/RC:C/CR:M/IR:M/AR:M, Score: 6.6 and Severity: Medium) and that is the reason I considered it to be a Medium severity issue. Moreover, based on the https://crbug.com/chromium/1038002#c18 made by Torne I believe some other cases discovered where header was sent which might affect the severity of the issue.

I would appreciate if you could provide me with the expected timelines regarding the closure of this issue as already mentioned I have plans of delivering a security talk/training around it. Also, considering Google Chrome is a CNA, could you please throw some light on the CVE allotment?

### to...@chromium.org (2020-01-23)

Thanks for the input Robert and Martin. Changing the behaviour is awkward as described in c#18 and we should probably reimplement this feature regardless of whether we change the redirect behaviour, due to the other problems I found with the way it's implemented right now :|

The other related problems have a much smaller potential security impact: they may cause headers to be sent in cases that would surprise the app developer, but only to the same URLs that the headers were previously sent to, so in the vast majority of cases this isn't disclosing any information to a party that doesn't already have it; it's only a risk in the case of, say, a transient webserver running on a random port on localhost.

Per the guidelines I agree that low severity is reasonable, primarily because this behaviour cannot be controlled by an attacker; whether sensitive headers are included and whether the page redirects to a 3P origin are entirely under the app developer's control, and most apps don't need to do this at all.

I'll investigate how difficult it would be to get LoadURLParams to support only including the headers for the initial request origin, because if that can be done in a way that the relevant owners are happy with, that's probably the best option.

### sh...@gmail.com (2020-02-08)

Hi Team,

I hope you guys are doing great!

Would appreciate if you could help me providing the information on the below-mentioned points:

1. What and how have we finalised to fix the issue?
2. What are the expected timelines regarding the closure of this issue as already mentioned I have plans of delivering a security talk/training around it.
3. Since Google Chrome is a CNA, could you please throw some light on the CVE allotment?


It would be really great if we could quickly work on the fix and roll it out asap so that I could deliver this in my upcoming talk on webview security.

~Shiv

### mb...@google.com (2020-02-10)

Thanks for checking in!

1. We still haven't decided on the best fix for this. There are compatibility considerations that make this difficult to fix. We should keep this bug up to date with any decisions we end up making.
2. As of today there isn't a clear timeline for when this will be fixed. Given the circumstances here I think it would be reasonable for you to go ahead with your talk regardless. Thanks for the heads up! Once this is fixed the reward panel will review the bug and I'll recommend that they consider it for a reward even if it's been made public (though I can't guarantee that it will be rewarded).
3. We assign CVEs to any externally reported security bugs that impact stable. Once this is fixed, it should be assigned a CVE.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e46cca3ee484bac0cdb5d4bdae69a18857f8efd

commit 6e46cca3ee484bac0cdb5d4bdae69a18857f8efd
Author: Torne (Richard Coles) <torne@google.com>
Date: Fri Mar 06 01:36:12 2020

webview: make extra header handling more sensible.

Change how extra headers provided through loadUrl(url, extra_headers)
are handled in WebView:

1) Remove any extra headers from the request if the request is
   redirected to a different origin, since they might be sensitive.

2) Don't attempt to add any extra headers for the redirect target URL
   when we encounter a redirect; this is likely to be surprising and
   unwanted.

3) Record metrics on when we add headers and what was done with them on
   redirect.

4) Add an additional test verifying that the extra headers are cleared
   if the app loads the same URL again via loadUrl(url).

Bug: 1038002
Change-Id: Ib39e2938f7b76d212cd20773aab56da138088b63
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1999229
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Reviewed-by: Tobias Sargeant <tobiasjs@chromium.org>
Commit-Queue: Richard Coles <torne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#747517}

[modify] https://crrev.com/6e46cca3ee484bac0cdb5d4bdae69a18857f8efd/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/6e46cca3ee484bac0cdb5d4bdae69a18857f8efd/android_webview/browser/network_service/aw_url_loader_throttle.h
[modify] https://crrev.com/6e46cca3ee484bac0cdb5d4bdae69a18857f8efd/android_webview/javatests/src/org/chromium/android_webview/test/LoadUrlTest.java
[modify] https://crrev.com/6e46cca3ee484bac0cdb5d4bdae69a18857f8efd/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/6e46cca3ee484bac0cdb5d4bdae69a18857f8efd/tools/metrics/histograms/histograms.xml


### sh...@gmail.com (2020-03-06)

This sounds really good. Thank you for the quick fix, I was not expecting it to be this quick. 
Can you guys please tell me about the next steps.

-Shiv

### to...@chromium.org (2020-03-06)

This may not be the final fix and we may have to revert it if there are significant compatibility issues with apps. I will *not* be merging this fix to beta/stable branches, so it will take some time to be released via the normal release path for M82 - I want to let it go through canary/dev and our manual QA as normal, to see if we see any sign that apps are negatively affected, and to collect some data via the metrics I added. I will follow up on this bug once the CL goes to beta and there's some data to look at (if we don't hit any issues before then).

If we're able to make this change without too much of a compatibility impact then we'll likely follow up with further refinements here - the code for adding the headers is still very weird and it's hard to clearly explain in which cases the headers are included vs not. We have an idea for a more sensible implementation but we need to see if removing the headers on cross-origin navigations causes issues before it's worth pursuing it further.

### sh...@gmail.com (2020-03-06)

Sure. Thanks for the information. Would it be possible to let me know about the tentative timelines that we are looking at? 


### to...@chromium.org (2020-03-06)

See https://chromiumdash.appspot.com/schedule for the estimated timeline for M82 - but we'll likely have to wait until some time *after* this reaches stable to conclude that this was an acceptable fix; it can take a long time for apps to notice that they've been broken by WebView updates :(

### to...@chromium.org (2020-04-02)

Unfortunately, due to the situation with COVID-19 the M82 release of Chrome/WebView was cancelled, so this change is still only available in the dev and canary channels. We've not had any reported issues yet but the populations using those versions is pretty small.

The current stats from dev/canary are that we see about 4% as many cross-origin redirects as we have requests with extra headers, and also about 4% same-origin redirects. That doesn't mean that 4% of extra header requests get sent cross-origin, though, as a single request might be redirected multiple times and thus counted more than once (and also potentially counted in both buckets). The volume of data is low so drawing any conclusions here is premature, but this looks like it's happening sufficiently often that there is a nontrivial compatibility risk. That doesn't mean it's actually incompatible - I imagine that a large number of these are the exact kind of accidental data leakage this bug is about -  but it would be a more encouraging sign if this situation was actually very rare in the first place.

Unless we hear about any breakages caused by this I'll check back on the metrics later in the M83 release cycle when this has reached more users.

### to...@chromium.org (2020-04-02)

Oh, one more metric point: it looks like about 2-3% of loadUrl calls to http/https URLs have extra headers specified, though this is a rough approximation by combining different stats as I didn't add a direct measurement of this (probably should have thought of it). So super rough estimate is that we're changing the behaviour of something like 0.1% of loadUrl calls.

### sh...@gmail.com (2020-04-05)

Thanks for the update. 

### sr...@google.com (2020-04-09)

We are one week past M83 branch point and in light of COVID-19 and extra scrutiny of M83 release, we are currently accepting only P0/P1 bugs in this release. Please ensure your bug priority is set properly and if it is not a P0/P1 then please move it to the next milestone. If this is a release blocker for M83, please adjust the priority to P0/P1 as applicable.

### to...@chromium.org (2020-04-10)

The change is in 83 already but we may need to followup in M84.

### aj...@google.com (2020-04-15)

Hey, I'm wrangling bugs, can this be marked Fixed or is there more to do besides merging?

### to...@chromium.org (2020-04-16)

I've left it open for now for several reasons:

- We may still have to revert this change if it turns out to cause significant app compatibility issues, and we're not likely to find that out until some time after 83 goes to stable (it often takes app developers quite a long time to report these problems to us). Now that the M83 timeline has been settled I'm updating the NextAction to reflect when I can look at the metrics.

- The implementation of header insertion is still very unintuitive and is still inserting headers in cases where developers probably don't expect it to even with this change, though the security impact of this should be greatly lessened now that we strip them on cross-origin navigations. We should follow up and make it more sensible once we're sure the current change is sufficiently ecosystem-compatible.


If you'd like I can split off a separate bug to follow up here, but it'd be slightly easier not to :)

### aj...@google.com (2020-04-17)

No that's great, thanks for the update!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dbc45f250ead6c886351fe189f7354c7548eff8f

commit dbc45f250ead6c886351fe189f7354c7548eff8f
Author: Ben Mason <benmason@chromium.org>
Date: Fri May 22 19:59:40 2020

Revert "webview: make extra header handling more sensible."

This reverts commit 6e46cca3ee484bac0cdb5d4bdae69a18857f8efd.

Reason for revert: Breaking auth flow b/156844354

Original change's description:
> webview: make extra header handling more sensible.
> 
> Change how extra headers provided through loadUrl(url, extra_headers)
> are handled in WebView:
> 
> 1) Remove any extra headers from the request if the request is
>    redirected to a different origin, since they might be sensitive.
> 
> 2) Don't attempt to add any extra headers for the redirect target URL
>    when we encounter a redirect; this is likely to be surprising and
>    unwanted.
> 
> 3) Record metrics on when we add headers and what was done with them on
>    redirect.
> 
> 4) Add an additional test verifying that the extra headers are cleared
>    if the app loads the same URL again via loadUrl(url).
> 
> Bug: 1038002
> Change-Id: Ib39e2938f7b76d212cd20773aab56da138088b63
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1999229
> Reviewed-by: Ilya Sherman <isherman@chromium.org>
> Reviewed-by: Tobias Sargeant <tobiasjs@chromium.org>
> Commit-Queue: Richard Coles <torne@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#747517}

TBR=isherman@chromium.org,torne@chromium.org,tobiasjs@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 1038002
Change-Id: I18791d4ef448d1ed9bcd4f0b02d4b8884018e8c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2213337
Reviewed-by: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/branch-heads/4151@{#12}
Cr-Branched-From: f00260ed8d970cace31eddcd333c20d20c77a887-refs/heads/master@{#770667}

[modify] https://crrev.com/dbc45f250ead6c886351fe189f7354c7548eff8f/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/dbc45f250ead6c886351fe189f7354c7548eff8f/android_webview/browser/network_service/aw_url_loader_throttle.h
[modify] https://crrev.com/dbc45f250ead6c886351fe189f7354c7548eff8f/android_webview/javatests/src/org/chromium/android_webview/test/LoadUrlTest.java
[modify] https://crrev.com/dbc45f250ead6c886351fe189f7354c7548eff8f/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/dbc45f250ead6c886351fe189f7354c7548eff8f/tools/metrics/histograms/histograms.xml


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/25e22803cd45bf2cfccaea8c716d3086618c43c7

commit 25e22803cd45bf2cfccaea8c716d3086618c43c7
Author: Ben Mason <benmason@chromium.org>
Date: Fri May 22 22:49:21 2020

Revert "webview: make extra header handling more sensible."

This reverts commit 6e46cca3ee484bac0cdb5d4bdae69a18857f8efd.

Reason for revert: Breaking auth flow b/156844354

Original change's description:
> webview: make extra header handling more sensible.
>
> Change how extra headers provided through loadUrl(url, extra_headers)
> are handled in WebView:
>
> 1) Remove any extra headers from the request if the request is
>    redirected to a different origin, since they might be sensitive.
>
> 2) Don't attempt to add any extra headers for the redirect target URL
>    when we encounter a redirect; this is likely to be surprising and
>    unwanted.
>
> 3) Record metrics on when we add headers and what was done with them on
>    redirect.
>
> 4) Add an additional test verifying that the extra headers are cleared
>    if the app loads the same URL again via loadUrl(url).
>
> Bug: 1038002
> Change-Id: Ib39e2938f7b76d212cd20773aab56da138088b63
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1999229
> Reviewed-by: Ilya Sherman <isherman@chromium.org>
> Reviewed-by: Tobias Sargeant <tobiasjs@chromium.org>
> Commit-Queue: Richard Coles <torne@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#747517}

TBR=isherman@chromium.org,torne@chromium.org,tobiasjs@chromium.org

Bug: 1038002
Change-Id: I18791d4ef448d1ed9bcd4f0b02d4b8884018e8c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2213119
Reviewed-by: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/branch-heads/4152@{#5}
Cr-Branched-From: 547e9589e8d4c7d966bc941354e059864a6aa132-refs/heads/master@{#771061}

[modify] https://crrev.com/25e22803cd45bf2cfccaea8c716d3086618c43c7/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/25e22803cd45bf2cfccaea8c716d3086618c43c7/android_webview/browser/network_service/aw_url_loader_throttle.h
[modify] https://crrev.com/25e22803cd45bf2cfccaea8c716d3086618c43c7/android_webview/javatests/src/org/chromium/android_webview/test/LoadUrlTest.java
[modify] https://crrev.com/25e22803cd45bf2cfccaea8c716d3086618c43c7/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/25e22803cd45bf2cfccaea8c716d3086618c43c7/tools/metrics/histograms/histograms.xml


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6170bc49652e605642469c7f59a284412b8590a9

commit 6170bc49652e605642469c7f59a284412b8590a9
Author: Ben Mason <benmason@chromium.org>
Date: Sat May 23 03:44:29 2020

Revert "webview: make extra header handling more sensible."

This reverts commit 6e46cca3ee484bac0cdb5d4bdae69a18857f8efd.

Reason for revert: Breaking auth flow b/156844354

Original change's description:
> webview: make extra header handling more sensible.
>
> Change how extra headers provided through loadUrl(url, extra_headers)
> are handled in WebView:
>
> 1) Remove any extra headers from the request if the request is
>    redirected to a different origin, since they might be sensitive.
>
> 2) Don't attempt to add any extra headers for the redirect target URL
>    when we encounter a redirect; this is likely to be surprising and
>    unwanted.
>
> 3) Record metrics on when we add headers and what was done with them on
>    redirect.
>
> 4) Add an additional test verifying that the extra headers are cleared
>    if the app loads the same URL again via loadUrl(url).
>
> Bug: 1038002
> Change-Id: Ib39e2938f7b76d212cd20773aab56da138088b63
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1999229
> Reviewed-by: Ilya Sherman <isherman@chromium.org>
> Reviewed-by: Tobias Sargeant <tobiasjs@chromium.org>
> Commit-Queue: Richard Coles <torne@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#747517}

TBR=isherman@chromium.org,torne@chromium.org,tobiasjs@chromium.org

Bug: 1038002
Change-Id: I18791d4ef448d1ed9bcd4f0b02d4b8884018e8c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2213972
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4153@{#3}
Cr-Branched-From: 2770346f01362a5f6d6f849a5a252b5d7e1c273d-refs/heads/master@{#771352}

[modify] https://crrev.com/6170bc49652e605642469c7f59a284412b8590a9/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/6170bc49652e605642469c7f59a284412b8590a9/android_webview/browser/network_service/aw_url_loader_throttle.h
[modify] https://crrev.com/6170bc49652e605642469c7f59a284412b8590a9/android_webview/javatests/src/org/chromium/android_webview/test/LoadUrlTest.java
[modify] https://crrev.com/6170bc49652e605642469c7f59a284412b8590a9/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/6170bc49652e605642469c7f59a284412b8590a9/tools/metrics/histograms/histograms.xml


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/442c0f850ae25c90d06930e5a5252983bb066a4f

commit 442c0f850ae25c90d06930e5a5252983bb066a4f
Author: Ben Mason <benmason@chromium.org>
Date: Sat May 23 13:00:14 2020

Revert "webview: make extra header handling more sensible."

This reverts commit 6e46cca3ee484bac0cdb5d4bdae69a18857f8efd.

Reason for revert: Breaking auth flow b/156844354

Original change's description:
> webview: make extra header handling more sensible.
>
> Change how extra headers provided through loadUrl(url, extra_headers)
> are handled in WebView:
>
> 1) Remove any extra headers from the request if the request is
>    redirected to a different origin, since they might be sensitive.
>
> 2) Don't attempt to add any extra headers for the redirect target URL
>    when we encounter a redirect; this is likely to be surprising and
>    unwanted.
>
> 3) Record metrics on when we add headers and what was done with them on
>    redirect.
>
> 4) Add an additional test verifying that the extra headers are cleared
>    if the app loads the same URL again via loadUrl(url).
>
> Bug: 1038002
> Change-Id: Ib39e2938f7b76d212cd20773aab56da138088b63
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1999229
> Reviewed-by: Ilya Sherman <isherman@chromium.org>
> Reviewed-by: Tobias Sargeant <tobiasjs@chromium.org>
> Commit-Queue: Richard Coles <torne@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#747517}

TBR=isherman@chromium.org,torne@chromium.org,tobiasjs@chromium.org

Bug: 1038002
Change-Id: I18791d4ef448d1ed9bcd4f0b02d4b8884018e8c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2213114
Commit-Queue: Ben Mason <benmason@chromium.org>
Reviewed-by: Tobias Sargeant <tobiasjs@chromium.org>
Reviewed-by: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/heads/master@{#771390}

[modify] https://crrev.com/442c0f850ae25c90d06930e5a5252983bb066a4f/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/442c0f850ae25c90d06930e5a5252983bb066a4f/android_webview/browser/network_service/aw_url_loader_throttle.h
[modify] https://crrev.com/442c0f850ae25c90d06930e5a5252983bb066a4f/android_webview/javatests/src/org/chromium/android_webview/test/LoadUrlTest.java


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3a2bcce9ad640e03f04732c8d50a48c21a2e0298

commit 3a2bcce9ad640e03f04732c8d50a48c21a2e0298
Author: Ben Mason <benmason@chromium.org>
Date: Sat May 23 13:44:18 2020

Revert "webview: make extra header handling more sensible."

This reverts commit 6e46cca3ee484bac0cdb5d4bdae69a18857f8efd.

Reason for revert: Breaking auth flow b/156844354

Original change's description:
> webview: make extra header handling more sensible.
>
> Change how extra headers provided through loadUrl(url, extra_headers)
> are handled in WebView:
>
> 1) Remove any extra headers from the request if the request is
>    redirected to a different origin, since they might be sensitive.
>
> 2) Don't attempt to add any extra headers for the redirect target URL
>    when we encounter a redirect; this is likely to be surprising and
>    unwanted.
>
> 3) Record metrics on when we add headers and what was done with them on
>    redirect.
>
> 4) Add an additional test verifying that the extra headers are cleared
>    if the app loads the same URL again via loadUrl(url).
>
> Bug: 1038002
> Change-Id: Ib39e2938f7b76d212cd20773aab56da138088b63
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1999229
> Reviewed-by: Ilya Sherman <isherman@chromium.org>
> Reviewed-by: Tobias Sargeant <tobiasjs@chromium.org>
> Commit-Queue: Richard Coles <torne@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#747517}

TBR=isherman@chromium.org,torne@chromium.org,tobiasjs@chromium.org

Bug: 1038002
Change-Id: I18791d4ef448d1ed9bcd4f0b02d4b8884018e8c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2213784
Reviewed-by: Ben Mason <benmason@chromium.org>
Commit-Queue: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#211}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/3a2bcce9ad640e03f04732c8d50a48c21a2e0298/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/3a2bcce9ad640e03f04732c8d50a48c21a2e0298/android_webview/browser/network_service/aw_url_loader_throttle.h
[modify] https://crrev.com/3a2bcce9ad640e03f04732c8d50a48c21a2e0298/android_webview/javatests/src/org/chromium/android_webview/test/LoadUrlTest.java


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/01a00adc19636c1e3f9f2afc4d7c2b1def1c7152

commit 01a00adc19636c1e3f9f2afc4d7c2b1def1c7152
Author: Ben Mason <benmason@chromium.org>
Date: Sat May 23 14:32:34 2020

Revert "webview: make extra header handling more sensible."

This reverts commit 6e46cca3ee484bac0cdb5d4bdae69a18857f8efd.

Reason for revert: Breaking auth flow b/156844354

Original change's description:
> webview: make extra header handling more sensible.
>
> Change how extra headers provided through loadUrl(url, extra_headers)
> are handled in WebView:
>
> 1) Remove any extra headers from the request if the request is
>    redirected to a different origin, since they might be sensitive.
>
> 2) Don't attempt to add any extra headers for the redirect target URL
>    when we encounter a redirect; this is likely to be surprising and
>    unwanted.
>
> 3) Record metrics on when we add headers and what was done with them on
>    redirect.
>
> 4) Add an additional test verifying that the extra headers are cleared
>    if the app loads the same URL again via loadUrl(url).
>
> Bug: 1038002
> Change-Id: Ib39e2938f7b76d212cd20773aab56da138088b63
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1999229
> Reviewed-by: Ilya Sherman <isherman@chromium.org>
> Reviewed-by: Tobias Sargeant <tobiasjs@chromium.org>
> Commit-Queue: Richard Coles <torne@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#747517}

TBR=isherman@chromium.org,torne@chromium.org,tobiasjs@chromium.org

Bug: 1038002
Change-Id: I18791d4ef448d1ed9bcd4f0b02d4b8884018e8c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2213117
Reviewed-by: Ben Mason <benmason@chromium.org>
Commit-Queue: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#596}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/01a00adc19636c1e3f9f2afc4d7c2b1def1c7152/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/01a00adc19636c1e3f9f2afc4d7c2b1def1c7152/android_webview/browser/network_service/aw_url_loader_throttle.h
[modify] https://crrev.com/01a00adc19636c1e3f9f2afc4d7c2b1def1c7152/android_webview/javatests/src/org/chromium/android_webview/test/LoadUrlTest.java


### [Deleted User] (2020-05-24)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-25)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-26)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-05-27)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-27)

Believed not fixed - reopening.

### to...@chromium.org (2020-05-28)

Yes, unfortunately the change here broke authentication flows in some apps and we had to revert it; we'll continue investigating the app use cases here and decide what to do.

### to...@chromium.org (2020-05-28)

+Andre who is working with us on developer outreach so he can see the discussion/details here.

### [Deleted User] (2020-05-28)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2020-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-01)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5

commit 25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5
Author: Torne (Richard Coles) <torne@google.com>
Date: Thu Jun 04 15:17:49 2020

Reland "webview: make extra header handling more sensible."

Reland the change to extra header handling with the actual behaviour
change behind a disabled-by-default base::Feature. UMA metrics are
collected even when the feature is disabled, simulating what would have
happened had the feature been enabled, so we can better gauge the
compatibility impact on applications.

Bug: 1038002
Change-Id: I3d722060cc4526a14adac076bbf4eec0a0992b70
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2229420
Commit-Queue: Richard Coles <torne@chromium.org>
Reviewed-by: Tim Volodine <timvolodine@chromium.org>
Reviewed-by: Nate Fischer <ntfschr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#775115}

[modify] https://crrev.com/25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5/android_webview/browser/network_service/aw_url_loader_throttle.h
[modify] https://crrev.com/25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5/android_webview/common/aw_features.cc
[modify] https://crrev.com/25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5/android_webview/common/aw_features.h
[modify] https://crrev.com/25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5/android_webview/java/src/org/chromium/android_webview/common/AwFeatures.java
[modify] https://crrev.com/25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5/android_webview/java/src/org/chromium/android_webview/common/ProductionSupportedFlagList.java
[modify] https://crrev.com/25560c2dd8e9d6097a0272d9c49f3fd4c28c0ad5/android_webview/javatests/src/org/chromium/android_webview/test/LoadUrlTest.java


### to...@chromium.org (2020-06-08)

I've relanded the behaviour change behind a flag (which can be enabled in the developer UI); we're communicating with the apps we identified as affected to find out more information and make a plan for how to roll this out.

One alternative implementation would be to limit it to the same eTLD+1 instead of the same origin, which would have avoided the issues we are aware of, but is not optimal from a security perspective; I'm also not aware of any other WebView APIs that are directly affected by any eTLD+1 logic so we'd have to explain that in documentation.

### [Deleted User] (2020-06-09)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2020-06-10)

This is not fixed, according to #57. Stop it, sheriffbot!

### sh...@gmail.com (2020-07-06)

Hi Team,

Hope things are well at your end!

Do we have any updates on the remediation timelines?

### to...@chromium.org (2020-07-15)

Hi; apologies for the lack of updates here. We've been communicating with developers of apps that are affected by this change (in potentially incompatible ways) and exploring the options, as well as waiting to collect more metrics from the field after my CL relanded it as an off-by-default flag. I'm currently working on the alternative fix discussed above, where we limit the headers to the same eTLD+1 instead of only the same origin; this avoids some of the compatibility issues we've seen while not weakening the security too badly. Once that's landed we'll run an experiment on one or both options and see what happens.

I'm really sorry this has taken so long - we do believe this is a security issue that needs fixing, but because there's a large number of apps that have the potential to rely on details of the current behaviour (in ways that are not security issues because all the servers are controlled by the developer, or because the data in the headers is not actually sensitive), we're having to be very cautious about the compatibility impact; we don't want to have to roll back the change a second time, hence taking the slower experimental approach.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/747a5e011637a2a586fc8eef7dc60057849435ff

commit 747a5e011637a2a586fc8eef7dc60057849435ff
Author: Torne (Richard Coles) <torne@google.com>
Date: Thu Jul 16 20:12:41 2020

webview: alternate option for extra headers.

Implement an alternative option for the handling of extra headers in
loadUrl, which only allows them to be sent to redirects to the same
domain (eTLD+1). This is less restrictive than the existing feature flag
requiring that they be the same origin (and if that flag is enabled,
this one has no effect).

Implement a new histogram that just records whether redirects are
same-origin, same-domain, or cross-domain, and obsolete the current one,
which doesn't make sense with the new option.

Bug: 1038002
Change-Id: I121de069d7a87fb4718ad9131ca427a5c017a7d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2264609
Auto-Submit: Richard Coles <torne@chromium.org>
Reviewed-by: Steven Holte <holte@chromium.org>
Reviewed-by: Nate Fischer <ntfschr@chromium.org>
Commit-Queue: Richard Coles <torne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#789174}

[modify] https://crrev.com/747a5e011637a2a586fc8eef7dc60057849435ff/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/747a5e011637a2a586fc8eef7dc60057849435ff/android_webview/common/aw_features.cc
[modify] https://crrev.com/747a5e011637a2a586fc8eef7dc60057849435ff/android_webview/common/aw_features.h
[modify] https://crrev.com/747a5e011637a2a586fc8eef7dc60057849435ff/android_webview/java/src/org/chromium/android_webview/common/AwFeatures.java
[modify] https://crrev.com/747a5e011637a2a586fc8eef7dc60057849435ff/android_webview/java/src/org/chromium/android_webview/common/ProductionSupportedFlagList.java
[modify] https://crrev.com/747a5e011637a2a586fc8eef7dc60057849435ff/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/747a5e011637a2a586fc8eef7dc60057849435ff/tools/metrics/histograms/histograms.xml


### to...@chromium.org (2020-07-17)

Will check that the new metric is working in a few days and then start on an experiment.

### to...@chromium.org (2020-07-23)

The histogram's working as expected; we have a small amount of data from dev/canary already, and currently it's about evenly split between same-origin, same-site, and cross-site. Once it reaches stable we'll have more reliable data from a more representative population and can investigate which apps are the sources.

I'm going to work on an experiment for this soon and see if we get any feedback from users/devs from enabling it in pre-stable channels.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7c7b2eff1c0ce46d161abc1cdd9c24f241743cfd

commit 7c7b2eff1c0ce46d161abc1cdd9c24f241743cfd
Author: Torne (Richard Coles) <torne@google.com>
Date: Thu Aug 13 16:46:08 2020

Add WebViewHeaderInjection field trial config.

Bug: 1038002
Change-Id: Ib53fe65d5a36af3146ad1f0c61cefbe9afcd8dac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2354151
Auto-Submit: Richard Coles <torne@chromium.org>
Commit-Queue: Richard Coles <torne@chromium.org>
Commit-Queue: Alexei Svitkine <asvitkine@chromium.org>
Reviewed-by: Alexei Svitkine <asvitkine@chromium.org>
Cr-Commit-Position: refs/heads/master@{#797718}

[modify] https://crrev.com/7c7b2eff1c0ce46d161abc1cdd9c24f241743cfd/testing/variations/fieldtrial_testing_config.json


### to...@chromium.org (2020-10-01)

No issues reported while this has been in beta and nothing unusual in the metrics. Will enable for 1% stable in advance of the 86 release to stable, and we can ramp up from there.

### to...@chromium.org (2020-10-15)

OK, this has been in 1% stable for a little while as M86 rolls out and there haven't been any issues reported, and the metrics haven't changed. The percentage of redirects that cross domains is about 14% and the list of apps that hit that case is, unfortunately, pretty much just a list of the most popular apps that use WebView, so I don't think we can do much more to identify compatibility issues without rolling it out.

I'm gonna enable it by default on ToT (which will go into M88) and then turn it on for all users via Finch for M86-87, and see if we have any issues reported.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/72c9a904da78180128cd27d4039147975551867d

commit 72c9a904da78180128cd27d4039147975551867d
Author: Torne (Richard Coles) <torne@google.com>
Date: Thu Oct 15 22:08:16 2020

Enable WebViewExtraHeadersSameDomainOnly by default.

Enable this experiment flag by default in preparation for enabling it on
stable via Finch.

Extend the expiry of the related metric so that it keeps collecting data
until after the default-enabling has reached stable.

Bug: 1038002
Change-Id: Ieae23184ab430565df775c1aad4112dc63ae1561
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2477155
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Reviewed-by: Nate Fischer <ntfschr@chromium.org>
Commit-Queue: Richard Coles <torne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#817692}

[modify] https://crrev.com/72c9a904da78180128cd27d4039147975551867d/android_webview/common/aw_features.cc
[modify] https://crrev.com/72c9a904da78180128cd27d4039147975551867d/testing/variations/fieldtrial_testing_config.json
[modify] https://crrev.com/72c9a904da78180128cd27d4039147975551867d/tools/metrics/histograms/histograms_xml/android/histograms.xml


### to...@chromium.org (2020-10-20)

Enabled by default for M88, and enabled for 10% of stable users on M66. We'll see if we get any issues reported in the next ~2 weeks and if not roll out further.

### to...@chromium.org (2020-10-29)

Going to 50% of stable.

### to...@chromium.org (2020-11-13)

Still no issues reported, I'm gonna roll out to 100%.

So, it will be enabled via Finch for 100% of users on 86.0.4206.0 and later, and enabled by default in the binary on 88.0.4295.0 and later.

We may still want to make further changes here - the behaviour is still weird, hard for developers to predict, and poorly documented, but I think that the same-site restriction now applied should be sufficient to mitigate the vast majority of potential app security issues caused by this behaviour.

Security folks: if I file a followup bug for the remaining issues, should we apply the same security labels/restrictions for now until this original bug is made public?

### rs...@chromium.org (2020-11-13)

> Security folks: if I file a followup bug for the remaining issues, should we apply the same security labels/restrictions for now until this original bug is made public?

If they reveal specific details of the vulnerability probably, but given that this is Sev-Low and a fix is in, that may be overkill.

### jd...@chromium.org (2020-11-18)

Gentle poke from a security sheriff -- shy of filing a follow-up bug for remaining issues, is there anything left on this bug? If not, let's close it out.

(Also, I agree with rsesek@ re: keeping the labels. Possibly overkill, but seems better to err on the side of caution.)

### to...@chromium.org (2020-11-19)

I'll file a followup bug shortly alongside cleaning up the experiment code, and for now I'll just keep the view restriction on the followup.

### to...@chromium.org (2020-11-19)

[Empty comment from Monorail migration]

### to...@chromium.org (2020-11-19)

OK, filed https://crbug.com/chromium/1150997 for the potential followups here. I'm including updating the Android API documentation as a followup because we should make sure we've settled on what the final implementation is going to be before revising the docs, to ensure we can actually explain it clearly this time.

Thanks for the report, Shiv, and thanks for your patience while we've worked on this; the compatibility issues made this much more time consuming than we would like.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/aa06acfa3f5d6c6ae910870a5c1ff34d1e3f3cba

commit aa06acfa3f5d6c6ae910870a5c1ff34d1e3f3cba
Author: Torne (Richard Coles) <torne@google.com>
Date: Fri Nov 20 00:01:35 2020

webview: clean up ExtraHeadersSameDomainOnly.

We've shipped this feature by default; remove the feature flag and false
branches from the code. Also remove the associated UMA metric; while we
may make more changes in this area, the data from the metric has not
proven valuable. The distribution of redirects is roughly split evenly,
across all apps, so doesn't really tell us anything about which cases
may be compatibility risks.

The stricter SameOriginOnly flag is retained for now while we consider
whether we want to run an experiment to make this behaviour stricter.

Bug: 1038002
Change-Id: I1c6cfccc92a360f5b2771608ef0c2678c2c6e6f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2550433
Reviewed-by: Nate Fischer <ntfschr@chromium.org>
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Auto-Submit: Richard Coles <torne@chromium.org>
Commit-Queue: Ilya Sherman <isherman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#829437}

[modify] https://crrev.com/aa06acfa3f5d6c6ae910870a5c1ff34d1e3f3cba/android_webview/browser/network_service/aw_url_loader_throttle.cc
[modify] https://crrev.com/aa06acfa3f5d6c6ae910870a5c1ff34d1e3f3cba/android_webview/common/aw_features.cc
[modify] https://crrev.com/aa06acfa3f5d6c6ae910870a5c1ff34d1e3f3cba/android_webview/common/aw_features.h
[modify] https://crrev.com/aa06acfa3f5d6c6ae910870a5c1ff34d1e3f3cba/android_webview/java/src/org/chromium/android_webview/common/ProductionSupportedFlagList.java
[modify] https://crrev.com/aa06acfa3f5d6c6ae910870a5c1ff34d1e3f3cba/tools/metrics/histograms/histograms_xml/android/histograms.xml


### sh...@gmail.com (2020-11-20)

Thanks for the timely keeping posted. The delay due to compatibility issue is totally understandable. Really appreciate the overall efforts done by the team for fixing the issue!


Can you please help me know about the next steps?

Thanks,
Shiv 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a22314e7144d8713f6d186563566060ffdd79914

commit a22314e7144d8713f6d186563566060ffdd79914
Author: Torne (Richard Coles) <torne@google.com>
Date: Tue Nov 24 17:20:53 2020

webview: mark correct header UMA as obsolete.

Previous CL marked Android.WebView.ExtraHeaders.Valid as obsolete, which
is incorrect; the UMA which was removed was ExtraHeadersRedirect.

Bug: 1038002
Change-Id: I4508958e02a3da78edd89077efd9418f415fa7c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2553860
Auto-Submit: Richard Coles <torne@chromium.org>
Reviewed-by: Robert Kaplow <rkaplow@chromium.org>
Commit-Queue: Robert Kaplow <rkaplow@chromium.org>
Cr-Commit-Position: refs/heads/master@{#830611}

[modify] https://crrev.com/a22314e7144d8713f6d186563566060ffdd79914/tools/metrics/histograms/histograms_xml/android/histograms.xml


### ad...@google.com (2020-12-02)

The commit from https://crbug.com/chromium/1038002#c69 looks like it will land in the initial M88 release.

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

Congratulations, the VRP panel has decided to award $2000 for this bug. Someone from our finance team will be in touch.

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### sh...@gmail.com (2020-12-09)

Hi Team,

Thank you for the reward and great work in fixing the issue. Can someone from security help me provide the following information:

1. Next steps for public disclosure
2. Issuance of CVE ID

### rs...@chromium.org (2020-12-09)

CVEs are usually assigned to bugs as part of the stable release process. And per https://www.google.com/about/appsecurity/chrome-rewards/, you are free to publicly disclose after the fix has rolled out to all our stable users (typically 1-2 weeks after the initial release of the stable version, because the update ramps up over time). M88 stable is currently scheduled to go out around Jan. 19.

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### sh...@gmail.com (2021-02-09)

Hey Team,

Thanks for the reward. I see that the CVE has been reserved for the security issue, Request you to kindly update if I can go-ahead with the public disclosure of the vulnerability. Also, I see no information has been updated against the CVE, appreciate if you could update the next steps around it as well.



### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### sh...@gmail.com (2021-02-15)

Hey Team,
Any updates on this?

### [Deleted User] (2021-02-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1038002?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1150997]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051073)*
