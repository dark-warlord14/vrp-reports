# Security: Extensions can run code in the local/instant NTP

| Field | Value |
|-------|-------|
| **Issue ID** | [40089982](https://issues.chromium.org/issues/40089982) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ka...@chromium.org |
| **Created** | 2017-12-23 |
| **Bounty** | $500.00 |

## Description

Chrome version: 63.0.3239.108

Chrome extensions can intercept a script request and run JS code in the local NTP ( chrome-search://local-ntp/local-ntp.html ). This is problematic because the page is a kind of privileged page. For example, the NTP has the following capabilities:
- The omnibox is empty by default.
- The page has APIs to put text in the omnibox.
- The page can steal focus (even if another application is focused).
- The page can query and manipulate the browsing history (most visited sites).

Steps to reproduce:
1. Load the attached extension (it will open the local NTP).

Expected result:
- A new tab page should be opened, and look normal.

Actual result:
- A new tab page is opened, the page content is spinning and the omnibox is continuously updated and stealing focus from other applications (I have only confirmed focus stealing behavior on Linux, other platforms are untested).

Explanation of exploit:
The "local NTP" loads a script from chrome-search://local-ntp/one-google.js (see local_ntp.js [1]), and uses the result to inject additional HTML, script and CSS in the page.
Contrary to what one may expect, this resource is not local, but generated from https://www.google.com/async/newtab_ogb (via OneGoogleBarFetcherImpl [2]).
Extensions can somehow intercept this request with the webRequest API and consequently run arbitrary scripts in the NTP, and abuse its privileges.

Extensions are not expected to observe, let alone modify such requests. This is probably a bug in one of the following places:
- OneGoogleBarFetcherImpl::Start [2]
- WebRequestPermissions::HideRequest [3]


[1] https://chromium.googlesource.com/chromium/src/+/5ea97e516ffd9d05c899d2a0fb308332f73c259c/chrome/browser/resources/local_ntp/local_ntp.js#549
[2] https://chromium.googlesource.com/chromium/src/+/818b1378d1974d65a4dd24f2e9f43711afdffe93/chrome/browser/search/one_google_bar/one_google_bar_fetcher_impl.cc#199
[3] https://chromium.googlesource.com/chromium/src/+/0928665a2f97833277504d979800bc45cc526da1/extensions/browser/api/web_request/web_request_permissions.cc#103

## Attachments

- [local-ntp-compromised.zip](attachments/local-ntp-compromised.zip) (application/octet-stream, 2.1 KB)
- [remote-ntp-compromised.zip](attachments/remote-ntp-compromised.zip) (application/octet-stream, 2.1 KB)

## Timeline

### rs...@chromium.org (2017-12-28)

treib: As OWNER of this code, can you help route?

[Monorail components: Platform>Extensions]

### sh...@chromium.org (2018-01-06)

treib: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tr...@chromium.org (2018-01-09)

I just came back from vacation, I'll take a look at this today.

I'm quite surprised that extensions can apparently intercept arbitrary HTTPS requests with that API?!
Does the same work on the remote NTP? It also dynamically loads the OneGoogleBar, and I don't immediately see why the same thing wouldn't apply there as well.

### tr...@chromium.org (2018-01-09)

I've confirmed that the same thing works on the remote NTP as well; modified repro extension attached.

(Also small fix to the original repro: It tries to use chrome.searchBox which doesn't exist anymore in recent versions of Chrome, so the omnibox clobbering doesn't work. If you use chrome.embeddedSearch.searchBox instead, it works again.)

Overall, I think this is simply a consequence of how the webRequest API is designed: If an extension is allowed to intercept requests to google.com, then it can do anything it wants on Google pages, including the NTP. It's maybe surprising that this applies to the local NTP too, but it's really no worse than on the remote NTP. We *could* put some extra protections in place to prevent this on the local NTP, but I'm not entirely convinced it's worth it.

### tr...@chromium.org (2018-01-09)

Thinking about this some more, we do have protections in place to prevent extensions from injecting code into the NTP (though I'm not exactly sure why). This is a way to circumvent those protections. To be consistent, we should probably try to prevent this as well.

### rd...@chromium.org (2018-01-09)

A few quick notes:
- Yes, webRequest can intercept https requests and requests to google.com (very much by design).  Otherwise the ultimate ad blocker thwarting would be serving ads over https :)
- Resources that are sensitive should be filtered out. We do this with a number of different resources that are remote, but shouldn't be modified (e.g. clients[0-9].google.com, chrome.google.com/webstore, safe browsing APIs, etc).  If this script is to remain used by the NTP, we should account for it.

### rd...@chromium.org (2018-01-09)

(Grr... submitted too soon - continuing)

- Extensions aren't allowed to modify the NTP with scripts because a) it is semi-privileged (as Rob described) and b) there's a separate API to do that with attribution and safety (chrome url overrides).  Modifying the Chrome NTP is prohibited.
- This issue would also be fixed if we properly limited webRequest to require the extension to have access to the requesting page in addition to the requested resource - something we've hoped to do for awhile, but is potentially breaking.  Karan's looking into that.

Marc, can you add some more detail about what this script is and why we need it?  Generally, we don't like to import resources from the web into any kind of privileged UI.  The NTP isn't fully privileged (thank goodness it's not chrome://settings!), but it's still not good...  Is there any chance we could have this file stored in chromium/chrome?

### cr...@chromium.org (2018-01-09)

Maybe it would be possible to identify that the request is coming from an NTP process and prevent the API from applying to it, while still letting the API intercept requests for the same URL in web processes?

### rd...@chromium.org (2018-01-09)

That's the policy we'd *like* to institute for all of web request, because of other issues.  Last I heard, we *should* be able to determine the requesting frame and origin for any resource by the time it gets to the ChromeExtensionsNetworkDelegate, which would let us do this.  Is that still accurate?  And can we do that from the chrome/extensions layer?  Ideally without any thread hops, if I'm completing my wishlist? :)

### tr...@chromium.org (2018-01-10)

Re #7: The script in question is for the OneGoogleBar. It's user-specific, it offers Google account features for signed-in users, so it's not possible to bake it into Chrome.

Re #8: For the remote NTP, the request comes from an Instant renderer, which we can probably detect and then block the API from meddling with it. But for the local NTP, the request comes from the browser process, so there that won't work.

The simplest way to fix this would be to filter out requests to "https://www.google.TLD/chrome/newtab" (for the remote NTP) and "https://www.google.TLD/chrome/newtab_ogb" (for the local NTP), but that's bound to break again when new features are added.


One step back: Why is the webRequest API allowed to intercept requests from the browser process at all? That seems like inviting them to mess with browser features, since definitely not all features use only "clients*.google.com" URLs.

### tr...@chromium.org (2018-01-10)

Argh, mistyped the URLs to be filtered above. The correct URLs to filter out are "https://www.google.TLD/async/newtab" and "https://www.google.TLD/async/newtab_ogb".

### rd...@chromium.org (2018-01-10)

@10
> One step back: Why is the webRequest API allowed to intercept requests from the browser process at all? That seems like inviting them to mess with browser features, since definitely not all features use only "clients*.google.com" URLs.

It depends on what you define as "from the browser process".  We only expose requests made through the BrowserContext's URLRequestContext, so something using the system request context will *not* be exposed to extensions.  Ideally, that's what most things would use for privileged/protected requests that shouldn't be messed with.  However, some of these requests also rely on e.g. the cookies of the browser context.  I could see a desired state where we have two request contexts for a browser context - one protected and one not - but I don't know for sure if that's sane and I don't think anyone has the bandwidth to tackle it.  We can't just filter out browser-initiated requests, since that would include things like user navigations from typing in the omnibox or right-click-open-in-new-tab - which need to be included.  And even if we did, the request for the script is in fact made by the renderer in this case, right?  The right solution really is to just enforce that an extension has permission to modify the requesting origin.

On a separate note, a thought for security triagers: I'm not quite sure this is severity-medium.  Modifying the NTP is not good, but not absolutely evil, and was in fact easily achievable before a behavior change in the last couple months.  I'd say this is severity-low.  But I'm not entirely familiar with all the criteria.

### mn...@chromium.org (2018-01-10)

[Empty comment from Monorail migration]

### tr...@chromium.org (2018-01-10)

@12
There are two separate cases here:

1) The remote NTP.
The request is initiated by the renderer, and its origin is www.google.ccTLD.

2) The local NTP (as originally reported).
Here, the request is initiated by the browser, so it doesn't have an origin/referer. It does need the BrowserContext's cookie jar though, so it can't use the system request context.

In either case, I don't see any good way to filter out these requests.


Agreed on severity-low.

### ro...@robwu.nl (2018-01-10)

> Modifying the NTP is not good, but not absolutely evil, and was in fact easily achievable before a behavior change in the last couple months.

Are you referring to chrome_url_overrides? Extensions can replace the NTP, but the resulting page runs in an extension process, whereas the NTP runs in a special NTP process, with access to APIs that are normally unavailable to extensions (see the report for some examples).


If you need a way to filter out requests, a way to do so is to call URLFetcher::SetInitator with some dummy value (e.g. a URL with the "chrome-search:" scheme) in OneGoogleBarFetcherImpl::AuthenticatedURLFetcher::Start, and filter out all events with that dummy value in WebRequestPermissions::CanExtensionAccessURL.
The initiator is empty by default, and in this way browser-initiated requests can be attributed to a specific entity without major changes to net/.

### tr...@chromium.org (2018-01-10)

I think Devlin just meant that the "extensions can't access the NTP" rule wasn't always around?

Thanks for the hint about SetInitiator! That indeed works fine and seems like a good solution for the local NTP. It doesn't really help with the remote NTP though, since there the initiator will just be "https://www.google.com" (or "https://www.bing.com" or whatever your default search engine is).

### rd...@chromium.org (2018-01-10)

>> Are you referring to chrome_url_overrides? Extensions can replace the NTP, but the resulting page runs in an extension process, whereas the NTP runs in a special NTP process, with access to APIs that are normally unavailable to extensions (see the report for some examples).
> I think Devlin just meant that the "extensions can't access the NTP" rule wasn't always around?

Correct - this was only changed as part of revision 993682e9e2b181a14f9fd9e6a7f848e401a551e7.  Before that, it was actually trivial to run scripts in the NTP.  We now disallow it because we much prefer extensions use the chrome_url_overrides (for the reasons you site and others).  But for years, this was possible, and even used (Pocket in particular had this behavior).

Regarding a fix, a short-term, band-aid fix would be to just add these urls as other sensitive urls (e.g., in IsSensitiveUrl()). However, that would only work if these resources were *only* requested by the NTP (or other "built-in" pieces) - if they are also requested by vanilla google.com, that's no good.  Do you know if they are, Marc?

Rob's idea about setting some initiator and checking it would work for the browser-initiated, though I think it might be cleaner/more straight-forward to just set a flag somewhere on URLRequest or ResourceRequestInfo or similar to indicate that it's supposed to be protected.  Charlie or Nasko, any thoughts there?

And, of course, just to be a broken record... we *really* should just enforce that the extension has access to the renderer making the request (which would work for the remote NTP *without* needing to have (more) magic urls in the IsSensitiveUrl() method.

### tr...@chromium.org (2018-01-10)

> Regarding a fix, a short-term, band-aid fix would be to just add these urls as other sensitive urls (e.g., in IsSensitiveUrl()). However, that would only work if these resources were *only* requested by the NTP (or other "built-in" pieces) - if they are also requested by vanilla google.com, that's no good.  Do you know if they are, Marc?

Yes, both of these endpoints are specific to their respective NTPs and are not used from anywhere else. So the band-aid fix should at least work.

### tr...@chromium.org (2018-01-18)

I have a pending CL with the "initiator" fix (which only works for the local NTP, not the remote one) here: https://crrev.com/c/870470

Devlin, did I read correctly that you'd prefer the "band-aid" fix of blacklisting the relevant URLs for now?
Any chance of getting the proper fix (ensuring access to the renderer)?

### tr...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### rd...@chromium.org (2018-01-24)

We won't be able to add the proper fix until we add UMA to see how many extensions it would affect, so I think we need to go with the band-aid approach for now.  I'll draft a CL.

### rd...@chromium.org (2018-01-24)

Actually, I'm wondering if we can do slightly better here.  While we can't use the proper "make sure the extension can access the requesting frame" fix globally, we might be able to at least do it for the NTP, which would ensure that we don't need to do this again if anyone adds a new URL.

In talking with creis@ and nasko@, it seems like URLRequest::initiator() *should* be sufficient in this case.  In particular, it should have the origin of the requesting frame (which will be null in the case of a browser-initiated request, as for the local NTP, or the NTP for a renderer-initiated frame, as for the remote version).  mkwst@, Charlie suggested I run this by you as well - would using initiator() here be sufficient and sane?

### rd...@chromium.org (2018-01-24)

We discussed offline, and decided this was closer to Security_Severity-Low.  Updating accordingly.

### rd...@chromium.org (2018-01-24)

Re #22, this actually becomes slightly harder, because the initiator in the renderer case is www.google.com, rather than chrome://newtab.  Dang.

What's more, it looks like some more stuff is potentially leaked to the extension, rather than just /async/newtab.  For instance, I see one here for https://www.google.com/_/chrome/newtab-serviceworker.js.  Marc, are you sure those aren't ones we need to protect?

### tr...@chromium.org (2018-01-25)

Good catch - the service worker should certainly also be protected if it isn't already. (Can extensions replace other pages' service workers?)

So if there's a way to protect all requests coming from an NTP (local or remote), then that's IMO a lot better than blacklisting certain target URLs. Since the initiator is only an origin rather than a full URL, that won't work for the remote NTP unfortunately. Could we (ab)use the referrer maybe?

### rd...@chromium.org (2018-01-25)

> (Can extensions replace other pages' service workers?)
Trivially by redirecting the call to the script, AFAIK.

> Could we (ab)use the referrer maybe?
I dunno about this... it seems very fragile, and more likely to break in either the direction of being too strict (and protecting google properties that shouldn't be) or not strict enough (and missing some from the NTP).  I think we really do need to just protect all requests from the NTP, and find the proper way of plumbing that through.



We already know if a request has WebUI bindings, which is a good start.  Unfortunately, there have been times in the past where we were overly liberal with giving renderers these bindings, and I don't feel comfortable using that alone as a signal to block.

Nasko, Charlie, Mike - any ideas here how we could, on the IO thread at the time of the request, definitively tell if something is originating from the NTP?  Is there some way we could put this on NavigationUIData or similar?

### tr...@chromium.org (2018-01-25)

I'm pretty sure that anything with WebUI bindings must absolutely be protected from meddling by extensions. But neither the local nor the remote NTP have WebUI bindings (the incognito/guest mode NTPs do).

Re detecting NTPs on the IO thread: SearchBouncer [1] lives on the IO thread and knows the remote NTP URL. For the local NTP, it's enough to compare the origin to "chrome-search://local-ntp".

What exactly does "originating from the NTP" mean - e.g. what about an iframe embedded on the NTP?

[1] https://cs.chromium.org/chromium/src/chrome/renderer/searchbox/search_bouncer.h

### rd...@chromium.org (2018-01-25)

> I'm pretty sure that anything with WebUI bindings must absolutely be protected from meddling by extensions.

You'd think!  But before https://crbug.com/chromium/659798 was fixed, we gave web ui bindings to all extension contents.  Admittedly, extensions shouldn't normally be affecting other extensions, but it mostly shows that there may be times that we give web ui bindings to things that aren't necessarily sacred.  Complicating matters more, webui bindings are granted to a full process, so until we have strict isolation for all webui renderers (or do we already?  That'd be awesome!), there's a chance it may be shared with other content.

And, yes, you're right - the NTPs don't have WebUI, I was wrong.  So, there's that idea gone.

> Re detecting NTPs on the IO thread: SearchBouncer [1] lives on the IO thread and knows the remote NTP URL. For the local NTP, it's enough to compare the origin to "chrome-search://local-ntp"

This doesn't help enough, because we don't know the full url of the initiator, only the origin.  And we can't just check for www.google.com.

> What exactly does "originating from the NTP" mean - e.g. what about an iframe embedded on the NTP?

By "originating from the NTP", I mean a resource request that's created on behalf of the NTP.  So if the NTP includes script.js, that would originate from the NTP.  Iframes are also potentially tricky, because I don't think we'd necessarily want to allow an extension that can run on example.com to intercept requests from an example.com frame that's embedded in google.com - but having full access to the frame tree information is much harder, and it would still be a strictly better situation than we have now.

### sh...@chromium.org (2018-01-27)

[Empty comment from Monorail migration]

### rd...@chromium.org (2018-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### ka...@chromium.org (2018-04-05)

If we want to avoid hardcoding the specific url endpoints being used, we can:

For browser initiated requests (local ntp case), I think just adding some field (say is_protected) to the url request which can then be fetched from ResourceRequestInfo, should suffice. Alternatively, adding some dummy initiator as suggested, should also work, but that's a bit ugly. Also, I see requests also have NetworkTrafficAnnotationTag associated with them. I don't have much context into what it is meant to be used for, but can that be used as a signal to whitelist the request?

For renderer initiated requests (remote NTP case), it seems we keep track of the process ids of these instant renderers, even on the IO thread. See InstantService/InstantIOContext. Shouldn't this suffice to track that the request initiated from an NTP renderer. We already know the render process id that generated the request.

### rd...@chromium.org (2018-04-05)

The local NTP case is a little easier, yeah.  Adding something to the URL request should be sufficient, or potentially just using the initiator of the request, if set.  I'm more worried about the remote NTP case (since this is also much more common).

I don't think looking at process IDs alone would necessarily be sufficient, because there might be other renderers in that process, and we wouldn't want to blanket-protect a process if there are other requests that don't originate from the NTP.

Charlie, Nasko - with site isolation, how does chrome://newtab work?  Is it isolated to chrome://newtab pages, chrome:// pages, or google.com pages?  If it's one of the former, blocking based on process would actually work - but if it's lumped into any google.com site, then it would be insufficient.

### tr...@chromium.org (2018-04-05)

There shouldn't be anything except NTPs in the NTP renderer process, see search::ShouldAssignURLToInstantRenderer. (The "Instant" naming is a relic, today "Instant" == "NTP".) So I think this approach should work.

"chrome://newtab" as a URL barely exists, it gets rewritten to the actual NTP URL very early on, see search::HandleNewTabURLRewrite.

### rd...@chromium.org (2018-04-05)

Karan has heroically offered to take this one over, since it's somewhat related to work he's done recently.

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### ka...@chromium.org (2018-04-20)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/1018724

### ka...@chromium.org (2018-04-23)

The above CL should take care of the NTP-renderer initiated requests. I tried logging NTP requests and we probably need to do something for some browser initiated requests as well:

1) Request made by OneGoogleBarFetcherImpl - https://www.google.com/async/newtab_ogb* (Local NTP)
2) Request made by LogoTracker::FetchLogo https://www.google.com/async/ddljson* (Local NTP).
3) Duplicate service worker request made by ServiceWorkerWriteToCacheJob - https://www.google.com/_/chrome/newtab-serviceworker.js (Remote NTP)
4) Thumbnails requests made by ThumbnailSource - https://www.google.com/webpagethumbnail* (Remote NTP)

