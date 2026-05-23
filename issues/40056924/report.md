# Security: "Origin" header incorrectly set for cross-site request via service worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40056924](https://issues.chromium.org/issues/40056924) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>ServiceWorker, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2021-08-18 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a cross-site request is made to a site that uses a service worker to fetch the request - the Origin header is incorrectly set to appear to come from the main site.

In the video you can see the problem in action.

Chrome states the Origin is "<http://cc.local>"  

Firefox states the Origin as "null"

I would consider this a serious security issue, as Chrome is simulating that the request "<http://cc.local>" which is not the actual Origin of the request.

**VERSION**  

Chrome Version: 92.0.4515.159 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**  

<https://github.com/garygreen/chrome-sw-origin-security-issue>

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: garygreen

## Attachments

- [chrome-sw-origin-prob.mp4](attachments/chrome-sw-origin-prob.mp4) (video/mp4, 391.1 KB)
- [repo.zip](attachments/repo.zip) (application/octet-stream, 1.8 KB)
- [firefox-sw-running-and-null-result.JPG](attachments/firefox-sw-running-and-null-result.JPG) (image/jpeg, 50.9 KB)
- [chrome-sw-origin-prob2.mp4](attachments/chrome-sw-origin-prob2.mp4) (video/mp4, 62.3 KB)
- [sw-echo.zip](attachments/sw-echo.zip) (application/octet-stream, 982 B)
- [echo.png](attachments/echo.png) (image/png, 5.8 KB)
- [sw-echo.png](attachments/sw-echo.png) (image/png, 5.8 KB)
- [sec.JPG](attachments/sec.JPG) (image/jpeg, 191.9 KB)

## Timeline

### [Deleted User] (2021-08-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2021-08-19)

Hmm, I can't seem to reproduce this. I'm on macOS. Instead of PHP I have a little Go server that appends the Origin header to whatever page it serves.

I followed your repro instructions (thanks! well-written!), but I consistently see "origin: https://example.test:10443" in the request headers, and that's what is printed on the page, too. That's the correct origin for me (self-signed cert with a trusted self-signed temporary root cert, and an entry in /etc/hosts). (https://github.com/FiloSottile/mkcert is very handy.)

mek, any chance you could take a look? Maybe it's Windows-specific, for some unlikely reason? Thanks!

[Monorail components: Blink>ServiceWorker]

### pa...@chromium.org (2021-08-19)

Oh, I should add: to qualify for a bug bounty, you have to keep the bug private until we've shipped the fix. Sadly, a public GitHub repo (as convenient as it is) violates that requirement.

See https://www.google.com/about/appsecurity/chrome-rewards/. I'm very sorry about that. However, the VRP Panel does decide on a case-by-case basis, so there may still be a chance for a reward, if we can reproduce the bug.

To be sure, next time, you can attach the proof-of-concept files right in the bug report.

### ho...@gmail.com (2021-08-19)

> I followed your repro instructions (thanks! well-written!), but I consistently see "origin: https://example.test:10443" in the request headers, and that's what is printed on the page, too

That's the problem - it shouldn't be printed on the page because it was a cross site request, so not the origin. Firefox displays "null" - either way, either Chrome or Firefox is wrong here. My gut says Chrome, because it shouldn't pretend the origin request came from the site. That sounds like a security exploit. 

We personally rely on the validity of the Origin header in our app to help prevent CSRF attacks.

> Oh, I should add: to qualify for a bug bounty, you have to keep the bug private until we've shipped the fix. Sadly, a public GitHub repo (as convenient as it is) violates that requirement.

Deeply sorry about that. I've made it private and attached the zip repo. The repo wasn't up long and I don't have many followers, so doubt anybody saw! My intention was never to spread this.

### me...@chromium.org (2021-08-19)

Is chrome's behavior actually incorrect? The service worker calls fetch(event.request). Per spec, the first thing fetch does is invoke the Request constructor with the passed in parameters (ending up calling https://fetch.spec.whatwg.org/#dom-request). If `input` is a Request object, that will not just reuse the request directly as is, rather in step 12 origin of the request is set to "client", and client of the request is set to the service worker global scope. Referrer policy and most other attributes are inherited from the original request though.

Then the actual fetch (in https://fetch.spec.whatwg.org/#concept-fetch) in step 9 replaces "client" as the request's origin with the actual origin of the service worker.

Finally the logic in https://fetch.spec.whatwg.org/#append-a-request-origin-header sees that the request method is not GET nor HEAD (it is POST), so it switches on referrer policy, which as long as that isn't set to no-referrer will append the requests origin as Origin header (well, it only does that if the requests "tainted origin flag" wasn't set, but I think that only gets set for redirects).

So if I'm understanding the spec correctly (I'm definitely not an expert here), the chrome behavior seems correct?

### ho...@gmail.com (2021-08-19)

Ok so I've checked that spec and this is my intrepretation. The key parts being:

https://fetch.spec.whatwg.org/#http-redirect-fetch

> 12. If locationURL’s origin is not same origin with request’s current URL’s origin and request’s origin is not same origin with request’s current URL’s origin, then set request’s tainted origin flag.

Then later on:

> Serializing a request origin, given a request request, is to run these steps:

1. If request’s tainted origin flag is set, then return "null".

2. Return request’s origin, serialized.

---

So to me it would seem like Chrome isn't probably determining that the origin is "tainted" during the cross site request here in the service worker, and therefore not returning `null`

Firefox seems to be handling this correctly imo.

### pa...@chromium.org (2021-08-19)

1: Oh dang, you're right — I forgot to serve cross-site.html from a local (i.e. a different site). The reason for this is that I am a deeply silly person. :) I apologize.

I do reproduce it in Chrome when making a cross-site request properly.

However, I'm still having trouble getting null in Firefox. In Firefox, when I load the main page, the Console says "Failed to register service worker: TypeError: ServiceWorker script at https://example.test:10443/sw.js for scope https://example.test:10443/ encountered an error during installation." Just "an error". :) The file and line given are "site.js:4:10", which is just the `console.log` line — nothing about sw.js or anything.

So, I don't know...

mek: Note the contents of sw.js in particular:

```
self.addEventListener('fetch', function(event) {
    console.log('Fetch event SW', event);

    // Commenting out the below line will cause Chrome to show Origin as "null" - same as Firefox.
    return event.respondWith(fetch(event.request));
});
```

Maybe that's a good clue. I don't know enough about SWs to know what difference that line might make.

2: I can't promise anything, but we understand, and the VRP Panel has a certain tendency to be gentle about well-meaning mishaps. :) Again, thanks for your help!

### pa...@chromium.org (2021-08-19)

mek! As always, feel free to CC anyone to the bug if they can help. There's no rule against that for security bugs. :) (Sometimes people worry, but it's all good.)

### ho...@gmail.com (2021-08-19)

> However, I'm still having trouble getting null in Firefox. In Firefox, when I load the main page, the Console says "Failed to register service worker: ...

Hmm that error is strange, not encountered that before in Firefox. Service Worker is definitely working for me (see screenshot) and I attached a video in my opening post showing Firefox's "null" result.

I did some Googling and it seems that if you click "Refresh Firefox" under "about:support" url it may help - though it looks like that may wipe your extensions and some settings. Maybe not an issue if you don't use Firefox much though, so worth a try?



### me...@chromium.org (2021-08-19)

The algorithm in "https://fetch.spec.whatwg.org/#http-redirect-fetch only comes into play when processing a redirect response, which isn't happening here.

The difference between not handling the fetch event at all and handling it by calling fetch(event.request) also seems correct. In the first case it is the original request that gets send to the network, with client and origin set to the page that posted the form, while in the second case client and origin are set to the service worker, resulting in the observed behavior.

### ho...@gmail.com (2021-08-19)

You’re correct, that section does indeed seem to apply specifically to redirects.

I've dug a bit further and checked the HTTP Origin spec. Some key points:

https://tools.ietf.org/id/draft-abarth-origin-03.html
> Whenever a user agent issues an HTTP request from a "privacy-sensitive" context, the user agent MUST send the value "null" in the Origin header.

It's unclear what is considered privacy-sensitive, but Mozilla's Wiki on the Origin header provides more clarity on what is considered "privacy-sensitive":

https://wiki.mozilla.org/Security/Origin

Whilst I understand that the service worker is the technical means in which the request is being made (essentially acting as proxy) - it's worth re-evaluating the key premise behind Origin header:

> The Origin header is added by the user agent to describe the security contexts that caused the user agent to initiate an HTTP request. HTTP servers can use the Origin header to mitigate against Cross-Site Request Forgery (CSRF) vulnerabilities.

So if the service worker is making out that a cross-site request ORIGINATED from the service worker that seems to defeat a key security characteristic the header.

### wa...@chromium.org (2021-08-19)

I wonder if the Origin header should be appended to the Request before invoking the service worker Handle Fetch algorithm.

### wa...@chromium.org (2021-08-19)

And just to make sure I understand, this is about a navigation POST request coming from a cross-origin initiator.  The destination site both has a service worker and wants its server to be able to detect if the request is coming from a cross-origin initiator.

I'll take this since I think Matt is busy at the moment.

If we want to support this use case (which seems reasonable to me), I think we would need to change the spec.  Unfortunately, since this is a security issue it makes public discussion on a spec issue difficult.  If no one objects, I start a private mail thread with the fetch spec editor who is external to chromium.

### ho...@gmail.com (2021-08-19)

Yes wanderview that is correct. It's a POST request initiated by cross-origin, then fetched in the service worker - it passes through the same request object.

It's about closing the security vulnerability by ensuring the service worker sets the Origin header as "null" due to the cross site request.

Firefox does this - it sets it as "null" which means Firefox doesn't have this security vulnerability. I wonder if the folks at Mozilla are able to assist?

### wa...@chromium.org (2021-08-19)

The fetch spec editor is annevk who works at mozilla.

### ho...@gmail.com (2021-08-19)

That's great! Thank you so much for looking into this. If you need any help let me know :-)

### wa...@chromium.org (2021-08-19)

I found another difference between chrome and firefox here.  Steps:

1. Visit https://fetch-event-echo.glitch.me to install its service worker.
2. Open an https://example.com tab.
3. Open the web console and set logs to persist across navigations.
4. Execute `window.location = 'https://fetch-event-echo.glitch.me'`
5. Note the FetchEvent logged to the console

In chrome the FetchEvent.request has an Origin header set to 'https://fetch-event-echo.glitch.me'.  In firefox FetchEvent.request does not have an Origin event.

So we are running into https://crbug.com/chromium/595993 as well.  It seems like an additional bug that its using the wrong origin for the header.

But none of that changes that the spec doesn't support the desired use case here.  So we should probably still talk to annevk.

### pa...@chromium.org (2021-08-19)

wnderview: Thanks for taking this! Regarding spec changes, it is totally OK to talk in public about spec changes/clarifications that you need to do for security reasons. Yes, there's a bug, but when it's design-y at least a much as implemention-y like this, we just have to talk about it publicly. I would bet that annevk would agree. So, don't feel like you have to be private about the design issues — it's more important to get the fix in, and Security Team never wants to slow that down.

Setting security labels: I think this is Medium, but I'm open to discussion either way.

### [Deleted User] (2021-08-19)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-08-20)

Jake, can you double check our take of the spec before I file a public spec issue?  What do you think of this use case?

