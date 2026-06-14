# Security: Headers are processed for aborted requests when passed through service worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40050173](https://issues.chromium.org/issues/40050173) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Network>FetchAPI, Blink>ServiceWorker |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bh...@jackhenry.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2019-09-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When a request is passed through a service worker, but is aborted before a response is received from the server, the browser processes response headers once the server returns a response.

The observed security case for this is when a user logs out while an authenticated request is in flight. The logout procedure involves aborting all in-progress requests and deleting the JWT authentication cookie. However, once the server returns a response, the `set-cookie` header--which updates the JWT cookie--is processed, essentially logging the user back in without their knowledge.

**VERSION**  

Chrome Version: 79.0.3909.0 (canary)  

Unaffected Chrome Version: 77.0.3865.90 (stable)  

Operating System: macOS 10.14.6 (18G95)

**REPRODUCTION CASE**  

<https://github.com/barronhagerman/chromium-sw-abort-fail>

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Barron Hagerman

## Timeline

### rs...@chromium.org (2019-09-19)

falken: Can you take a look? It looks like this may have changed recently since it does not affect stable.

[Monorail components: Blink>ServiceWorker]

### rs...@chromium.org (2019-09-19)

[Empty comment from Monorail migration]

### fa...@google.com (2019-09-19)

(won't be at a workstation until next week) It could help if someone can do a bisect.

### rs...@chromium.org (2019-09-19)

[Empty comment from Monorail migration]

### fa...@google.com (2019-09-20)

I heard via kinuko@ that the reporter reports that it might not a recent regression because similar behavior was observed on Stable, so a timing change might have just made the repro easier. So bisect may not be so useful.

### bh...@jackhenry.com (2019-09-20)

To clarify, I have been unable to reproduce this in Stable, but I was told of a situation on Stable (specifically 76.0.3809.132) where a user logged out and hit the back button to find out they were still logged in. This is the only issue I've observed that definitely causes that to happen, but I have not yet observed this particular behavior in Stable.

### bh...@jackhenry.com (2019-09-20)

I recant that comment.. with the repro case, the headers do not appear in the dev tools Network tab in 77.0.3865.90 (Stable), but the cookie is nevertheless re-created just like Canary.

### bh...@jackhenry.com (2019-09-20)

Cc: chad.killingsworth@banno.com

### sh...@chromium.org (2019-09-20)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ki...@chromium.org (2019-09-20)

Per #7 this seems to repro on Stable. Guessing that this might be related to (or same as) https://crbug.com/chromium/823697 (to be more specific, 823697#c6 seems to be saying the same thing). CC-ing ricea@ and yhirano@

### ki...@chromium.org (2019-09-20)

(chad.killingsworth@banno.com is the co-reporter)

### ck...@jackhenry.com (2019-09-21)

If preferred, we can make the GitHub repository with the repo code private.

### fa...@chromium.org (2019-09-26)

I'm now at a workstation. Looking.

[Monorail components: Blink>Network>FetchAPI]

### fa...@chromium.org (2019-09-26)

I'm not sure I'm able to reproduce this.

How do you see the cookie was recreated? After visiting the page and watching the 3 requests in the Network tab, and waiting some additional seconds, in DevTools -> Application -> Cookies, there are no cookies listed, and in the omnibox padlock icon -> Cookies, there is ""CookieCreatedAfterAbort" listed but with empty content and expiry date of the time of the reload, suggesting max-age: 0 was respected. When I reload the page, the cookie isn't sent according to the Request headers in the Network tab.

I tried copying the code to glitch at https://fetch-abort-fail-in-sw.glitch.me/ (https://glitch.com/edit/#!/fetch-abort-fail-in-sw) and also tried following the instructions on the GitHub repo.



### fa...@chromium.org (2019-09-26)

I'm not seeing this part so I'm probably failing to repro: "
"About 5000ms after the page is loaded, note that there are response headers listed for the aborted GET /delayedApiResponse request"

I'm on  79.0.3921.0. Would it be possible to host a repro on Glitch?

### fa...@chromium.org (2019-09-26)

Well this is interesting. I can repro on  79.0.3909.0  on https://fetch-abort-fail-in-sw.glitch.me/ as reported, but not  79.0.3921.0.

### fa...@chromium.org (2019-09-26)

There seems to be a timing issue. I can't repro on any Chromium build I've made, which will make this hard to debug. I'm also wondering if the service worker really matters here or if it's just tickling the timing.

Cookie committing seem to be done by URLRequestHttpJob (which I think runs in the network service?). I suspect when a request is aborted in Blink, we'll need to destroy the URLRequestHttpJob ASAP.  yhirano@ gave a pointer that this destruction happens by ResourceLoader/WebURLLoaderImpl  breaking the Mojo connection. 

In the good case where the cookie isn't recreated, the destruction appears to happen like this:

#2 0x7ff322f9f039 net::URLRequestHttpJob::Kill()
#3 0x7ff322f9622a net::URLRequest::DoCancel()
#4 0x7ff322f930df net::URLRequest::~URLRequest()
#5 0x7ff322f9350e net::URLRequest::~URLRequest()
#6 0x7ff31eea6233 network::URLLoader::~URLLoader()
#7 0x7ff31eea643e network::URLLoader::~URLLoader()
#8 0x7ff31ee23f7e network::cors::CorsURLLoaderFactory::DestroyURLLoader()
#9 0x7ff31eea5d10 network::URLLoader::NotifyCompleted()
#10 0x7ff32419f05f mojo::InterfaceEndpointClient::NotifyError()



### ck...@jackhenry.com (2019-09-26)

We've had a horrific time reliably reproducing this. I do have a live site that I can privately send creds to someone where it occurs pretty consistently.

It's definitely easier to reproduce with a service worker, but I can't say that's absolutely required. Whether the requests are aborted from script or by page navigation doesn't seem to matter.

### fa...@chromium.org (2019-09-27)

yhirano@: do you have ideas how to investigate this more?

It looks like in the good case the cancelling happens via:

#2 0x7f8548728c2d blink::ResourceLoader::ScheduleCancel()
#3 0x7f85486fb97c blink::Resource::DidRemoveClientOrObserver()
#4 0x7f85486fdcef blink::Resource::RemoveClient()
#5 0x7f8548705761 blink::ResourceClient::SetResource()
#6 0x7f854ad0dc89 blink::ThreadableLoader::DispatchDidFail()
#7 0x7f854ad0e1ca blink::ThreadableLoader::Cancel()
#8 0x7f854a5ef285 blink::FetchManager::Loader::Abort()

Which leads to:

#2 0x7f85505368de content::ResourceDispatcher::RemovePendingRequest()
#3 0x7f8550536b64 content::ResourceDispatcher::Cancel()
#4 0x7f855054164a content::WebURLLoaderImpl::Context::Cancel()
#5 0x7f8550546fee content::WebURLLoaderImpl::~WebURLLoaderImpl()
#6 0x7f85505470de content::WebURLLoaderImpl::~WebURLLoaderImpl()
#7 0x7f8548728f92 blink::ResourceLoader::HandleError()
#8 0x7f854872787f blink::ResourceLoader::Cancel()
#9 0x7f8548673829 blink::TimerBase::RunInternal()

Which clears the ThrottlingURLLoader which I assume breaks the Mojo connection and leads to the stack trace from https://crbug.com/chromium/1005948#c17:

#2 0x7ff322f9f039 net::URLRequestHttpJob::Kill()
#3 0x7ff322f9622a net::URLRequest::DoCancel()
#4 0x7ff322f930df net::URLRequest::~URLRequest()
#5 0x7ff322f9350e net::URLRequest::~URLRequest()
#6 0x7ff31eea6233 network::URLLoader::~URLLoader()
#7 0x7ff31eea643e network::URLLoader::~URLLoader()
#8 0x7ff31ee23f7e network::cors::CorsURLLoaderFactory::DestroyURLLoader()
#9 0x7ff31eea5d10 network::URLLoader::NotifyCompleted()
#10 0x7ff32419f05f mojo::InterfaceEndpointClient::NotifyError()

Now the question is what happens in the bad case that prevents this from happening within 2500 ms.

### fa...@google.com (2019-09-27)

Ideas from meeting (ricea, yhirano, kinuko, et al):
* Install an AdBlocker to try to repro on Chromium.
* Add trace events and repro on Chrome Canary with the traces.

### yh...@chromium.org (2019-09-27)

FYI there is a trace event for WebURLLoaderImpl::Cancel.

### fa...@chromium.org (2019-09-27)

barron.hagerman: To confirm, do you see this on canaries past 79.0.3909.0?

I can repro on 79.0.3909.0 but not recent canaries. One interesting point is a 79.0.3911.0 has a fix (cc/ cduvall, karandeepb):

    Speculative fix for WebRequest memory leak
    
    It seems the WebRequest is leaking InProgressRequest objects (see bug).
    We were not catching errors on the loader binding, which may have caused
    us to miss the errors.

https://chromium-review.googlesource.com/c/chromium/src/+/1772060

If this has to do with WebRequest API and not deleting loaders/URLRequestHttpJob, it's possible that fix is related. However, yhirano@ doesn't see how that fix would have affected AbortController() in terms of catching the Mojo connection error.

I tried installing an AdBlocker but it didn't help with the repro. I tried looking at trace events on 79.0.3909.0 and it looked like WebURLLoaderImpl::Context::Cancel() is entered even though the HttpJob didn't get killed (the event doesn't have URL info though). If I add additional trace events to the tree it won't help since I can't repro on recent canary.

### bh...@jackhenry.com (2019-09-27)

I can still consistently reproduce it on stable 77.0.3865.0 (incognito, no extensions enabled), but no longer in canary 79.0.3922.0 or 79.0.3925.0, so something appears to have fixed it between 79.0.3909.0 and 79.0.3922.0.

### fa...@chromium.org (2019-09-30)

Thanks! I found I can repro this by:
1) Reverting https://chromium-review.googlesource.com/c/chromium/src/+/1772060
2) Building Chromium
3) Installing AdBlock
4) Navigating to https://fetch-abort-fail-in-sw.glitch.me/

