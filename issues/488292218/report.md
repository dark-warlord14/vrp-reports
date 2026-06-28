# Not preflighting message/ad-auction-trusted-signals-request breaks CSRF prevention features

| Field | Value |
|-------|-------|
| **Issue ID** | [488292218](https://issues.chromium.org/issues/488292218) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>InterestGroups |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 145.0.7632.111 |
| **Reporter** | gl...@apollographql.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open Network tab of dev tools
2. Go to <https://web.mit.edu/glasser/www/cors-no-preflight.html>
3. Observe that a cross-origin request was sent to the origin <https://graphql.api.apollographql.com/> with content-type message/ad-auction-trusted-signals-request with no CORS preflight. (The server does not return CORS headers that accept this origin, so the GET request has a CORS error, but it is still sent to the server)
4. Go to <https://web.mit.edu/glasser/www/cors-preflight.html>
5. Observe that this request (with a different content-type) was properly preflighted

# Problem Description

A common mechanism for cookie-protected web APIs which do not need to be triggered by browser features such as <FORM> to protect themselves from CSRF attacks is to reject all "simple" requests that may have come from a non-preflighted cross-origin browser context. See OWASP recommendation: <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#disallowing-simple-requests>

I am a maintainer of the popular open source GraphQL servers Apollo Server and Apollo Router (<https://www.apollographql.com/docs/graphos/routing/security/csrf>) both of which implement this protection by default.

This protection depends on browsers accurately implementing the CORS standard and only skipping preflight on requests with no content-type or the three standard non-preflighted content-types.

However, Chrome appears to now also skip preflighting on the message/ad-auction-trusted-signals-request content-type. This means that origins can send cross-origin requests with `content-type: message/ad-auction-trusted-signals-request` which are not preflighted; servers which assume standards-compliant browser behavior won't block this as a potential CSRF.

You may expect the servers to reject messages with a surprising content-type, but "parsing request body" is a different layer than "could request be CSRF". For example the Apollo GraphQL servers consider GET requests with non-simple content-types to be "definitely preflighted" even though it never parses the bodies of these GET requests, and so it will execute GraphQL queries sent with GET message/ad-auction-trusted-signals-request. (The browser will not be able to read the response and GETs should not be able to mutate state, but this can still be used for a timing-based "XS-Search" attack by determining whether the authenticated GraphQL read query was slow or fast.)

It looks like this feature requires a flag to enable: <https://chromium.googlesource.com/chromium/src/+/refs/tags/145.0.7632.111/services/network/public/cpp/cors/cors.cc#112>
Which I don't see in my chrome://flags but my browser is vulnerable.

I see this discussed by a Google employee at <https://github.com/WICG/turtledove/issues/1395>
This whole repo is archived as being part of a deprecated part of Chrome:
<https://github.com/WICG/turtledove>
<https://privacysandbox.google.com/private-advertising/protected-audience>

So it seems pretty bad for Chrome to be breaking common CSRF and XS-Search prevention techniques for a deprecated ads project.

This was reported to Apollo Graph Inc. by a user of Apollo Server.

# Summary

Not preflighting message/ad-auction-trusted-signals-request breaks CSRF prevention features

# Custom Questions

#### Type of crash:

n/a

#### Crash state:

n/a

#### Reporter credit:

David Glasser (Apollo Graph) and Amirmohammad Safari

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: Yes \

## Timeline

### gl...@apollographql.com (2026-02-27)

Full reporter credit should be: David Glasser (Apollo Graph) and Amirmohammad Safari

### li...@chromium.org (2026-02-27)

This might be WAI. @mm...@chromium.org can you take a look or reroute as necessary?

> It looks like this feature requires a flag to enable: <https://chromium.googlesource.com/chromium/src/+/refs/tags/145.0.7632.111/services/network/public/cpp/cors/cors.cc#112> Which I don't see in my chrome://flags but my browser is vulnerable.

That's because the `kProtectedAudienceCorsSafelistKVv2Signals` is already enabled by default.

### mm...@chromium.org (2026-02-27)

This is WAI. It is indeed treated as a CORS safelisted content-type. The requests, however, are uncredentialed. Moreover, the response cannot be accessed by a third party - it's only provided to scripts that are same-origin to the signals, in a restricted JS environment (if the seller script is 3P to the signals, there is a preflight).

There are on plans to make web-visible changes to the API before its removal, given the high overhead of doing so. We can't just remove the API yet for the exact same reason, unfortunately.

### gl...@apollographql.com (2026-02-27)

Hi, it's not accurate that requests are uncredentialed, though my initial replication does not show that. Here is a replication that shows it better:

1. Go to https://setcookie.net/ and create a cookie. Set SameSite to None, check "secure-only" and uncheck "HTTP-only".  This creates a cookie that can be sent cross-site via `fetch` with `credentials: 'include'`
2. Open dev console and go to https://web.mit.edu/glasser/www/cors-credentials.html and observe the request being sent the cookie without a preflight.

It is true that this only works with cookies set to that mode, but it is not unreasonable for servers to expect they can tell whether a request was preflighted by looking at the Content-Type headers. (It is true that servers can now use Sec-Fetch-Site and friends to protect modern browsers, but existing servers following recommendations do depend on the documented behavior that CORS agents have obeyed for many years.)

(Like other CSRF/XS-Search issues, this also lets an attacker send non-credentialed non-preflighted requests to private network locations accessible to the browser but not to the attacker directly, and similar timing attacks can be carried out on these servers if their CSRF prevention features have been bypassed by this ad feature.)

### es...@chromium.org (2026-02-27)

mmenke: it may be WAI but I think it's still a vulnerability. Non-preflighted Content-Types are supposed to be documented at https://fetch.spec.whatwg.org/#cors-protocol-exceptions and limited to "requests that can be triggered by web content but whose headers and bodies can be only minimally controlled by the web content".

### es...@chromium.org (2026-02-27)

> this also lets an attacker send non-credentialed non-preflighted requests to private network locations accessible to the browser but not to the attacker directly

This should be blocked by Local Network Access (https://developer.chrome.com/blog/local-network-access); if setting this header also permits an LNA bypass, that might be a separate bug.

### gl...@apollographql.com (2026-02-27)

> This should be blocked by Local Network Access (https://developer.chrome.com/blog/local-network-access); if setting this header also permits an LNA bypass, that might be a separate bug.

That's fair — last time I worked on our servers' CSRF features LNA was not yet rolled out (I think the previous Private Network Access was being tested), and I'm glad to see it exists by now; I did not try to reproduce this issue on local networks.

### mm...@chromium.org (2026-02-27)

estark: There is no control over the headers. Unfortunately, this request doesn't fit into the standard notion of CORS, since one context provides the URL, and another receives the response, and CORS is unable to distinguish the two concepts - as such, we use the latter as the CORS origin.

We did have PNA tests for this feature, which I believe have been converted to LNA tests now.

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/interest_group/auction_url_loader_factory_proxy.cc;l=215> unconditionally sets the credentials mode to omit, so a bit confused by the comment about these including cookies. We do have tests for that.

### mm...@chromium.org (2026-02-27)

I feel that it would in fact be more dangerous to use the origin of the page as the CORS origin, instead of the origin that has access to the response, and I do not have the authority to remove the API. The deprecation process is painfully slow, sadly, and I certainly don't have the authority or visibility into it to speed it up. Unassigning from myself, because I don't feel I can take any action here.

### gl...@apollographql.com (2026-02-27)

The issue here is that arbitrary JS code can forge requests that look like these, though.  The cors special case doesn't apply just to the requests you're talking about where "one context provides the URL, and another receives the response", but to any request that chooses to set this header.

Do I understand correctly that the expected use case for this feature is that the requests are issued by some sort of built-in-to-the-browser mechanism (not just JS)?  If Chrome prevented `fetch` calls (and other similar APIs) from setting this content-type, in the same way that fetch calls cannot set forbidden request headers (https://fetch.spec.whatwg.org/#forbidden-request-header) then that would fix the vulnerability, I think? I have no idea if this is an easy thing to implement or would cause other compatibility issues.

### mm...@chromium.org (2026-02-27)

Ok, so is the concern solely about the Content-Type being implicitly added to the allowlist of content-types, and let through CORS checks or about requests made by the API itself?

### gl...@apollographql.com (2026-02-27)

Right, I don't know much about this API and my reproduction doesn't involve it — it's the fact that the addition of this API changes the basic definition of how CORS is applied to JS-initiated requests from code like

```
fetch("https://setcookie.net/", {
method: 'GET',
credentials: 'include',
headers: {"Content-type": "message/ad-auction-trusted-signals-request"}
});
```

If it were possible for Chromium to only apply this special case to requests that come from this API then that would probably help (assuming an attacker can't manipulate the structure of the API-created request in a sketchy way).

### mm...@chromium.org (2026-02-27)

Ok, that's more feasible. Sorry for my confusion. I don't think we want to just block the content-type - for all that no one is likely using it on the entire Internet, I'd still rather not break anyone who is, so we probably want to apply the CORS exception only to certain requests, and out of caution, I don't think we want to bypass the rest of the CORS header checking for those requests.

[behamilton] What's the timeline for disabling PA completely? Life would be simpler if we can just wait until then, and call it a day. The number of auctions currently being run looks to be pretty much zero, at this point.

### gl...@apollographql.com (2026-02-27)

Thanks. Note that this creates a vulnerability in our servers (among others) so we do need to know at some point how to address that — eg we could explicitly block this content-type but that would reveal the existence of this issue publicly from our open-source code.

### gl...@apollographql.com (2026-03-04)

Hi, checking in about this — we do have our own external reporter hoping for feedback, and I don't know what approaches are appropriate for updating our open-source software without knowing what Chromium's feelings are re being blatant about "this is a new edge case that anybody using this approach to CSRF/XS-Search prevention needs to temporarily adopt".

### me...@google.com (2026-03-04)

behamilton: Assinging to you so that this security bug has an owner. Please see [comment #14](https://issues.chromium.org/issues/488292218#comment14). Thanks.

### mm...@chromium.org (2026-03-09)

Talked to behamilton, and it sounds like we do need to keep the feature around for ~6 months before we can remove it. We should be able to implement a workaround to block it from fetch requests in the meantime, but what's the actual attack here? Servers trying to deduce if a request was already preflighted, and bypassing checks on cross-origin requests if they deduce it was, or something else?

### gl...@apollographql.com (2026-03-09)

Basically a classic XS-Search (timing-based read-only CSRF equivalent). The GraphQL protocol is particularly sensitive to this because it allows complex user-provided read queries in GETs (which don't have a body and so having a weird Content-Type might not break the server implementation). Because of this, it's recommended practice for GraphQL servers to refuse to run any query that looks like it may have come from a web content that has not been preflighted. A spec-compliant browser will preflight any requests from web content that have an explicit content type other than "application/x-www-form-urlencoded", "multipart/form-data", or "text/plain". Chromium is not currently spec-compliant due to this issue, so attackers can evade this protection in Chromium.

An attack looks something like an untrusted origin issuing a GET request (with your ads content-type) against a target GraphQL server with credentials enabled which is written in such a way that it is noticeably slower depending on some state of the server that the attacker is trying to learn.  For example, the GraphQL query could be something like "search through all my data an item containing the string X; if you find an item, look up a very large number of different fields on that item afterwards". The performance of this query is noticeably different if user's data has an item containing X or not. Even though the untrusted origin will not be listed in the access-control-allow-origins header of the response and it will not be able to read the data directly, it can learn whether the data existed by measuring timing.

A recommended way to prevent this attack is to refuse to run operations that could be produced by untrusted cross-origin web content unless they are of a form that implies that they must have been pre-flighted. That lets the server rely on the browser's CORS origin comparison code instead of trying to directly process the Origin header in the server, and lets your server configuration separate your CORS configuration (probably provided directly by your web framework's standard CORS support rather than something GraphQL-specific) from the GraphQL security code.

This is reliable as long as browsers don't randomly decide that a particular structure of web-content-generated request does not need to be preflighted in explicit violation of standards. Unfortunately, Chrome has made that decision.

### es...@chromium.org (2026-03-09)

@mm...@chromium.org I see 3 possibilities for how to fix if the API can't be removed:
1.) [best option IMO] block this Content-Type from being sent on any request except one generated by the API -- I'm not familiar with the protected audiences implementation and how feasible this is
2.) block this Content-Type from being set by fetch(), XMLHttpRequest, and form submissions (less good because I don't know for sure that web content can't set Content-Type some other way)
3.) or, document the exception in https://fetch.spec.whatwg.org/#cors-protocol-exceptions so that servers know to block it server-side

### mm...@chromium.org (2026-03-09)

2) I'm not comfortable with, since it potentially breaks web content (admittedly, no one is likely using that, but still, would prefer to avoid it). 3) was the original plan, but now that we're going to remove the API, I don't think it makes sense.

I think that the simplest fix, albeit a hacky one, is to add a boolean field to ResourceRequest::TrustedParams to identify these requests, and allow the field to bypass CORS if that bool is set. Then we just revert out the change when we remove the API.

It's not lovely, and certainly not something I'd want to keep long term, but it's incredibly simple, and avoids issues with even compromised renderers, since TrustedParams can't be set by them.

### mm...@chromium.org (2026-03-09)

To clarify, we'd allow the extra accept field without a preflight if the bool is present, not bypass CORS entirely, since we do actually want CORS. Anyhow, I'll plan to go with that approach, barring any objections here or during code review.

### gl...@apollographql.com (2026-03-09)

Just to be clear, the bool you're talking about is something that the special code implementing the ads feature will be able to set, but web content (JS) won't?

### mm...@chromium.org (2026-03-09)

Correct, it will be a bool in an internal Chrome Mojo API. Web content doesn't have direct access to internal Chrome APIs. Moreover, this specific API is guarded so that even a compromised renderer can't set it.

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  main  

Author:  Matt Menke [mmenke@chromium.org](mailto:mmenke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7646934>

Replace enabled-by-default feature with a per-network request bool.

---


Expand for full commit details
```
     
    In particular, remove kProtectedAudienceCorsSafelistKVv2Signals, which 
    is enabled by default, and replace it with a bool in TrustedParams that 
    allows sending the message/ad-auction-trusted-signals-request 
    Content-Type without requiring a CORS preflight. 
     
    This adds the expected preflight to web-initiated requests with the 
    Content-Type, while not affecting the behavior of (deprecated and 
    slated for removal) Protected Audiences ad auction signals requests. 
     
    Unfortunately, we can't remove or break the Protected Audiences code 
    yet, but this gets us into a a better state in the meantime. When 
    we're finally able to remove the code in ~6 months, we can remove this 
    bool as well, and the logic associated with it. 
     
    Since it's in TrustedParams, even compromised renderers will be unable 
    to set the bool in the meantime. 
     
    Fixed: 488292218 
    Change-Id: I55de43411a17d3a67624f6d945e3074928ef782c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7646934 
    Reviewed-by: Maks Orlovich <morlovich@chromium.org> 
    Commit-Queue: mmenke <mmenke@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600128}

```

---

Files:

- M `content/browser/interest_group/auction_url_loader_factory_proxy.cc`
- M `content/browser/interest_group/trusted_signals_fetcher.cc`
- M `content/browser/interest_group/trusted_signals_fetcher_unittest.cc`
- M `services/network/cors/cors_url_loader.cc`
- M `services/network/cors/cors_url_loader_unittest.cc`
- M `services/network/cors/cors_util.cc`
- M `services/network/cors/cors_util.h`
- M `services/network/cors/cors_util_unittest.cc`
- M `services/network/cors/preflight_cache.cc`
- M `services/network/cors/preflight_cache.h`
- M `services/network/cors/preflight_cache_unittest.cc`
- M `services/network/cors/preflight_controller.cc`
- M `services/network/cors/preflight_result.cc`
- M `services/network/cors/preflight_result.h`
- M `services/network/public/cpp/cors/cors.cc`
- M `services/network/public/cpp/cors/cors.h`
- M `services/network/public/cpp/cors/cors_unittest.cc`
- M `services/network/public/cpp/features.cc`
- M `services/network/public/cpp/features.h`
- M `services/network/public/cpp/resource_request.cc`
- M `services/network/public/cpp/resource_request.h`
- M `services/network/public/cpp/url_request_mojom_traits.cc`
- M `services/network/public/cpp/url_request_mojom_traits.h`
- M `services/network/public/mojom/url_request.mojom`

---

Hash: [635cc5052af5b0c2d05f9bad46183ab97d2049a5](https://chromiumdash.appspot.com/commit/635cc5052af5b0c2d05f9bad46183ab97d2049a5)  

Date: Mon Mar 16 21:34:43 2026


---

### gl...@apollographql.com (2026-03-17)

I see this got merged — excellent, thanks! I'm not very familiar with the Chromium/Chrome release process — how do I tell when this patch has made it to the bulk of vulnerable Chrome users in the wild? Is there a rough timeline of when that is likely to be (assuming it doesn't get rolled back or anything)?

### mm...@chromium.org (2026-03-17)

This will be in Chrome 148, unless we opt to merge it to Chrome 147. Per https://chromiumdash.appspot.com/schedule, Chrome 148 is scheduled for release May 5th. If we do merge it to Chrome 147, it would be released on April 7th. I defer to the security team on whether this CL should be merged to 147.

### es...@chromium.org (2026-03-17)

We wouldn't normally merge to 147 for an S3 and it's a big CL, so I'd say this will roll out with M148.

Re #26: I don't think we publish stats on update uptake anywhere. If I were you, I would probably put an exception in your server-side check for 6-12 months or so to protect Chrome users that aren't updating. You can feel free to do that now because the patch is public already.

(Note to VRP panel: IMO disclosure of the bug by mitigating it in open-source server code shouldn't disqualify the reporter from a VRP payout in this case.)

### gl...@apollographql.com (2026-03-18)

Thank you. If we were to apply for a CVE against our own software for this issue, would that be an issue for Chrome/Chromium?  And if the patch specifically blocks message/ad-auction-trusted-signals-request, that would not be a problem according to my interpretation of what you said?  (I suspect a more future-proof fix would be for our servers to ban GET requests with content-types (or content-types other than application/json, which some GraphQL clients send for historical reasons) rather than to name message/ad-auction-trusted-signals-request, but I do want to make sure we're on the same page that we would be OK doing so if we wanted.)

### es...@chromium.org (2026-03-18)

@aj...@chromium.org or @el...@chromium.org, would either of you be able to comment on this:

> If we were to apply for a CVE against our own software for this issue, would that be an issue for Chrome/Chromium?

For context, the reporter's server-side code contains a CSRF defense that assumes browsers follow the spec wrt certain CORS rules; Chrome wasn't following the spec, thus the server's CSRF defense wasn't working as expected.

---

> if the patch specifically blocks message/ad-auction-trusted-signals-request, that would not be a problem according to my interpretation of what you said

Yes, this should be fine.

### gl...@apollographql.com (2026-03-20)

We are aiming for a security release of our open-source/source-available systems (Apollo Router and Apollo Server) on Monday or Tuesday of next week. At this point the plan is to be a little vague about exactly which browser is relevant and the precise content-type, though a motivated attacker could probably figure it out. Currently intending to have GitHub security advisories on our projects but no CVE, though we may change our mind. Thank you for your help.

### mm...@chromium.org (2026-03-23)

I'm not a security person, but I do think tying behavior so closely to the spec that if a new content-type is safelisted due to a spec change, it becomes a security issue on your side, that's a problem. You basically have to eternally monitor the spec for any additions there. I think it would make more sense to have an allowlist of trusted headers/types, rather than a distrusted list that may not have been preflighted.

It would be nice if the protocol itself provided information about what had been preflighted, for situations like these, but not sure how common this sort of behavior expectation is.

### gl...@apollographql.com (2026-03-23)

Yes, our fix is to switch from a "carefully read the spec and rely on perfect browser behavior" to an allow-list (which can be very small, because providing a content-type with a GET is a bizarre thing in the first place).

I think one of the sec-fetch-* headers might provide the information you're referring to, though I don't quite understand their implications myself (or know how prevelant they are across all modern browsers).

### gl...@apollographql.com (2026-03-24)

In case anyone is curious, our advisories:
https://github.com/apollographql/router/security/advisories/GHSA-hff2-gcpx-8f4p
https://github.com/apollographql/apollo-server/security/advisories/GHSA-9q82-xgwf-vj6h

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline with bisect. Exploitation Mitigation Bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488292218)*