### ho...@gmail.com (2021-08-20)

In regards to severity - this security vulnerability was brought to our attention because we rely on the Origin header to prevent Cross-Site Request Forgery (CSRF).

Our particular case here is a site can POST to our url

http://oursite.com/update-user-password
> BODY
>> password: some_new_password123

... and in our app the service worker implies the Origin came from the site, which we trust. So we allow password to be updated even though it was a cross-site POST request.

We can mitigate things like this by requiring they enter their existing password.. but generally it's a vulnerability that exists across all POST requests on our site. We can no longer trust the Origin header with Chrome.

Severity wise, for us it's quite high. But overall, medium seems reasonable as it requires sites to use both SW + fetch() + Trust the Origin header.


### wa...@chromium.org (2021-08-20)

Does using the referer header work for you here?  If your same-origin referrer-policy sense same-origin referers, then it seems you could look for that?

### ho...@gmail.com (2021-08-20)

Hmm I think we decided to go with the Origin header as we were concerned the referrer was something that could be removed with privacy extensions/generally not as reliable, though maybe things have changed there since we last looked.

We implemented Origin as it looked more bullet proof and specifically suited for CSRF mitigation.

Though I'll do some more research and testing on it - thank you for the suggestion and help here wanderview! :-)

### pa...@chromium.org (2021-08-20)

Additional defenses against CSRF you can try: putting a transaction token in each state-changing form; using Same-Site cookies.

### ho...@gmail.com (2021-08-23)

Thank you for the extra suggestions palmer. We originally used a token in each state changing form (we use Laravel) but we noticed lots of TokenMismatch exceptions, especially during long-lived sessions where people were coming back to their devices. So we switched to the Origin approach and trusted it. Things have been very reliable with it for years but since we implemented our PWA that's when we noticed this security vulnerability.

Looks like we may need to go back to the token method as you suggested for time being!

Is there any indication on how long this issue could take to fix? Sounds like it's a design/spec thing?

### wa...@chromium.org (2021-08-23)

I don't think this will be a quick fix.  We need to get consensus on spec, there are other existing bugs that interact, etc.

### wa...@chromium.org (2021-08-23)

To help the spec conversation I made a public glitch that can be used to test the situation:

https://service-worker-echo-origin-header.glitch.me/

### wa...@chromium.org (2021-08-23)

Interestingly, both firefox and safari show the cross-origin origin header.  Only chrome is showing the same-origin header.  This makes me think we're missing something in our reading of the spec.

### ho...@gmail.com (2021-08-23)

[Comment Deleted]

### wa...@chromium.org (2021-08-23)

I sent mail to start the spec discussion.

### ho...@gmail.com (2021-08-23)

In your example demo it's giving the same result for both buttons "Origin: https://service-worker-echo-origin-header-form.glitch.me"

It should be giving NULL for without service worker.

I've attached a new reproduceable zip file. Also see video example attached comparing Chrome and Firefox.

Vulnerability occurs on the "With SW" button in Chrome.

### ho...@gmail.com (2021-08-23)

I wonder if it's because I'm testing using local file:// and your testing on live domain?

### wa...@chromium.org (2021-08-23)

I believe "null" is provided instead of the origin based on the referrer-policy.

But I see the glitch demo showing different values for the two submission buttons on chrome.  One has "-form" at the end of the subdomain and the other does not.  See the attachments.  I think this is consistent with the problem you reported.

### ho...@gmail.com (2021-08-23)

Ah yes my mistake. I didn't spot the "-form". Your correct this is consistent with the problem I've reported.

### ho...@gmail.com (2021-08-23)

Is this a public spec discussion I'm able to see? Or is it still semi-public/private?

### ja...@chromium.org (2021-08-24)

Sorry I didn't get to this sooner. Here's the thoughts I sent to a smaller group:

---
The Firefox/Safari behaviour is definitely what we want in terms of security.

It feels like things go wrong with step 12 of the request constructor (https://fetch.spec.whatwg.org/#dom-request), where we should set origin to request's origin, rather than "client". The spec already does something similar for referrer.

Similar to referrer, the origin should be set back to "client" within step 13, since the request has been modified.

I'm assuming that the only time the service worker gets a request that has a cross-origin client is during a navigation.
---

I agree this is a pretty serious issue, as it 'disables' the modern way to avoid CSRF. Sites are only vulnerable if they opt-in by installing a service worker, but yeah, that shouldn't be such a security downgrade.

### wa...@chromium.org (2021-08-24)

I started working on a CL to see if I could fix this:

https://chromium-review.googlesource.com/c/chromium/src/+/3115917

Fixing this will run into network service and site isolation restrictions around ResourceRequest::request_initiator.  So far I'm seeing:

1) Network service asserts that only the browser process can initiate request with a "navigate" mode:

https://source.chromium.org/chromium/chromium/src/+/main:services/network/cors/cors_url_loader_factory.cc;l=380;drc=0ce9df69ba9e32bafc53c3d90db8a707c243da40

2) Network service also checks a site-isolation-like lock to make sure the request_initiator matches the expected site of the renderer process:

https://source.chromium.org/chromium/chromium/src/+/main:services/network/cors/cors_url_loader_factory.cc;l=403;drc=0ce9df69ba9e32bafc53c3d90db8a707c243da40

Both of these restrictions are violated by plumbing through the original origin of the requestor in this case.

I was thinking of relaxing these restrictions in the case that the request has a "navigate" mode and was originated from a service worker.  If the origin header is only exposed on non-GET requests, then maybe we could include that restriction too.  (I don't have this working in the CL yet, though, because something is overwriting the navigate mode and I haven't found it yet.)

David, what do you think?  Any advice here?  Thanks.

### da...@chromium.org (2021-08-24)

I don't think I'm familiar enough with this to say anything useful. :-( +mmenke perhaps?

### mm...@chromium.org (2021-08-24)

Since ServiceWorker's are potentially attacker controlled, I'd be much more comfortable proxying navigation requests from SW's through the browser process, and having it validate the information we get from them (Or better, fill it in itself).  Alternatively, we could vend a URLLoaderFactory specific for each navigation - the SW ultimately has to get navigation information from the browser process, anyways, so it could get a URLLoaderFactory with requisite fields pre-filled at the same time.

[+lukasza], who's the expert on the initiator lock.

I assume we run into issues with IsolationInfo here as well.

### lu...@chromium.org (2021-08-24)

RE: https://crbug.com/chromium/1241188#c37: wanderview@:

RE: "navigate" mode:

"navigate" mode is disallowed from renderers, because it bypasses 1) CORB and CORP protections for "no-cors" mode and 2) CORS protections for "cors" and "same-origin" modes.  If we allowed "navigate" mode then a renderer (compromised rendererer, or one using Spectre) could easily fetch https://cross-site.victim.com/secret.json in "navigate" mode (and read it if the renderer has been compromised, or if the attacker uses Spectre).

RE: request_initiator_origin_lock

Renderer process that hosts content (service workers, html documents, etc) from foo.com is only able to issue fetch requests with request_initiator set to foo.com.  This prevents such renderer process from being able to spoof a Sec-Fetch-Site request header, spoof Origin request header, or bypass CORB/CORP/etc.

For example, a renderer process locked to foo.com should *not* be able to initiate requests to bar.com with "Sec-Fetch-Site: same-origin" request header.  It seems that the proposal here violates this by granting service workers of foo.com an ability to initiate (arbitrary?) requests with request_initiator set to a cross-site navigation initiator bar.com.

[Monorail components: UI>Browser>Navigation]

### ho...@gmail.com (2021-08-25)

I took a look at the Sec-* headers in comparison to Chrome vs Firefox and it looks like it's showing it as same-origin request for the "Submit with service worker" example.

So it seems even the Sec- headers are vulnerable too. Or is this just a consequent of how Origin is handled?

### wa...@chromium.org (2021-08-25)

I could use some help coming up with a solution here.  I don't know the browser navigation path or network service code at all.

In terms of having the browser process broker the navigation request, would that mean doing something like:

1. Having a unique id associated with navigation requests.
2. If fetch sees that its processing a request with a navigate mode it sends the unique id to a mojo service in the browser instead.
3. The browser process then looks up the outstanding navigation request and starts fetching it.
4. The response and body data would then have to be plumbed back through.  (Hopefully devtools, extensions, etc work since browser already initiates navigation requests?)

### ho...@gmail.com (2021-08-25)

wanderview did you see my previous comment? Does that help at all in understanding how the navigation path could work?

I think it would be worth updating your demo to also output the Sec-* headers because they are vulnerable too.

### wa...@chromium.org (2021-08-25)

I saw your comment and I think if we plumbed the origin through the sec- headers would be fixed as well.

At this point I think we have concluded we need to fix something and we just need to figure out how to do that.  Other security constraints in chromium are going to make this tricky.

### lu...@chromium.org (2021-08-26)

wanderview@, can you PTAL at my reply below?

+yhirano@ for CORS expertise (mainly for the idea below to use mode=cors in navigation requests that are forwarded via service workers)

RE: request_initiator (and request_initiator_origin_lock)

It seems to me that to get "Origin: null", we would need to set network::ResourceRequest::request_initiator to an opaque origin (which serializes as "null" + which is compatible with any request_initiator_origin_lock.  This should address problem #2 from https://crbug.com/chromium/1241188#c37.

Note that currently VerifyRequestInitiatorLock doesn't verify the origin's "precursor", but we should still try to ensure that the opaque origin is derived from the service worker's origin (this will be compatible with request_initiator_origin_lock once it eventually takes the "precursor" origin into account).

I think this can be achieved by tweaking https://chromium-review.googlesource.com/c/chromium/src/+/3115917/3/third_party/blink/renderer/core/fetch/fetch_request_data.cc so that it doesn't just propagate `fetch_api_request->origin`, but first checks if the current execution context's origin is cross-origin from `fetch_api_request->origin` - pseudo-code:

    OLD proposal in https://crrev.com/c/3115917:
      if (fetch_api_request->origin)
        request->SetOrigin(fetch_api_request->origin);

    NEW proposal:
      if (fetch_api_request->origin) {
        blink::SecurityOrigin* execution_context_origin = ... somehow get this from `script_state`? ...
        if (!fetch_api_request->origin->IsSameOriginWith(execution_context_origin))
          request->SetOrigin(execution_context_origin->DeriveNewOpaqueOrigin());
      }


RE: mode=navigate VS mode=cors

I wonder if it would be okay if the service worker's request would go out with mode=cors.  This might not quite match the spec, but it could get us closer to spec compliance (wrt request_initiator / origin tainting) and would mostly address the current security bug (wrt Origin and Sec-Fetch-Site headers).

Pros:

*) mode=cors from renderer is compatible with the current Chrome security architecture (where navigations are always processed-by / driven-from the Browser process;  AFAIU without this restriction CORB and Site Isolation can't prevent cross-site data disclosure;  in theory a Browser process could proxy a navigate request on behalf of a service worker, but I don't _currently_ see how this can be cleanly and securely).

*) mode=cors would be used by default in `fetch(...)` API calls do not pass/forward an existing Request, but instead pass a URL/string as the first argument.

*) AFAICT the `fetch(...)` API doesn't allow using mode=navigate in the init object.  "navigate" is not mentioned in https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/fetch#parameters.  And "navigate" is not set/handled in blink::Request::CreateRequestWithRequestOrString - https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/request.cc;l=413;drc=2e3b822f787c5c328f9ae7a3140ff04165b11bfa