I think we can conclude https://chromium-review.googlesource.com/c/chromium/src/+/1772060 fixed this issue.

cduvall: Any thoughts on merge safety to 78?

It'd be nice to have a test, but I'm not sure what it'd be: install an web request api extension,  do a cancelled request, and wait for the URLRequestHttpJob to be killed?


### bh...@jackhenry.com (2019-09-30)

This should be testable without installing an extension; I ensured that this was an issue when no extensions were installed. The first aborted request is not affected because the service worker is not installed yet; only requests passed through the service worker appear to be affected. However, it does appear to be fixed in at least canary 79.0.3909.0.

### cd...@chromium.org (2019-09-30)

This should be safe to merge to 78, I'll request the merge on https://crbug.com/chromium/999681.

### cd...@chromium.org (2019-09-30)

Merged in 8e3335ca11840269bdcccc40e47188532bf73f29.

### yh...@chromium.org (2019-10-01)

> #25

There are built-in extensions which uses WebRequest API.

### fa...@chromium.org (2019-10-01)

Thanks all. Based on this discussion thread, closing this as fixed in 78 and 79.

### sh...@chromium.org (2019-10-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-09)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-10-09)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-01-07)

This issue was migrated from crbug.com/chromium/1005948?no_tracker_redirect=1

[Multiple monorail components: Blink>Network>FetchAPI, Blink>ServiceWorker]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050173)*