It seems we would want to at least protect request made by OneGoogleBarFetcherImpl (since it's a script request). Not quite sure about the other requests. Also, is possible if these requests could be made through the NTP renderer itself?

### bu...@chromium.org (2018-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5d00f36cfb22129d6d551eb570ce653edc0fa084

commit 5d00f36cfb22129d6d551eb570ce653edc0fa084
Author: Karan Bhatia <karandeepb@chromium.org>
Date: Tue Apr 24 20:51:04 2018

Extensions: Hide network requests from the NTP renderer.

The NTP (New tab page) renderer is a semi-priveleged process having access to
some special APIs. But currently, network requests made by an NTP renderer can
be intercepted by extensions using the web request API.

This CL hides network requests made by an NTP renderer from extensions. This
works since it's guaranteed that the NTP won't share the renderer process with
any other site.

BUG=797461

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: Id8523aa7cbb4e5fb74256fa6cfc180709849568a
Reviewed-on: https://chromium-review.googlesource.com/1018724
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Marc Treib <treib@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#553265}
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/browser/extensions/api/chrome_extensions_api_client.cc
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/browser/extensions/api/chrome_extensions_api_client.h
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/browser/extensions/api/web_request/web_request_apitest.cc
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/browser/search/instant_io_context.cc
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/browser/search/instant_io_context.h
[add] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/test/data/extensions/api_test/webrequest/ntp_request_interception/extension/background.js
[add] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/test/data/extensions/api_test/webrequest/ntp_request_interception/extension/manifest.json
[add] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/test/data/extensions/api_test/webrequest/ntp_request_interception/fake_ntp.html
[add] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/test/data/extensions/api_test/webrequest/ntp_request_interception/fake_ntp_script.js
[add] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/chrome/test/data/extensions/api_test/webrequest/ntp_request_interception/page_with_ntp_script.html
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/extensions/browser/api/extensions_api_client.cc
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/extensions/browser/api/extensions_api_client.h
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/extensions/browser/api/web_request/web_request_info.cc
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/extensions/browser/api/web_request/web_request_info.h
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/extensions/browser/api/web_request/web_request_permissions.cc
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/extensions/browser/api/web_request/web_request_permissions.h
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/extensions/browser/api/web_request/web_request_permissions_unittest.cc
[modify] https://crrev.com/5d00f36cfb22129d6d551eb570ce653edc0fa084/testing/buildbot/filters/mojo.fyi.network_browser_tests.filter


### ka...@chromium.org (2018-04-25)

treib@: It seems that there is no ResourceContext with a network service. See comment on https://chromium-review.googlesource.com/c/chromium/src/+/1018724. Given a render_process_id, is there another way to determine on the IO thread whether it corresponds to an instant renderer?

### tr...@chromium.org (2018-04-25)

I don't know of any other way to check for "is this an instant process", sorry - AFAIK there's InstantIOContext on the IO thread, and InstantService on the UI thread.

Generally, it looks like ResourceContext is deprecated, so probably InstantIOContext should be keyed off something else eventually?

### bu...@chromium.org (2018-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/53d030a18b1965c20878d6300738ed29c3bfdd08

commit 53d030a18b1965c20878d6300738ed29c3bfdd08
Author: Karandeep Bhatia <karandeepb@chromium.org>
Date: Fri Apr 27 23:29:33 2018

Network servicification: Plumb ResourceContext through WebRequestProxyingURLLoaderFactory.

This CL plumbs the ResourceContext to the WebRequestInfo structure through
WebRequestProxyingURLLoaderFactory. This is necessary to fix
NTPInterceptionWebRequestAPITest.NTPRendererRequestsHidden for the network
servicification path.

BUG=797461, 721414

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: I2957c1ece0f8f7b44f15156aeb5e554b3a91ff01
Reviewed-on: https://chromium-review.googlesource.com/1029549
Reviewed-by: Ken Rockot <rockot@chromium.org>
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#554556}
[modify] https://crrev.com/53d030a18b1965c20878d6300738ed29c3bfdd08/extensions/browser/api/web_request/web_request_api.cc
[modify] https://crrev.com/53d030a18b1965c20878d6300738ed29c3bfdd08/extensions/browser/api/web_request/web_request_info.cc
[modify] https://crrev.com/53d030a18b1965c20878d6300738ed29c3bfdd08/extensions/browser/api/web_request/web_request_info.h
[modify] https://crrev.com/53d030a18b1965c20878d6300738ed29c3bfdd08/extensions/browser/api/web_request/web_request_proxying_url_loader_factory.cc
[modify] https://crrev.com/53d030a18b1965c20878d6300738ed29c3bfdd08/extensions/browser/api/web_request/web_request_proxying_url_loader_factory.h
[modify] https://crrev.com/53d030a18b1965c20878d6300738ed29c3bfdd08/testing/buildbot/filters/mojo.fyi.network_browser_tests.filter


### bu...@chromium.org (2018-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5d11c9e146eeba027517ac40816839d0f1bc5416

commit 5d11c9e146eeba027517ac40816839d0f1bc5416
Author: Karandeep Bhatia <karandeepb@chromium.org>
Date: Sat Apr 28 06:07:03 2018

Extensions: Hide OneGoogleBar requests from extensions.

LocalNtpSource serves resources for the local New Tab page. It makes browser
requests to fetch one google bar data over the network. This is then served to
the local NTP renderer.

Currently, extensions can intercept these requests using the Web Request API.
However, this is not desired as the NTP is a semi-privileged process. Hide these
requests from extensions.

BUG=797461

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: Ic8bb3268ba37ec859237f6805bba9a96cae6d464
Reviewed-on: https://chromium-review.googlesource.com/1026996
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Marc Treib <treib@chromium.org>
Cr-Commit-Position: refs/heads/master@{#554631}
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/browser/extensions/api/chrome_extensions_api_client.cc
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/browser/extensions/api/chrome_extensions_api_client_unittest.cc
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/browser/extensions/api/web_request/web_request_apitest.cc
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/browser/search/one_google_bar/one_google_bar_fetcher.h
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/browser/search/one_google_bar/one_google_bar_fetcher_impl.cc
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/browser/search/one_google_bar/one_google_bar_fetcher_impl.h
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/browser/search/one_google_bar/one_google_bar_service_unittest.cc
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/browser/ui/search/local_ntp_one_google_bar_browsertest.cc
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/chrome/test/data/extensions/api_test/webrequest/ntp_request_interception/extension/background.js
[modify] https://crrev.com/5d11c9e146eeba027517ac40816839d0f1bc5416/testing/buildbot/filters/mojo.fyi.network_browser_tests.filter


### ka...@chromium.org (2018-05-01)

As far as the browser initiated NTP requests, the one google bar request should now be protected. Also turns out that service workers requests can't be redirected i.e. if an extension redirects a request for a service worker, it is treated as an invalid redirect. 

There are still some requests made on behalf of the NTP which could be manipulated by extensions (see c#38) but it seems to me that they need not be protected. And protecting individual requests for the NTP in this way seems a bit brittle. Maybe we should think of another solution long term.

This should be fixed now, I think.

### ka...@chromium.org (2018-05-01)

Also, since this was evaluated as Security_Severity-Low, this might not need a merge to 67. Will leave it to Release managers.

### sh...@chromium.org (2018-05-01)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-09)

Many thanks Rob, $500 for this one!

### aw...@chromium.org (2018-05-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-09-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### ni...@uwalumni.com (2019-08-08)

The Chrome release notes have a different (apparently incorrect) CVE id associated with this. https://chromereleases.googleblog.com/2018/07/stable-channel-update-for-desktop.html

### is...@google.com (2019-08-08)

This issue was migrated from crbug.com/chromium/797461?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>NewTabPage]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089982)*