*) I _think_ that mode=cors and mode=navigate should result in the same wrt Origin and Sec-Fetch-Site request headers.

Cons:

*) The difference between mode=cors and mode=navigate would still be observable via Sec-Fetch-Mode.

### lu...@chromium.org (2021-08-26)

FWIW, I see that there are some extra exceptions in the code for how the request mode is set.  Let me try to loop in authors and reviewers of the changes that brought in those exceptions:

*) in blink::Request::CreateRequestWithRequestOrString
   (introduced in r562739: [Fetch API] Allow creating a request from a navigation request)

  // "If any of |init|'s members are present, then:"
  if (AreAnyMembersPresent(init)) {
    // "If |request|'s |mode| is "navigate", then set it to "same-origin".
    if (request->Mode() == network::mojom::RequestMode::kNavigate)
      request->SetMode(network::mojom::RequestMode::kSameOrigin);

*) in FetchManager::Loader::PerformHTTPFetch
   (introduced in r654060: Enforce no mojom::FetchRequestMode::kNavigate from renderer processes)

    case RequestMode::kNavigate:
      // NetworkService (i.e. CorsURLLoaderFactory::IsSane) rejects kNavigate
      // requests coming from renderers, so using kSameOrigin here.
      // TODO(lukasza): Tweak CorsURLLoaderFactory::IsSane to accept kNavigate
      // if request_initiator and the target are same-origin.
      request.SetMode(RequestMode::kSameOrigin);

FWIW, it seems that this spec violation has been recognized when discussing the code above - e.g. in the comment thread at https://chromium-review.googlesource.com/c/chromium/src/+/1574144/9#message-f3c87277f70f51c2c39c7e578e5eaa8dc649d42a there are comments saying:

*) In any case, as coded it indeed looks like Chrome doesn't allow the renderer to make "navigate" requests via fetch().

*) I guess it's a spec violation and we can now observe the difference via Sec-Fetch-Mode.

### wa...@chromium.org (2021-08-26)

Getting to a null origin might be enough for this bug, but it wouldn't get us to alignment with other browsers (which the spec is likely going to match soon).

If you test the other browsers with my demo:

https://service-worker-echo-origin-header.glitch.me/

You can see they provide an Origin header with the full cross-origin initiator populated.

Do you see significant obstacles to a brokering system like outlined in https://crbug.com/chromium/1241188#c42?  I think that would get us to full spec compliance.


### lu...@chromium.org (2021-08-26)

+mkwst@ for Sec-Fetch-Mode

RE: https://crbug.com/chromium/1241188#c47: wanderview@:

Can we move forward with using a null origin in this scenario?  This would fix this security bug + align Chrome behavior with other browsers wrt Origin and Sec-Fetch-Site expectations.  Therefore this seems desirable (even if it doesn't fix *all* problems associated with the scenario being discussed here).

We can track the remaining spec violations (only observable via Sec-Fetch-Mode?) in a separate bug.  If using a null origin works out, then I'd be happy to open a separate bug for this (I might ping mkwst@ for some hints/guidance on authoring a WPT test that covers Sec-Fetch-Mode via cross-origin navigation proxied by the target's service worker).

RE: Do you see significant obstacles to a brokering system like outlined in https://crbug.com/chromium/1241188#c42?

An important property of the current security architecture is that responses to navigation requests never go to/through renderers until the Browser process has determined which renderer can host the HTML document from the response.  It seems that this property would be violated by the 4th item from https://crbug.com/chromium/1241188#c42.

### lu...@chromium.org (2021-08-26)

+mkwst@ for real this time

### wa...@chromium.org (2021-08-26)

> Can we move forward with using a null origin in this scenario? 

I guess I'd rather fully bring us into spec compliance and alignment with other browsers than do a half measure if we can.

> An important property of the current security architecture is that responses to navigation requests never go to/through renderers until the Browser process has determined which renderer can host the HTML document from the response.  It seems that this property would be violated by the 4th item from https://crbug.com/chromium/1241188#c42.

How so?  The browser has already picked a process in this case (the process containing the service worker as its guaranteed to be same origin to the destination URL).  The idea is that the request has a UUID or similarly hard to guess id that a hostile renderer could not forge, so we can rely on only the renderers we give the id to being able to restart the request from the browser process.

An alternative approach would be to try to adapt our logic for handling the case where the service worker does not call respondWith() to this case.  Indeed this is very similar to what we do in that case.  There might be some differences in how redirects should be handled there, though.

### wa...@chromium.org (2021-08-26)

I'll investigate adapting the "didn't call respondWIth()" fallback logic to handle this case as well.  Maybe we don't need to add much at all.

### lu...@chromium.org (2021-08-26)

RE: https://crbug.com/chromium/1241188#c50: wanderview@:

RE: I guess I'd rather fully bring us into spec compliance and alignment with other browsers than do a half measure if we can.

I agree that full spec compliance is a desirable goal.  A small, necessary step toward this goal can be called "a half measure", but such a step still seems desirable to me (fixing a security bug seems desirable on its own;  small CLs seem desirable as they are usually easier to understand and less risky).

RE: How so [asking about myearlier claim that "this property would be violated by the 4th item from https://crbug.com/chromium/1241188#c42"]

Good point.  The `fetch(...)` API doesn't allow overriding the target URL of a request, and the `init` parameter only allows overriding a limited set of properties.  So, the UUID/proxying should work.

I would encourage trying this as a separate step (if possible).  This will help with more focused evaluation of the non-zero extra code complexity required by this step.  In particular the hierarchy of constituencies asks to treat spec purity as lower priority than complexity of implementations (https://www.w3.org/TR/html-design-principles/#priority-of-constituencies).

### wa...@chromium.org (2021-08-26)

> I would encourage trying this as a separate step (if possible).  This will help with more focused evaluation of the non-zero extra code complexity required by this step.  In particular the hierarchy of constituencies asks to treat spec purity as lower priority than complexity of implementations (https://www.w3.org/TR/html-design-principles/#priority-of-constituencies).

I would argue that overwriting mode with arbitrary other modes is introducing more complexity and technical debt.  We already have a mechanism that says "please restart and continue this navigation request".  I think fixing this bug requires a variant of that existing capability, so I think adapting it offers the least added complexity/confusion.

I'll write a design doc and we can have more concrete discussions about added complexity there.  Does that sound reasonable?

### lu...@chromium.org (2021-08-27)

RE: https://crbug.com/chromium/1241188#c53: wanderview@: design doc

That sounds totally reasonable.  Thank you for looking into fixing this bug.

Maybe to maximize the chance of fixing the security bug in M95 we can "timebox" this exploration and fallback to the narrower solution if needed to land the fix before the M95 branchpoint (which according to https://chromiumdash.appspot.com/schedule will happen on September the 9th).


RE: proxying

Let me try to help with exploring the design space here by sharing one random, brainstorming idea about how the proxying can be potentially implemented.  On the Browser process side, the NavigationURLLoaderImpl uses a mojo::Remote<URLLoaderImpl> - it could potentially be stored and wrapped in a new, proxying-kind-of factory (let's call it RequestProxyFactory).

The RequestProxyFactory would remember the original network::ResourceRequest and in its URLLoaderFactory::CreateLoaderAndStart implementation would prevent changing the ResourceRequest's properties, outside of a handful of changes allowed via the `fetch(...)` API's `init` object (which AFAIU makes it possible to override the `method`, `headers`, `body`, `mode`, `credentials` mode, `referrer`, etc.).

Reusing the `mojom::URLLoaderFactory` interface hopefully helps with "response and body data would then have to be plumbed back" from https://crbug.com/chromium/1241188#c42 - we could just reuse the existing mechanism.  And on the Browser side, the wrapped URLLoaderFactory is already correctly hooked into DevTools+Extensions/WebRequestApi.

I note that (AFAICT) the DOM Request object can be stashed by the service worker beyond the lifetime of the NavigationURLLoaderImpl.  This should be okay with RequestProxyFactory as long as it stays alive while it is bound (this can be achieved by deriving the implementation from network::SelfDeletingURLLoaderFactory).

2 potential issues that I see with the RequestProxyFactory approach (not necessarily unique to this approach):

1. Have to update RequestProxyFactory's knowledge of allowed ResourceRequest property changes whenever `fetch(...)` API's `init` allows extra properties.  I wonder if this needs to be achieved via comments/documentation VS if it would be possible to make RequestProxyFactory compilation fail if there are discrepancies (by having a shadow/duplicate/no-op struct next to RequestProxyFactory that static_asserts that is has to be the same size as the Init payload?).

2. I am not sure how to plumb RequestProxyFactory between the FetchRequestManager layer and wherever the URLLoaderFactory interface is used.  Maybe this requires adding a URLLoaderFactoryOverride property/field at the various intermediate layers?  (at the C++ class wrapping DOM Request + in other C++ representations of the Request used in Blink).

### wa...@chromium.org (2021-08-27)

In terms of timeframe I was not planning to try to rush something in before September 9.  This issue has existed in chrome for years (since service workers were introduced I think) and is only security severity medium.  On the other hand, I'm hopeful we will be able to have a solution in place that can be merged up to M95 before it goes stable.

Thanks for the design thoughts on a proxying solution!

### wa...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-09-02)

Koehei had another idea in an offline discussion:

1. When a navigation request is sent to the service worker we mint an unguessable token and include it with the request.
2. If the service worker does a fetch(evt.request) then we send the token back to the browser process/network service.
3. The network service would then validate the token if it see a navigation request from a renderer.  If the token is valid, then it would permit the request.

The token could be constructed by:

a. Generating a new cryptographic key at browser startup.
b. Use the key to hash key parts of the request together (initiator origin, navigation url, request id, etc.)
c. Use the hash as they token.

To validate the token the network service would just hash the new request and compare the result to the token.

This would require the browser process and network service to share the cryptographic key.  Perhaps this would require sending a message to the network service when it starts up.

lukasza@, what do you think of this idea?  It would be substantially less complex in terms of plumbing.

### da...@chromium.org (2021-09-02)

Pulling in cryptography for purely local communication always makes me a little suspicious. Not to say it's necessary wrong, just suspicious. It introduces questions like what bits should we hash in, what about replays, or what happens if the request is sent at a much much later time?

Perhaps there's a simpler solution by allowing same-origin requests a bit more control over the Origin header? Or maybe we just say null is the right answer here?

(NB: I may be misunderstanding some of the parts here. I read through the discussion but had to skim some bits since it's pretty long. It's quite possible all this is nonsense and you should ignore me. In particular I'm not quite following what the state of the spec is. Chrome and Firefox actually match for me, using the link in https://crbug.com/chromium/1241188#c47, strangely.)

As I understand it, we have some page under origin A making a cross-origin POST navigation to site B. Normally, this would turn into a network request to B's server with "Origin: A", so that B's server knows the request was constructed by A, not B. However, B has a service worker, which means navigations under B go to B/service-worker, not B/server. And the problem is that, when B/service-worker initiates a request, it is tagged "Origin: B". Yet we want to allow B/service-worker to tell B/server that A was involved. And now the conundrum is that we don't want to, in general, allow a service-worker or a compromised renderer process to spoof requests as coming from arbitrary other origins.

Is that right?

It seems to me there are a couple of options that don't require careful binding of request parameters:

Option 1: we say that going through B/service-worker is like a redirect and thus the correct answer is "Origin: null", not "Origin: A", because mixing two origins together gives null. Then we say that a fetch caller is always allowed to downgrade "Origin: yourself" to "Origin: null" because it is strictly lowering capabilities. But this means going through a service worker does not give the same answer as without the service worker, and I gather it not what the spec says? (Again, I'm not quite following what's going on with the spec.)

Option 2: we say that content is allowed to spoof the Origin header *only on same-origin requests*. The observation is B/service-worker already can lie to B/server by upgrading "Origin: A" to "Origin: B". It just makes a new request with the same parameters. So maybe we're willing to say that B/service-worker can claim it's acting on behalf of any other origin, specifically when talking to B/server (i.e. same-origin requests).

Option 2 is incompatible with B/server somehow granting "Origin: C" requests some capability not granted to "Origin: B" requests, but maybe that's fine? It's an odd case, and seems a cleaner model than saying "you can spoof this, even replaying it over time, but only if these various parameters match".

Or maybe I'm completely misunderstanding the issue and this comment is nonsense. :-)

### ho...@gmail.com (2021-09-02)

@davidben

>  Chrome and Firefox actually match for me, using the link in https://crbug.com/chromium/1241188#c47, strangely.)

I thought that too - but they are slightly different if you look at the end of the URL... 

Without SW: Origin: https://service-worker-echo-origin-header-form.glitch.me
With SW: Origin: https://service-worker-echo-origin-header.glitch.me

(notice "-form" difference)

----

Not sure I understand option 2 and the lieing spoofing thing? The issue is that a service worker can claim it's the initiator and override "Origin" during a cross site request.

All that needs to happen here is just to ensure during a cross-site request the service worker set’s the origin as “null”, or as you say "downgrade" the origin.. Though I have no idea how the renderer plays into this, sounds like there is existing security protocols in place which prevents this from being a straightforward fix 🤷‍♀️

@wanderview

For the cryptographic key idea that sounds quite complex - would that have any effect on performance on these requests? If so would be good to explore simpler solutions

### da...@chromium.org (2021-09-02)

> I thought that too - but they are slightly different if you look at the end of the URL... 

Right. I'm getting that Safari reports -form in both cases, while Chrome and Firefox reports -form w/o service worker and unsuffixed w/ service worker.

### ho...@gmail.com (2021-09-02)

[Comment Deleted]

### ho...@gmail.com (2021-09-02)

Ignore that comment, was testing wrong. Mozilla Firefox seems all secure

### ho...@gmail.com (2021-09-02)

[Comment Deleted]

### lu...@chromium.org (2021-09-02)

RE: https://crbug.com/chromium/1241188#c55: wanderview@: This issue has existed in chrome for years [...] and is only security severity medium

I am worried that we are pursuing a functionally-correct long-term solution, while the security aspect of this Pri1 bug remains unaddressed.  I am not sure if I agree with the current label of Security_Severity-Medium (brought up in https://crbug.com/chromium/1241188#c55, stamped in https://crbug.com/chromium/1241188#c18) - I think there are arguments for treating this as high severity, because an unexpected Origin header effectively does allow an attacker to 
execute code in the context of, or otherwise impersonate other origins.

RE: https://crbug.com/chromium/1241188#c58: davidben@: "Origin: null" + don't worry about proxying other aspects of the original request

This is what I was trying to encourage in https://crbug.com/chromium/1241188#c54 ("timebox") and https://crbug.com/chromium/1241188#c52.  OTOH, in the long-term we will also want to preserve (or at least consider preserving) other aspects of the original request - most importantly mode=navigate (which is visible on the wire in the Sec-Fetch-Mode http request header).

RE: https://crbug.com/chromium/1241188#c57: wanderview@: Introducing a new kind of a capability token

If the capability token doesn't remember the target URL, then this approach seems insecure - a compromised renderer that has received a capability token would be able to issue navigation requests to arbitrary URLs.

If the Browser or NetworkService process remembers the target URL associated with the capability token, then this requires extra complexity to clean-up the Browser/NetworkService-side data structures when the DOM Request object gets garbage collected in the Renderer process.  As I pointed out in https://crbug.com/chromium/1241188#c54, the DOM Request object can live for a long time - potentially much longer than the content::NavigationRequest object.


There is potentially one other option to consider for the long-term solution - see item B below.  So, I'd like to propose the following next steps:

Step 1: First land the security fix to use request_initiator=opaque-origin in this scenario (this seemed to be within reach according to my understanding of https://crbug.com/chromium/1241188#c47)

Step 2. Then start allowing mode=navigate in CorsURLLoaderFactory::IsValidRequest, but only if the request_initiator.GetTupleOrPrecursorTupleIfOpaque() matches the target URL.

Reasons for doing the 2nd step above as a separate CL:

*) There are quite a few of URLLoaderFactoryParams and ResourceRequest properties - I worry that this approach wouldn't use exactly the same properties as navigation requests initiated from the Browser process.

*) Smaller CLs are desirable in general (easier to review, more bisect friendly, safer to revert, less likely to cause merge conflicts, etc.)

*) It seems desirable to give ourselves more time to get more input from the Chrome Security Architecture and Network teams on whether matching request_initiator and target URL is sufficient.  (i.e. if we can ignore other properties of the Renderer process lock [e.g. coep/coop?] and of the ResourceRequest [NIK?])

### lu...@chromium.org (2021-09-03)

RE: https://crbug.com/chromium/1241188#c64: lukasza@ (myself :-)

RE: allowing mode=navigate if request_initiator or its precursor match the target URL

One caveat here is that request_initiator_origin_lock currently allows any opaque origin (i.e. doesn't verify the precursor origin of opaque origins).  This would need to be fixed before we could take step2 from https://crbug.com/chromium/1241188#c64.  I don't know if fixing this is easy or hard, because this extra validation of request_initiator_origin_lock hasn't been tried yet (OTOH, there are definitely some other known cases where origin precursors might be mismatched in some security or navigation checks - e.g. an Android WebView exception under ChildProcessSecurityPolicyImpl::CanCommitOriginAndUrl).


RE: severity

This was discussed on the security chat and there were good arguments both for keeping it as severity=medium and bumping it up to medium=high.    Omitting the Origin header in _most_ cases would definitely be severity=high (this allows for impersonation of another origin), but the extra prerequisites for this bug seem to be a mitigating factor that allows for downgrading to severity=medium.  This isn't clear-cut, because the bug doesn't require a specific user action or gesture, using the Origin header as an XSRF defense-in-depth seems reasonable [1], and service workers are an important feature of the modern web.  Given that this bug seems to be near the boundary of high and medium severity, it probably makes sense to keep the bug as severity=medium for now.

[1] https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html



### wa...@chromium.org (2021-09-03)

> If the capability token doesn't remember the target URL, then this approach seems insecure - a compromised renderer that has received a capability token would be able to issue navigation requests to arbitrary URLs.

What I proposed was a hash of the target URL plus additional information from the request.  So it would "remember" the target URL.

> If the Browser or NetworkService process remembers the target URL associated with the capability token, then this requires extra complexity to clean-up the Browser/NetworkService-side data structures when the DOM Request object gets garbage collected in the Renderer process.  As I pointed out in https://crbug.com/chromium/1241188#c54, the DOM Request object can live for a long time - potentially much longer than the content::NavigationRequest object.

I suggested a hashing mechanism for the token to avoid the necessity of this kind of clean up code.

But again, this was just an idea.  We don't have to go this way.

> Step 1: First land the security fix to use request_initiator=opaque-origin in this scenario (this seemed to be within reach according to my understanding of https://crbug.com/chromium/1241188#c47)

If we can set the request_initiator to achieve this, then I agree that we should do that now.  I'll take a look.  (My previous impression was that the short term fix required overwriting mode with CORS, etc, which I felt would just create more confusion.)

I'll still work on a design doc for a longer term solution.

### wa...@chromium.org (2021-09-03)

Yea, I believe firefox behavior just changed in regards to the origin header.  Testing in browserstack shows that firefox 89 does prints "-form" in the SW test case, but FF90+ now don't.  I'll let the mozilla folks know.

### wa...@chromium.org (2021-09-03)

Actually, I'm not sure sure setting request_initiator to a null origin will work.  If we continue to send "same-origin" for mode, then I think the network service will reject the request.  Is that correct?

I also don't think we can set mode to "cors" as was suggested above.  That would require the server to provide CORS headers for these kinds of requests to load which is very atypical for navigations.

We might be able to set the mode to "no-cors" and depend on fetch understanding its really a same-origin request to the SW to provide access to the Response, but that could run into CORB.

If we want something like this solution I think perhaps we would need to add a "force null Origin header" flag that fetch could set.  We would then leave the request_initiator as the SW's origin, set the flag, and the network service would check the flag when adding the Origin header.

### lu...@chromium.org (2021-09-03)

RE: https://crbug.com/chromium/1241188#c68: "same-origin" for mode [...] will reject the request.  Is that correct?

I think so.  We already do that (that = overwrite the mode with kSameOrigin) today in some cases pointed out in https://crbug.com/chromium/1241188#c46.

RE: https://crbug.com/chromium/1241188#c68: That would require the server to provide CORS headers for these kinds of requests to load which is very atypical for navigations.

I think this (requiring Access-Control-Allow-Origin response header) should already be the case for cross-origin POST navigations without a service worker.  Is it not the case?

RE: https://crbug.com/chromium/1241188#c68: force null Origin header flag

This is tricky, because request_initiator is consulted not only for CORS (where it influences the Origin header), but also for other features (e.g. Sec-Fetch-Site).  And if we change request_initiator then mode=same-origin will fail the request for opaque initiators.

Maybe the following would work:
1. Production code changes:
    1.1. Tweak CorsURLLoaderFactory::IsValidRequest to accept mode=navigate, but only if:
          1.1.1. request_initiator or its precursor origin matches request_initiator_origin_lock
                 (this requires a TODO to eventually move precursor checks into VerifyRequestInitiatorLock)
          1.1.2. request_initiator or its precursor is same-origin with the target URL of the request
2. Test coverage (verifying Origin, Sec-Fetch-Site, Sec-Fetch-Mode):
    2.1. This bug: foo.com -> service-worker.com POST (expecting "Sec-Fetch-Site: cross-origin" and "Origin: null")
    2.2. service->worker.com -> service-worker.com POST (expecting "Sec-Fetch-Site: same-origin", right?)

PS. "Origin or its precursor origin" = url::Origin::GetTupleOrPrecursorTupleIfOpaque (repackaged as url::Origin??)
PPS. Sorry for misunderstanding the token proposal yesterday :-/.


### wa...@chromium.org (2021-09-03)

> I think this (requiring Access-Control-Allow-Origin response header) should already be the case for cross-origin POST navigations without a service worker.  Is it not the case?

It is not needed for navigations, no.  This is a POST navigation per the spec and not a CORS request.  No CORS headers should be required.

> This is tricky, because request_initiator is consulted not only for CORS (where it influences the Origin header), but also for other features (e.g. Sec-Fetch-Site).  And if we change request_initiator then mode=same-origin will fail the request for opaque initiators.

What if we made this flag affect Sec-Fetch-Site as well?  Something like `expose_request_initiator_as_opaque = true`.

### lu...@chromium.org (2021-09-03)

RE: https://crbug.com/chromium/1241188#c70: What if we made `expose_request_initiator_as_opaque` flag affect Sec-Fetch-Site as well?

This seems fragile - it requires that whenever somebody reads network::ResourceRequest::request_initiator they might need to be careful and consider taking `expose_request_initiator_as_opaque` into account.


### wa...@chromium.org (2021-09-03)

I guess that leads us back to the longer term solutions, then.

### wa...@chromium.org (2021-09-03)

Looking at this idea from https://crbug.com/chromium/1241188#c69:

> Maybe the following would work:
> 1. Production code changes:
>     1.1. Tweak CorsURLLoaderFactory::IsValidRequest to accept mode=navigate, but only if:
>          1.1.1. request_initiator or its precursor origin matches request_initiator_origin_lock
>                (this requires a TODO to eventually move precursor checks into VerifyRequestInitiatorLock)
>          1.1.2. request_initiator or its precursor is same-origin with the target URL of the request

To make sure I understand, you are suggesting that we:

a. Have the renderer keep the mode as navigate instead of overwriting to same-origin.
b. If the request_initiator is cross-origin, then we set it to `request_initiator.DeriveNewOpaqueOrigin()`.  This captures the precursor origin.
c. We then make the network service changes you mention above.

Yes, that does seem doable.  Let me try that in a CL to see if anything blows up.  Thanks!

### wa...@chromium.org (2021-09-03)

Also, I am floating the idea of forcing to opaque origin in the spec discussion as well.

### wa...@chromium.org (2021-09-03)

lukasza corrected something in chat.  https://crbug.com/chromium/1241188#c73 should read:

b. If the request_initiator is cross-origin to context_origin, then we set it to `context_origin.DeriveNewOpaqueOrigin()`.  This captures the precursor origin of the context.

We need to derive the opaque from the context origin and not from the request_initiator.

### wa...@chromium.org (2021-09-03)

Here's a twist.  It turns out we set the Origin header for POST navigation requests in the renderer anyway.  So in theory I can just patch that up in FetchManager.  (This seems pretty bad if we just let renderers make this stuff up.)

That feels terribly unsatisfying, though, as the request_initiator is still using same-origin and will trigger other headers to perhaps be wrong.  So I'm still going to try forcing the request_initiator to an opaque origin.

### wa...@chromium.org (2021-09-03)

Note, setting the request_initiator to an opaque origin does appear to be working so far.  So I don't think do this extra work will take much extra work.

### wa...@chromium.org (2021-09-03)

WIP CL:

https://chromium-review.googlesource.com/c/chromium/src/+/3115917

### ho...@gmail.com (2021-09-07)

I've found another security vulnerability - it may share some similarities with this issue as it's to do with cross-site requests and vulnerability in a service worker. However, it works based on an entirely different mechanism.

Someone on your team has already closed the issue claiming it's a "duplicate" however I am very dubious, as service workers didn’t even exist when the "duplicate" issue was created.

Are any of you in a position to check if this was a mistake? I would be most grateful if you can provide a second opinion:

https://bugs.chromium.org/p/chromium/issues/detail?id=1246961

### wa...@chromium.org (2021-09-07)

I would need someone to cc me to that bug.

### da...@google.com (2021-09-07)

It seems to have been triaged correctly to me.

> as service workers didn’t even exist when the "duplicate" issue was created.

Hrm? The issue it was merged into also involves service workers and long post-dates them.

### ko...@chromium.org (2021-09-08)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-09-10)

Ok, the WIP CL is now fully working:

https://bugs.chromium.org/p/chromium/issues/detail?id=1241188

I will update comments, add tests, and send for review on Monday.

I also updated:

https://service-worker-echo-origin-header.glitch.me/

To echo a few more headers.  This shows that the WIP sends consistent values for origin, referer, and sec-fetch-site.  It also shows that we no longer overwrite sec-fetch-mode.

We still haven't decided anything at the spec level, though.  We will likely have a session at TPAC about service worker CSRF issues to discuss.

### wa...@chromium.org (2021-09-13)

Note, my initial testing of firefox was flawed.  On some versions of FF I started in the middle of my demo and missed getting the SW installed.  That is what produced the "regression" in the results.  Retesting correctly shows firefox has been sending the SW's origin in the header consistently.

### wa...@chromium.org (2021-09-13)

Status update:

I am still working on the test.  I'm running into some test harness issues that I need to figure out.

Also, I am aiming now to preserve the original cross-origin referer and origin headers.  Since these are set in the renderer we can set them as expected by the spec even if the request_initiator is an opaque origin.  We can bite off the longer term solution if/when folks want to invest in moving the navigation origin header code to network service.

### wa...@chromium.org (2021-09-14)

So now that its clear chrome and firefox have the same legacy behavior and match what has been in the spec, the fetch spec editor is asking us to hold off on making changes to chromium until we can determine the desired spec change.

How does the security team feel about that?

CC'ing Anne as the fetch spec editor.

### wa...@chromium.org (2021-09-14)

[Empty comment from Monorail migration]

### lu...@chromium.org (2021-09-14)

RE: aiming now to preserve the original cross-origin referer and origin headers

AFAIU there is no clear requirement for that + that diverges from the current behavior of Firefox.  When 


RE: Since these are set in the renderer we can set them as expected by the spec even if the request_initiator is an opaque origin.

I want to note a TODO that you've pointed out exists in services/network/cors/cors_url_loader.cc:
  
  // We exclude navigation requests to keep the existing behavior.
  // TODO(yhirano): Reconsider this.

I think that our high-level principles would require that the Origin header (and other security-sensitive headers like Sec-Fetch-Site, etc) should *not* be controlled by a renderere process.  It may seem okay in this case, because *initially* the request initiator (or its precursor) is the same origin as the target URL of the request, but I wonder what happens during 307 redirects.  See also a longer comment in https://chromium-review.googlesource.com/c/chromium/src/+/3115917/10#message-9b6b60b0916ccc4eafdb24156db8fa5501748895


RE: How does the security team feel about that?

Not sure if I can speak for the whole security team, but 1) we should verify what happens during 307 redirects and 2) even if 307 redirects are okay, using "Origin: null" would still seem like a safer starting point ("safer" meaning: A) more restrictive = more secure + B) safer to relax in the future without backcompatibility concerns).

### wa...@chromium.org (2021-09-14)

> AFAIU there is no clear requirement for that + that diverges from the current behavior of Firefox.

If we are going by firefox behavior then this bug is a WONTFIX.  What I am proposing matches safari behavior.

Also, the discussion from the spec group so far is fairly against setting an opaque origin header.

> I think that our high-level principles would require that the Origin header (and other security-sensitive headers like Sec-Fetch-Site, etc) should *not* be controlled by a renderere process.

Sure, but throughout this bug you have been consistently pushing me to do something short term to fix the security problem quickly.  Changing how we set origin headers for all non-get navigations seems like a separate bug, does not seem like a quick fix, and is not something I feel prepared to take on.  I think the network or loading team would need to drive the work for that.

When that work happens, though, we can also take the time to design the correct long term fix for service worker forwarded navigation requests without breaking service worker behavior.  I was prepared to do this longer term SW solution here, but you convinced me that we should get a shorter term solution done instead.

> Not sure if I can speak for the whole security team, but 1) we should verify what happens during 307 redirects and 2) even if 307 redirects are okay, using "Origin: null" would still seem like a safer starting point ("safer" meaning: A) more restrictive = more secure + B) safer to relax in the future without backcompatibility concerns).

I'm not sure I understand.  My question for the security group was about holding off on doing anything here until the spec discussion resolved.  It doesn't seem like you addressed that at all?

> I wonder what happens during 307 redirects.  See also a longer comment

Service worker navigation requests do not follow redirects.  They use the manual redirect mode.  So I think it will do the right thing, but we can test it.

Also, can we please keep security sensitive discussions in the private bug and out of the public CL?

### wa...@chromium.org (2021-09-14)

FWIW, I updated https://service-worker-echo-origin-header-form.glitch.me/ to have some redirect test paths.  The redirect flow is:

1. "-form" origin has a button with action pointing to "-redirect" origin.
2. "-redirect" origin redirects to main target origin (no suffix on the origin)

Without a service worker the 3 browser behaviors for this kind of redirect are:

  chrome: "origin: null"
  firefox: "origin: https://service-worker-echo-origin-header-form.glitch.me" (form origin)
  safari: "origin: null"

With a service worker the 3 browser behaviors are currently:

  chrome: "origin: https://service-worker-echo-origin-header.glitch.me" (sw origin as described by this bug)
  firefox: "origin: https://service-worker-echo-origin-header.glitch.me" (sw origin)
  safari: "origin: https://service-worker-echo-origin-header-form.glitch.me" (form origin)

I realized I can actually remove any changing of origin headers in my CL.  With that we get:

  modified chrome: "origin: null"

Matching the no service worker case.

In regards to a compromised renderer, though, I think you are correct that allowing a renderer to send a navigation will allow it to spoof any origin header it likes.  This probably applies to the referer as well.

This suggests two solutions:

1. The longer term solution I proposed earlier of proxying the navigation request back through the FetchEvent mojo connection so it can be initiated through browser process.
2. Change all non-get navigations to set origin and referer in the network service and then also do the proposed change currently in the WIP CL.

I'm inclined to wait for the spec discussion to resolve and then, if we need to make a change, implement (1).  It gives us the best match to the way the spec is architected and doesn't force any artificial restrictions.

I'm disinclined to pursue (2) because changing how all non-get navigations work seems like a big task and I don't feel prepared to take that on.  In addition, it would leave us with technical debt in terms of this weird artificial opaque origin.

### ho...@gmail.com (2021-09-14)

@wanderview - did Firefox update the behaviour? Because I'm sure when I was testing this initially Firefox was returning null for cross site requests.

Makes me thing guys over at Mozilla decided to update Firefox to less secure behaviour in order to follow spec? 8_d

Could be mistaken though

### wa...@chromium.org (2021-09-14)

No, Firefox did not change anything recently.  At least in my case I ran some tests accidentally without the SW installed which led to previously incorrect results.  It's also possible that you are testing in an environment with a different referrer policy set.

### ho...@gmail.com (2021-09-14)

I was testing using file:// as cross-site initiator. I've confirmed in Mozilla service worker is registered and running and even now it's returning `null` as origin when submitted thru sw

So looks like Mozilla generally sees file:// as dodgy and cross site, but behaves differently on live site with https. Not sure why that would be though, if this is a spec thing

### wa...@chromium.org (2021-09-14)

I guess an option is:

3. Modify the CL to keep the origin (and referer) in sync with the request_initiator and then validate the headers in the network service for navigations coming from a renderer.

I don't love this option as I think the opaque origin header is a bit weird and unexpected for developers.  Also, if we keep the referer in sync as being opaque then we deprive developers of information they could be usefully collecting for their product today.  That's a bit breaking.

But I think we should see where the spec discussion goes.  My impression from Anne is that we may end up saying the current firefox and chrome behavior is intended and we shouldn't change anything at all.

### ho...@gmail.com (2021-09-14)

> My impression from Anne is that we may end up saying the current firefox and chrome behavior is intended and we shouldn't change anything at all.

Are you suggesting this may not be fixed in the spec... and origin + sec headers + same site cookies will stay vulnerable when a site has a service worker? That seems bonkers.

I would push for a spec change if this is seen as "intended behaviour"...

### wa...@chromium.org (2021-09-14)

To help get the spec discussion to conclusion I scheduled a TPAC session:

https://github.com/w3c/ServiceWorker/issues/1604

### ho...@gmail.com (2021-09-14)

Thanks for doing that, sounds good!  It's the "and we shouldn't change anything at all" comment that's got me concerned.

This change isn't just for CSRF but I suspect is having an impact on same-site cookies vulnerability, and probably others.

I think if nothing is changed it would be sensible to discuss what wider trust issues that could cause in the community for security of PWAs. If nothing changes, then this vulnerability is open for public consumption. Both seem unpalatable.

### wa...@chromium.org (2021-09-15)

I'm continuing to work on the short term fix in my CL so we can land it ASAP if we get a resolution.

I have my CL updated to send opaque origin/referer headers and to check them in network service.  I also have a wpt_internal test.

I still need to add a unit test that shows the CorsURLLoaderFactory rejects invalid renderer requests.  I tried doing this in a normal unit test, but it crashes the entire test.  I think I might need to figure out how to do this in a browser test.

### lu...@chromium.org (2021-09-15)

RE: https://crbug.com/chromium/1241188#c89:  wanderview@: Service worker navigation requests do not follow redirects.  They use the manual redirect mode.  So I think it will do the right thing.

I see.  That would indeed help.  We should make sure there is an explicit verification of the redirects mode in CorsURLLoaderFactory::IsValidRequest (i.e. only allow mode=navigate from renderer if 1) it is same-origin/precursor wrt the target URL *and* 2) it uses manual redirect mode).

RE: https://crbug.com/chromium/1241188#c90: wanderview@: I think you are correct that allowing a renderer to send a navigation will allow it to spoof any origin header it likes.

If we enforce manual redirect mode, then the renderer would only be able to control the Origin header in same-origin requests, right?  So it seems okay maybe?  (Unless the renderer-controlled Origin header can be used cross-origin in other requests, where redirects are not required.)

RE: https://crbug.com/chromium/1241188#c89:  wanderview@: Changing how we set origin headers for all non-get navigations seems like a separate bug, does not seem like a quick fix, and is not something I feel prepared to take on.

That's fair.  It seems okay to proceed with renderer-controlled Origin header if we are confident that this doesn't allow spoofing of the header in cross-origin requests (otherwise it would be a regression on https://chromium.googlesource.com/chromium/src/+/main/docs/security/compromised-renderers.md#http-request-headers).  It does seem more risky then enforcing the Origin header in OOR-CORS/NetworkService, but there are no known security issues + it would fix a known security bug (this bug).


### lu...@chromium.org (2021-09-15)

+adetaylor@ help with the urgency/scheduling/spec considerations

RE: https://crbug.com/chromium/1241188#c89:  wanderview@: My question for the security group was about holding off on doing anything here until the spec discussion resolved.

@adetaylor, could you please chime in on this?  IMHO if we have a fix that 1) addresses this CSRF / incorrect-Origin-header bug and 2) doesn't introduce new security concerns, then 3) we should proceed with landing the fix sooner rather than later.  This is a tricky area and I may be missing something, but I think that such fix might indeed be possible (e.g. see https://crbug.com/chromium/1241188#c99).  I also think that it is okay to proceed with a partial/imperfect fix, even if subsequent follow-ups might be needed (e.g. to get spec agreement + to cover mode=navigate in OOR-CORS).

### mm...@chromium.org (2021-09-15)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-09-15)

Re https://crbug.com/chromium/1241188#c99 lukasza@: If we enforce manual redirect mode, then the renderer would only be able to control the Origin header in same-origin requests, right?  So it seems okay maybe?  (Unless the renderer-controlled Origin header can be used cross-origin in other requests, where redirects are not required.)

I thought the threat model was a compromised renderer.  If the renderer is compromised, it seems like it could run arbitrary code to append an origin header to a navigation request like this regardless of redirection.  I think the network service needs to validate the origin header on renderer-sourced navigations to prevent this kind of spoofing in compromised renderers.

Or maybe I misunderstand the threat model here?  Sorry for my confusion.

### lu...@chromium.org (2021-09-15)

RE: https://crbug.com/chromium/1241188#c102: wanderview@:

Even if a renderer process is compromised, the NetworkService process can securely enforce that:

1. The renderer can only control the Origin header if mode=navigate (I believe this is already done in OOR-CORS;  if not, then it would be a separate bug)

2. The renderer can only use mode=navigate if
2.1. (secure, trustworthy, browser-process-controlled) request_initiator_origin_lock matches the (untrustworthy, renderer-controlled) request_initiator (or its precursor for opaque initiators)
2.2. the target URL of the request is same-origin with request_initiator (or its precursor for opaque initiators)
2.3. the request uses RedirectMode::kError (I may have misspoke earlier in https://crbug.com/chromium/1241188#c99 about RedirectMode::kManual - it seems that the manual mode might still allow redirects to go through if the renderer calls FollowRedirect later).

I assume that 2.1-2.3 are sufficient to prevent a compromised renderer from triggering HTTP requests that target a URL that is cross-origin from request_initiator.  (Please shout if I missed some scenario here;  redirects seem to be the only known problem here.)

I apologize for missing that in the WIP CL 2.1 was not fully present (because VerifyRequestInitiatorLockWithPluginCheck doesn't verify precursor origins today) - the CL should explicitly compare the initiator-or-precursor with request_initiator_origin_lock (by calling VerifyRequestInitiatorLockWithPluginCheck).

All of 2.1 - 2.3 seem doable in the WIP CL.  It seems that the approach in the WIP CL is most viable one in the short term (although I recognize that its complexity has grown as we continue to explore it;  my unscientific gut-feeling is that proxying would be more complex to achieve).

I don't know if RedirectMode::kError (rather than RedirectMode::kManual) is compatible with functional requirements here.


RE: I think the network service needs to validate the origin header on renderer-sourced navigation

This sounds like a good idea.  As a defense-in-depth it might indeed be worth checking the Origin header in mode=navigate requests to ensure that it is either "Origin: null" or that it matches a non-opaque request_initiator.  (OTOH, it doesn't seem strictly necessary, because (given 2.1-2.3) it seems that a compromised renderer can only lie to the same-origin HTTP server.)

And if RedirectMode::kError cannot be use for some reason, then maybe checking the Origin header is a good idea.  OTOH, it might be worth double-checking with yhirano@ and toyoshim@ on whether applying OOR-CORS to mode=navigate requests might be a preferrable approach.

### wa...@chromium.org (2021-09-15)

> I assume that 2.1-2.3 are sufficient to prevent a compromised renderer from triggering HTTP requests that target a URL that is cross-origin from request_initiator.  (Please shout if I missed some scenario here;  redirects seem to be the only known problem here.)

I think this is only adequate if the network service is adding the origin header based on the request_initiator.  In the current architecture, though, non-get navigations have the origin header added much earlier (in the renderer I believe).  This gives the compromised renderer the ability to change the origin header to whatever it wants irrespective of the request_initiator.

> I don't know if RedirectMode::kError (rather than RedirectMode::kManual) is compatible with functional requirements here.

No, that would not be ok from a spec perspective.  It would be very breaking for the exposed web API.

But can you explain more why the renderer following redirect would be a problem?  Wouldn't it trigger another request that will be validated again by the network service?  It would seem the origin header validation checks would catch any shenanigans here.

### wa...@chromium.org (2021-09-15)

To clarify, I don't think there is anything that says the renderer must set the origin header based on the request_initiator for navigation requests.  (And my testing supports that.)  The network service needs to enforce the restriction.

### wa...@chromium.org (2021-09-15)

The CL is now updated with working unit tests that verify the CORS loader factory is actually blocking bad initiators, headers, and redirect modes.

The CL still needs some cleanup before its ready for review, though.

### lu...@chromium.org (2021-09-16)

RE: https://crbug.com/chromium/1241188#c104: But can you explain more why the renderer following redirect would be a problem?  Wouldn't it trigger another request that will be validated again by the network service?

The validation needs to happen not only in CreateLoaderAndStart / CorsURLLoaderFactory::IsValidRequest, but also in URLLoader::FollowRedirect (AFAIU in RedirectMode::kManualRedirect the network::CORSURLLoader [in NetworkService] will call mojom::URLLoaderClient::OnReceiveRedirect [in a renderer process] which has a comment indicating that the receipient can call back [into the NetworkService process] mojom::URLLoader::FollowRedirect which has an ability to modify and remove http request headers).  Some earlier work in this area happened in https://crbug.com/chromium/973103 and r668849 and mmenke@ might be able to help.

### wa...@chromium.org (2021-09-16)

We had an internal meeting about this today.  Our position going into the spec meeting is going to be that we need to do something like aligning to the safari behavior. (This means preserving the origin header across pass-through fetch handlers.)

Given that, we plan to land our short term fix when its ready, even if the spec discussion is not resolved.  If the spec aligns on a different solution we will have plenty of time to revert the change before it hits stable channel.

### ad...@chromium.org (2021-09-16)

Re https://crbug.com/chromium/1241188#c100:

It sounds like lukasza@ (#c100) and wanderview@ (#c108) are aligned that we should land an interim fix, when it's ready, even if a fuller fix might take longer. That SGTM. I would be opposed to merging this to stable, as I think we should give maximal time for any unanticipated compatibility consequences to show up.

### an...@gmail.com (2021-09-21)

I don't see how preserving the Origin header helps with CSRF. Are you also going to change "site for cookies"? It seems like a very selective change that doesn't address the problem of where authority lies with requests initiated by the service worker.

### wa...@chromium.org (2021-09-21)

The short term fix does more than change the origin header.  It also changes the request_initiator internal field that is used by the network service to populate Sec-Fetch-* headers, etc.  I believe if the request_initiator is not the same as the site for cookies, then samesite cookies will not be sent.  I'm double checking on that, though.

### wa...@chromium.org (2021-09-21)

I think this code is where we use the request_initiator in the samesite cookie computation:

https://source.chromium.org/chromium/chromium/src/+/main:net/cookies/cookie_util.cc;l=153;drc=8f95b5eab2797a3e26bba299f3b0df85bfc98bf5

### an...@gmail.com (2021-09-21)

Ah, that does sound like an interesting middle ground. There will still be the two sources of authority as the service worker will be responsible for enforcing various policies (and presumably Sec-Fetch-Dest would still be "empty", not "document", to avoid confusing CSP) and a number of values associated with the request, but maybe it's good enough? It would not surprise me if we keep running into subtle issues here though.

### wa...@chromium.org (2021-09-22)

The WIP CL is getting close.  I think I have all the requested changes (except comments) in place now.  There are a couple things I still want to do before cleanup/review.

I realized I need to plumb request_initiator through the request stored in cache_storage.  Otherwise we could end up with oddities like:

```
// uses opaque initiator
evt.respondWith(fetch(evt.request));

// uses SW origin initiator
evt.respondWith(async function() {
  const c = await caches.open('foo');
  await c.put(evt.request, new Response(''), { ignoreMethod: true });
  const keys = await c.keys(evt.request);
  return fetch(keys[0]);
}());

This doesn't matter for the origin header since we only permit GET requests in cache_storage, but it could matter for sec-fetch-site, samesite cookies, etc.

I also want to write a test showing that this CL fixes samesite cookie behavior in service workers.

### an...@gmail.com (2021-09-23)

The cache API shouldn't have access to any of those headers though, right? Or are you thinking of including the origin in what it takes to create a cache match?

### wa...@chromium.org (2021-09-23)

>The cache API shouldn't have access to any of those headers though, right? Or are you thinking of including the origin in what it takes to create a cache match?

I'm talking about preserving the internal request_initiator origin field when storing in cache_storage.  There would be no observable difference to the code running in the SW.  The server, however, would continue to get headers/cookies consistent with a passthrough fetch.

The alternative would be to not preserve the request_initiator so it appear the request coming from cache_storage was created by the current service worker's origin.  I guess this might be ok since laundering through cache_storage is a bit weird.  But I hesitate to leave it like that because service workers have no way to tell if an incoming navigation request is from a potentially hostile intiator or not.  So they can't know if its safe to put that request in cache_storage or not.  Maybe we could consider something like a FetchEvent.request.same-origin-initiator flag or something (or maybe same-site-initiator).

### wa...@chromium.org (2021-09-23)

I will say, one thing I dislike about the short term CL fix is that it makes same-site requests appear to be cross-site.  This could be breaking for some sites.

### wa...@chromium.org (2021-09-23)

I've got enough of my same-site cookie test working to see that there is also a potential interop problem here as well.  When we set the request_initiator to be an opaque origin it apparently blocks SameSite=Lax cookies from being sent.  That seems like a potentially pretty big breaking change to me.  It would mean site using passthrough service workers would suddenly have users complaining that when they navigate to their page they are signed out.

lukasza@, do you have any ideas to fix this in the short term approach?  I wonder if I should instead try to get the longer term approach working.

### wa...@chromium.org (2021-09-23)

I'm checking with the SameSite folks as well in case I am missing some other piece of information that allows Lax for these "auxiliary" navigations.

### lu...@chromium.org (2021-09-24)

RE: https://crbug.com/chromium/1241188#c118 and https://crbug.com/chromium/1241188#c119:

Maybe I don't fully understand how samesite cookies are supposed to work, but I would expect that without a service worker a top-level navigation to bar.com would work the same way if it is initiated from 1) opaque origin and 2) cross-site origin foo.com (i.e. I would expect no samesite cookies in both of these cases).  It seems to me that having the same behavior in presence of a "forwarding" service workers is okay.

OTOH, you are right that the fix does risk breaking some websites - requests that were treated as same-origin (no CORS, SameSite cookies, Sec-Fetch-Site, etc) will after the fix be treated as cross-site.  This is unfortunate, but ultimately we *do* want CORS for POST navigations initiated by another origin (and similar argument can be made for SameSite cookies, Sec-Fetch-Site, etc.).

### wa...@chromium.org (2021-09-24)

> Maybe I don't fully understand how samesite cookies are supposed to work, but I would expect that without a service worker a top-level navigation to bar.com would work the same way if it is initiated from 1) opaque origin and 2) cross-site origin foo.com (i.e. I would expect no samesite cookies in both of these cases).  It seems to me that having the same behavior in presence of a "forwarding" service workers is okay.

SameSite=Strict are not sent in this case, but SameSite=:Lax (the default) are supposed to be sent for cross-site main frame navigations.

I think this is failing in my CL because the "main frame" bit comes from the IsolationInfo which is of course not main frame for the service worker.  I'll see if I can find a reasonable way to fix this without being too hacky.

> OTOH, you are right that the fix does risk breaking some websites - requests that were treated as same-origin (no CORS, SameSite cookies, Sec-Fetch-Site, etc) will after the fix be treated as cross-site.  This is unfortunate, but ultimately we *do* want CORS for POST navigations initiated by another origin (and similar argument can be made for SameSite cookies, Sec-Fetch-Site, etc.).

My other concern was more about make same-site initiators look like cross-site initiators.  I agree there should be an origin header, sec-fetch-site, etc, that says something other than same-origin, but forcing same-site to cross-site may break some product integrations.  This one is less likely to be a problem then the cookies, though.

### wa...@chromium.org (2021-09-24)

Ok, I was able to fix SameSite=Lax cookies on navigations.  I'm not sure the fix will be acceptable, though.  It does the following:

1. Plumbs the original request.destination through a fetch().  Not sure this will pass spec discussion.  If not, we can use an internal flag instead.
2. Makes url_request_http_job.cc look at the destination in addition to the IsolationInfo. [1]  This unfortunately moves this SameSite check from being wholely controlled by the browser process to accepting input from the renderer process.  Not sure if this is acceptable.

Networking folks on this bug, what do you think?  Also adding some SameSite cookie folks for their opinion.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:net/url_request/url_request_http_job.cc;l=600;drc=cd71ede85341000da32cc74a2044eb5834e5e05b

### wa...@chromium.org (2021-10-07)

In regards to https://crbug.com/chromium/1241188#c122 I got some feedback from a cookie owner that this is probably ok.  We can also validate that its only set in certain controlled circumstances.

We also had the spec meeting and have general agreement to propagate the internal request origin value.

The meeting did raise another problem, though.  We need to properly taint requests that have performed cross-site redirects.  My CL does not currently do that.  Looks like that will require plumbing through the entire list of redirected URLs in order for this logic to trigger:

https://source.chromium.org/chromium/chromium/src/+/main:services/network/sec_header_helpers.cc;l=107;drc=bc987503e9be79c8d2de7487ef2ef12133fec908

### wa...@chromium.org (2021-10-07)

I have a rough working draft of a CL to fix the redirect tainting:

https://chromium-review.googlesource.com/c/chromium/src/+/3213310

Not sure if I should fold this into my original (quite large) CL or keep it a separate CL.

### [Deleted User] (2021-10-22)

wanderview: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2021-10-22)

I'm getting close to requesting review on my main CL.  There will then be a couple follow-up CLs.

### wa...@chromium.org (2021-10-22)

Here is an (internal) document describing all the changes I intend to make over 3 CLs.

https://docs.google.com/document/d/1KZscujuV7bCFEnzJW-0DaCPU-I40RJimQKoCcI0umTQ/edit?usp=sharing

I put this together because it felt like a lot of context to include in the CLs while the bug is still private.

### wa...@chromium.org (2021-10-25)

The first CL is finally out for review:

https://chromium-review.googlesource.com/c/chromium/src/+/3115917

### gi...@appspot.gserviceaccount.com (2021-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/da0a6501cf321579bd46a27ff9fba1bb8ea910bb

commit da0a6501cf321579bd46a27ff9fba1bb8ea910bb
Author: Ben Kelly <wanderview@chromium.org>
Date: Thu Oct 28 19:19:49 2021

Fetch: Plumb request initiator through passthrough service workers.

This CL contains essentially two changes:

1. The request initiator origin is plumbed through service workers
   that do `fetch(evt.request)`.  In addition to plumbing, this
   requires changes to how we validate navigation requests in the
   CorsURLLoaderFactory.
2. Tracks the original destination of a request passed through a
   service worker.  This is then used in the network service to force
   SameSite=Lax cookies to treat the request as a main frame navigation
   where appropriate.

For more detailed information about these changes please see the
internal design doc at:

https://docs.google.com/document/d/1KZscujuV7bCFEnzJW-0DaCPU-I40RJimQKoCcI0umTQ/edit?usp=sharing

In addition, there is some discussion of these features in the following
spec issues:

https://github.com/whatwg/fetch/issues/1321
https://github.com/whatwg/fetch/issues/1327

The test includes WPT tests that verify navigation headers and SameSite
cookies.  Note, chrome has a couple expected failures in the SameSite
cookie tests because of the "lax-allowing-unsafe" intervention that is
currently enabled.  See:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/TestExpectations;l=4635;drc=e8133cbf2469adb99c6610483ab78bcfb8cc4c76

Bug: 1115847,1241188
Change-Id: I7e236fa20aeabb705aef40fcf8d5c36da6d2798c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3115917
Reviewed-by: Matt Menke <mmenke@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/main@{#936029}

[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/renderer/platform/loader/fetch/resource_request.h
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/same-site-cookies.https-expected.txt
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/public/cpp/url_request_mojom_traits.h
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/cors/cors_url_loader_unittest.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/content/common/fetch/fetch_request_type_converters.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/public/cpp/resource_request.h
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/fetch-rewrite-worker.js
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/renderer/core/fetch/fetch_request_data.h
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/net/url_request/url_request_http_job.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/renderer/core/fetch/fetch_manager.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/net/url_request/url_request.cc
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/same-site-cookies-unregister.html
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/renderer/platform/loader/fetch/url_loader/request_conversion.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/public/mojom/fetch/fetch_api_request.mojom
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/public/mojom/url_request.mojom
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/net/url_request/url_request_unittest.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/renderer/core/fetch/fetch_request_data.cc
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/form-poster.html
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/same-site-cookies.https.html
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/fetch-rewrite-worker.js.headers
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/cors/cors_url_loader_factory.cc
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/location-setter.html
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/cors/cors_url_loader_factory_unittest.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/net/url_request/url_request.h
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/BUILD.gn
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/cors/cors_url_loader.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/renderer/modules/cache_storage/inspector_cache_storage_agent.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/renderer/core/fetch/request.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/url_loader.cc
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/navigation-headers.https.html
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/navigation-headers-server.py
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/services/network/public/cpp/url_request_mojom_traits.cc
[modify] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/content/common/background_fetch/background_fetch_types.cc
[add] https://crrev.com/da0a6501cf321579bd46a27ff9fba1bb8ea910bb/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/same-site-cookies-register.html


### wa...@chromium.org (2021-10-28)

Note, this still needs another CL in order to fix redirects.

### gi...@appspot.gserviceaccount.com (2021-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a

commit a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a
Author: Alan Screen <awscreen@chromium.org>
Date: Thu Oct 28 22:04:50 2021

Revert "Fetch: Plumb request initiator through passthrough service workers."

This reverts commit da0a6501cf321579bd46a27ff9fba1bb8ea910bb.

Reason for revert: Failure on many bots with the following error message:
The service worker navigation preload request was cancelled before 'preloadResponse' settled. If you intend to use 'preloadResponse', use waitUntil() or respondWith() to wait for the promise to settle.", source:  (0)

Original change's description:
> Fetch: Plumb request initiator through passthrough service workers.
>
> This CL contains essentially two changes:
>
> 1. The request initiator origin is plumbed through service workers
>    that do `fetch(evt.request)`.  In addition to plumbing, this
>    requires changes to how we validate navigation requests in the
>    CorsURLLoaderFactory.
> 2. Tracks the original destination of a request passed through a
>    service worker.  This is then used in the network service to force
>    SameSite=Lax cookies to treat the request as a main frame navigation
>    where appropriate.
>
> For more detailed information about these changes please see the
> internal design doc at:
>
> https://docs.google.com/document/d/1KZscujuV7bCFEnzJW-0DaCPU-I40RJimQKoCcI0umTQ/edit?usp=sharing
>
> In addition, there is some discussion of these features in the following
> spec issues:
>
> https://github.com/whatwg/fetch/issues/1321
> https://github.com/whatwg/fetch/issues/1327
>
> The test includes WPT tests that verify navigation headers and SameSite
> cookies.  Note, chrome has a couple expected failures in the SameSite
> cookie tests because of the "lax-allowing-unsafe" intervention that is
> currently enabled.  See:
>
> https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/TestExpectations;l=4635;drc=e8133cbf2469adb99c6610483ab78bcfb8cc4c76
>
> Bug: 1115847,1241188
> Change-Id: I7e236fa20aeabb705aef40fcf8d5c36da6d2798c
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3115917
> Reviewed-by: Matt Menke <mmenke@chromium.org>
> Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
> Reviewed-by: Nasko Oskov <nasko@chromium.org>
> Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
> Commit-Queue: Ben Kelly <wanderview@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#936029}

Bug: 1115847,1241188
Change-Id: I3044a6d20de172b4a8ab7e39a9f26191580003fa
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3251692
Auto-Submit: Alan Screen <awscreen@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Alan Screen <awscreen@chromium.org>
Owners-Override: Alan Screen <awscreen@chromium.org>
Cr-Commit-Position: refs/heads/main@{#936125}

[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/renderer/platform/loader/fetch/resource_request.h
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/same-site-cookies.https-expected.txt
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/public/cpp/url_request_mojom_traits.h
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/cors/cors_url_loader_unittest.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/content/common/fetch/fetch_request_type_converters.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/fetch-rewrite-worker.js
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/public/cpp/resource_request.h
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/renderer/core/fetch/fetch_request_data.h
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/net/url_request/url_request_http_job.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/renderer/core/fetch/fetch_manager.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/net/url_request/url_request.cc
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/same-site-cookies-unregister.html
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/renderer/platform/loader/fetch/url_loader/request_conversion.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/public/mojom/fetch/fetch_api_request.mojom
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/net/url_request/url_request_unittest.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/public/mojom/url_request.mojom
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/renderer/core/fetch/fetch_request_data.cc
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/form-poster.html
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/fetch-rewrite-worker.js.headers
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/same-site-cookies.https.html
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/cors/cors_url_loader_factory.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/cors/cors_url_loader_factory_unittest.cc
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/location-setter.html
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/net/url_request/url_request.h
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/BUILD.gn
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/renderer/modules/cache_storage/inspector_cache_storage_agent.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/third_party/blink/renderer/core/fetch/request.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/cors/cors_url_loader.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/url_loader.cc
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/navigation-headers.https.html
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/navigation-headers-server.py
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/services/network/public/cpp/url_request_mojom_traits.cc
[modify] https://crrev.com/a6601b2cf2bb7c0a0ffa3c795a0dbc730ef81d1a/content/common/background_fetch/background_fetch_types.cc
[delete] https://crrev.com/b91ae55530943cc4c51f30f90a63ce77c65808dd/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/same-site-cookies-register.html


### gi...@appspot.gserviceaccount.com (2021-10-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d916566085e4f09bca93021f2b1650ea6237077

commit 2d916566085e4f09bca93021f2b1650ea6237077
Author: Ben Kelly <wanderview@chromium.org>
Date: Fri Oct 29 21:19:29 2021

Reland "Fetch: Plumb request initiator through passthrough service workers."

This is a reland of da0a6501cf321579bd46a27ff9fba1bb8ea910bb

This CL also includes a change to mark the two WPT tests as requiring
long timeout durations.  On my fast build machine with an opt build
they take ~5 seconds each to complete and the default timeout is 10
seconds.  On slower bots with debug builds its highly likely that these
tests would be marked as timing out.  This change gives them a 60 second
timeout instead.

Original change's description:
> Fetch: Plumb request initiator through passthrough service workers.
>
> This CL contains essentially two changes:
>
> 1. The request initiator origin is plumbed through service workers
>    that do `fetch(evt.request)`.  In addition to plumbing, this
>    requires changes to how we validate navigation requests in the
>    CorsURLLoaderFactory.
> 2. Tracks the original destination of a request passed through a
>    service worker.  This is then used in the network service to force
>    SameSite=Lax cookies to treat the request as a main frame navigation
>    where appropriate.
>
> For more detailed information about these changes please see the
> internal design doc at:
>
> https://docs.google.com/document/d/1KZscujuV7bCFEnzJW-0DaCPU-I40RJimQKoCcI0umTQ/edit?usp=sharing
>
> In addition, there is some discussion of these features in the following
> spec issues:
>
> https://github.com/whatwg/fetch/issues/1321
> https://github.com/whatwg/fetch/issues/1327
>
> The test includes WPT tests that verify navigation headers and SameSite
> cookies.  Note, chrome has a couple expected failures in the SameSite
> cookie tests because of the "lax-allowing-unsafe" intervention that is
> currently enabled.  See:
>
> https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/TestExpectations;l=4635;drc=e8133cbf2469adb99c6610483ab78bcfb8cc4c76
>
> Bug: 1115847,1241188
> Change-Id: I7e236fa20aeabb705aef40fcf8d5c36da6d2798c
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3115917
> Reviewed-by: Matt Menke <mmenke@chromium.org>
> Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
> Reviewed-by: Nasko Oskov <nasko@chromium.org>
> Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
> Commit-Queue: Ben Kelly <wanderview@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#936029}

Bug: 1115847,1241188
Change-Id: Ia26acbdd0d7ce6583d9a44f83ed086708657b8bd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3251368
Reviewed-by: Matt Menke <mmenke@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Auto-Submit: Ben Kelly <wanderview@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/main@{#936560}

[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/renderer/platform/loader/fetch/resource_request.h
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/same-site-cookies.https-expected.txt
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/public/cpp/url_request_mojom_traits.h
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/cors/cors_url_loader_unittest.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/content/common/fetch/fetch_request_type_converters.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/fetch-rewrite-worker.js
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/public/cpp/resource_request.h
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/renderer/core/fetch/fetch_request_data.h
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/net/url_request/url_request_http_job.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/net/url_request/url_request.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/renderer/core/fetch/fetch_manager.cc
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/same-site-cookies-unregister.html
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/renderer/platform/loader/fetch/url_loader/request_conversion.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/public/mojom/fetch/fetch_api_request.mojom
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/net/url_request/url_request_unittest.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/public/mojom/url_request.mojom
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/renderer/core/fetch/fetch_request_data.cc
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/form-poster.html
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/same-site-cookies.https.html
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/fetch-rewrite-worker.js.headers
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/cors/cors_url_loader_factory.cc
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/location-setter.html
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/cors/cors_url_loader_factory_unittest.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/net/url_request/url_request.h
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/BUILD.gn
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/cors/cors_url_loader.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/renderer/modules/cache_storage/inspector_cache_storage_agent.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/renderer/core/fetch/request.cc
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/navigation-headers.https.html
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/url_loader.cc
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/navigation-headers-server.py
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/services/network/public/cpp/url_request_mojom_traits.cc
[modify] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/content/common/background_fetch/background_fetch_types.cc
[add] https://crrev.com/2d916566085e4f09bca93021f2b1650ea6237077/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/same-site-cookies-register.html


### wa...@chromium.org (2021-11-03)

Second CL up for review:

https://chromium-review.googlesource.com/c/chromium/src/+/3213310

### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/579df7b562fd2a85591e44fd314a1710c93e6901

commit 579df7b562fd2a85591e44fd314a1710c93e6901
Author: Ben Kelly <wanderview@chromium.org>
Date: Tue Nov 09 15:48:30 2021

Fetch: Plumb navigation redirect chain through service workers

Navigation redirection works differently than normal redirection.
Navigation requests are made using "manual" redirect mode which means
the redirect is not immediately followed.  Instead the redirect location
is handed back up to the NavigationURLLoaderImpl which then manually
follows the redirect.  This results in a new request being sent for each
step in the redirect chain.

This CL plumbs the redirect chain information from
NavigationURLLoaderImpl down through each request so it can be included
with requests proxied by a passthrough service worker.

For more detailed information about these changes please see the
internal design doc at:

https://docs.google.com/document/d/1KZscujuV7bCFEnzJW-0DaCPU-I40RJimQKoCcI0umTQ/edit?usp=sharing

We have rough consensus to make this change in this spec issue:

https://github.com/whatwg/fetch/issues/1335

Note, this CL includes some expected test failures.  These are due to
the "lax-allowing-unsafe" intervention that is currently enabled.  See:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/TestExpectations;l=4635;drc=e8133cbf2469adb99c6610483ab78bcfb8cc4c76

Bug: 1115847,1241188
Change-Id: I2a2a17639e0bec3222684e0d444d6d98a21402ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3213310
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/main@{#939851}

[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/renderer/platform/loader/fetch/resource_request.h
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/web_tests/external/wpt/service-workers/service-worker/same-site-cookies.https-expected.txt
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/services/network/public/cpp/url_request_mojom_traits.h
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/services/network/cors/cors_url_loader_unittest.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/content/common/fetch/fetch_request_type_converters.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/services/network/public/cpp/resource_request.h
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/renderer/core/fetch/fetch_request_data.h
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/renderer/core/fetch/fetch_manager.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/net/url_request/url_request.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/renderer/platform/loader/fetch/url_loader/request_conversion.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/public/mojom/fetch/fetch_api_request.mojom
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/services/network/public/mojom/url_request.mojom
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/net/url_request/url_request_unittest.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/renderer/core/fetch/fetch_request_data.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/form-poster.html
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/web_tests/external/wpt/service-workers/service-worker/same-site-cookies.https.html
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/services/network/cors/cors_url_loader_factory.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/location-setter.html
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/services/network/cors/cors_url_loader_factory_unittest.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resources/redirect.py
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/net/url_request/url_request.h
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/renderer/core/fetch/request.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/renderer/modules/cache_storage/inspector_cache_storage_agent.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/third_party/blink/web_tests/external/wpt/service-workers/service-worker/navigation-headers.https.html
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/services/network/url_loader.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/content/browser/loader/navigation_url_loader_impl.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/services/network/public/cpp/url_request_mojom_traits.cc
[modify] https://crrev.com/579df7b562fd2a85591e44fd314a1710c93e6901/content/common/background_fetch/background_fetch_types.cc


### wa...@chromium.org (2021-11-09)

I believe this is now fixed.  The first CL landed in M97 and I believe the second CL landed in M98.  I would prefer not to merge anything here because the CLs are huge, but we could maybe merge the second CL to M97 since the branch point was recent.

### wa...@chromium.org (2021-11-09)

FWIW, I'm also still working on spec pull requests to reflect the new behavior.

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-17)

Congratulations -- the VRP Panel has decided to award you $3000 for this report. A member of our finance tam will be in touch soon to arrange for payment. Thank you for reporting this issue to us! 

### ho...@gmail.com (2021-11-17)

@amyressler thank you so much! Also like to extend a BIG THANK YOU to everyone involved in this from managing the issue, to spec discussion and clarification and eventual patch! Your all amazing :-)

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-11)

Not requesting merge to dev (M98) because latest trunk commit (939851) appears to be prior to dev branch point (950365). If this is incorrect, please replace the Merge-NA-98 label with Merge-Request-98. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### yo...@chromium.org (2022-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ki...@gmail.com (2022-04-20)

Since the restriction removed, I’ve been able to finally follow up on the whole issue (I reported https://crbug.com/chromium/1115847) and I see many conversations happened here. Great work all!

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1241188?no_tracker_redirect=1

[Multiple monorail components: Blink>ServiceWorker, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056924)*
