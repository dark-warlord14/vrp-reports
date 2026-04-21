# Security: leak cross-site response size - countermeasure bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40053737](https://issues.chromium.org/issues/40053737) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>CacheStorage |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2020-10-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

In order to protect the Storage API from leaking the size of opaque cross-origin resources, random padding is added to the resources (as per <https://bugs.chromium.org/p/chromium/issues/detail?id=617963>)  

There were some other reports that leverage different mechanism to still leak the size: presence/absence of credentials (<https://bugs.chromium.org/p/chromium/issues/detail?id=1013906>), and request method (<https://bugs.chromium.org/p/chromium/issues/detail?id=1039882>).

The fix for the presence/absence of credentials (see here: <https://chromium.googlesource.com/chromium/src/+/64d2022359fed5668c631dda83cda2dfd7e956ce%5E%21/#F7>) was to add "CREDENTIALED" to the key if the request contained credentials. The fix can be easily bypassed:

1. cache /foo.png? where {"credentials": "include"} is set
2. get storage estimate (await navigator.storage.estimate())
3. cache /foo.png?CREDENTIALED where {"credentials": "omit"} is set
4. get storage estimate again
5. subtract the two estimates to get the difference of credentialed and non-credentialed (the latter is known by the attacker)

Alternatively, /foo.png and /foo.pngCREDENTIALED could be used (in order to force the latter to return a 404/bogus response).

The fix is very easy: just add a string after response\_url, before CREDENTIALED is added. In /storage/browser/quota/padding\_key.cc:  

std::string key = response\_url; → std::string key = response\_url + "SEPARATOR";

**VERSION**  

Chrome Version: 85.0.4183.121 stable  

Operating System: macOS

**REPRODUCTION CASE**  

A PoC is available here: <https://kul.tom.vg/chrome-storage-leak.html>; it will show the difference in size. Because the not-found resource is CORB'ed, the resulting size is 0, so the PoC will show the size of the response (35508 bytes - note that there's some static overhead).

**CREDIT INFORMATION**  

Reporter credit: Tom Van Goethem (@tomvangoethem) - mainly inspired by the report by Luan Herrera @ <https://bugs.chromium.org/p/chromium/issues/detail?id=1039882>

## Attachments

- [chrome-storage-leak.html](attachments/chrome-storage-leak.html) (text/plain, 1.1 KB)
- [chrome-storage-leak.patch](attachments/chrome-storage-leak.patch) (text/plain, 530 B)
- [chrome-storage-leak-post-body.html](attachments/chrome-storage-leak-post-body.html) (text/plain, 1.8 KB)

## Timeline

### wf...@chromium.org (2020-10-29)

Thanks for your report, and your suggested fix. I've looped the developers in to take a look at the issue.

[Monorail components: Blink>Storage>CacheStorage]

### to...@gmail.com (2020-10-29)

I've attached a patch with the fix.

I forgot to explain why the fix works: by always (i.e. not just conditionally) appending a static value to the string, you ensure that an attacker is unable to append the CREDENTIALED flag. For instance the key for /foo.pngCREDENTIALED that was sent without credentials becomes "/foo.pngCREDENTIALED_". The request for /foo.png that was sent with credentials become "/foo.png_CREDENTIALED". As such, the key of a non-credentialed response_url will always end with "_".

As an additional precaution, it might be worthwhile to verify whether it's not possible to send 2 different requests that map to the same response_url (e.g. if canonicalization happens for the response_url, but not for the URL sent in the request) -- I doubt that this is the case though.

### wa...@chromium.org (2020-10-30)

Thanks for the report.  Sorry I missed this in my previous fix here.

It seems we could also just always add something in the non-credentialed case.  For example,

  if (loaded_with_credentials)
    key += "CREDENTIALED";
  else
    key += "NOTCREDENTIALED";

Not sure if it would be clearer to do that or the separator that you suggest.

### to...@gmail.com (2020-10-30)

I just realized that there's another issue with the current implementation: for AppCache the loaded_with_credentials will always be false, as per https://source.chromium.org/chromium/chromium/src/+/master:content/browser/appcache/appcache_backfillers.cc;l=23;drc=87a63ed093790f8c2d1751e5a3914dfb03352d21;bpv=1;bpt=1
However, the request is sent with credentials. The key for AppCache is the same as the Cache API with {"credentials": "omit"}, assuming the latter is of known size, it's possible to determine the padding key and therefor the size of the resource.
Possible solution: set loaded_with_credentials to true for AppCache (I assume this accurately reflects what happens); alternatively, adding a APPCACHE flag if loaded with AppCache will also do the trick.

I think there might be another issue (although I haven't tested this yet): Content-Type is a CORS-whitelisted request header. With a POST request it's possible to vary between different content types and charsets (following the spec these are the allowed Content-Type “essences”: "application/x-www-form-urlencoded", "multipart/form-data", or "text/plain"); an attacker could forge requests such that one is valid and one is bogus (leading to a predictable response).

Now that I think of it; I don't think that the POST body is actually part of the key; this obviously leads to the same issue.

As it seems that there might be several ways to generate two different responses for the same padding key, wouldn't it be better to generate a (completely) random padding key for every new Response (and persist this value when adding it to the cache, such that it can be subtracted from the quota afterwards)?

### to...@gmail.com (2020-10-30)

PoC for a different POST body: https://kul.tom.vg/chrome-storage-leak-post-body.html (I just reflect the request body, but you get the idea... :))

### wa...@chromium.org (2020-10-30)

> As it seems that there might be several ways to generate two different responses for the same padding key, wouldn't it be better to generate a (completely) random padding key for every new Response (and persist this value when adding it to the cache, such that it can be subtracted from the quota afterwards)?

Doesn't this allow someone to make many requests and over time average out the padding?

I wonder if we could instead append the size of the response itself to the padding key.  This would create a stable padding for a particular response that cannot be averaged out, but would automatically change the padding for requests that result in different responses.  I guess it would still leave a small hole for different-but-same-length responses.

### to...@gmail.com (2020-10-30)

> Doesn't this allow someone to make many requests and over time average out the padding?

I think this is currently also possible, an attacker can simply add a random bogus parameter to the URL to get a different padding value.

> I wonder if we could instead append the size of the response itself to the padding key.

I think this still allows for certain attack scenarios: e.g. consider /search-mailbox 1) POST body: keyword=secret, 2) POST body: keyword=bogusnoresults. If keyword=secret has results the padding key will be different than with bogusnoresults, otherwise it will be the same. Perhaps more important: if part of the request body is reflected (or the attacker can in some other way vary responses over different response sizes), the attacker can still determine the exact size (up to the exact byte - because only at a specific byte you will get the same padding key)

### wa...@chromium.org (2020-10-30)

> I think this is currently also possible, an attacker can simply add a random bogus parameter to the URL to get a different padding value.

That's a good point.  Just brainstorming, but maybe when there are query params we could split our padding budget between search-vs-non-search parts of the URL and hash them separately.  Then varying the query param would only allow averaging out part of the padding.

For post body and other things, its sounds like we would need to hash as much of the request as possible.  (Or give up on the averaging protection and just do pure random as you suggest.)

### to...@gmail.com (2020-10-30)

I actually think that the padding was chosen in such a way that averaging padding values would be highly impractical/impossible, so that's (I believe) a non-issue. The main thing that needs to be ensured is that a new padding value can only be obtained by sending a request (=> several order of magnitude slower than placing it in the cache). If I remember correctly, there should be an internal Google document that describes/discusses this (I don't have access to it though).

I think that splitting the padding budget between search-vs-non-search parts of the URL would be disadvantageous in certain cases; e.g. /search/keyword vs /search?q=keyword.

Hashing the entire request (CORS-whitelisted headers + body) and using that as the padding key should do the trick indeed. Personally, I favour pure random though: there are no clear benefits to hashing the request; many parts of the request can be varied without affecting the response (and trying to guess which parts would affect the response seems to introduce its own issues), so effectively hashing the request doesn't provide any additional protection over pure random padding.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### jk...@chromium.org (2020-10-30)

Agree that the goal is force the attacker to send a network request to get a new padding value for the same resource. But if we give a random pad to every response then we violate that, so I don't understand your suggestion Tom. BTW: Good to hear from you again :)

The doc you're referring to is: https://docs.google.com/document/d/1LPUZwV0CtYBtFNGcceGX8VzJmLUf8NY1qWfJjCAjXks/edit#heading=h.aju8jnxy5fc3



### wa...@chromium.org (2020-10-30)

> But if we give a random pad to every response then we violate that

We can do this by stamping the padding on the Response object when its created in the fetch code.  Its then propagated down into cache_storage.  This is what firefox does, for example.

### jk...@chromium.org (2020-10-30)

Ah, so the intent isn't for every response, just for every response not served from the cache. But in that case, can't you tell when something new is put in the cache for the same url? E.g., a credentialed request would have a different response body, but use the same cache key. Unless vary=cookie is used, but does anyone actually use that? I guess another question is do people typically cache credentialed resources? Forgive me if I'm being daft, it's been awhile since I've thought about this stuff.

### wa...@chromium.org (2020-10-30)

Not sure I understand what you mean.  I think the idea is it would work like this:

 * fetch() associates a random padding with Response when it creates an opaque response
 * Response.clone() copies padding
 * cache_storage put() stores Response padding
 * cache_storage match() restores Response padding
 * service worker respondWith() propagates Response.padding

The padding only has to be generated in fetch() and then persisted/propagated with the Response from then on.

### jk...@chromium.org (2020-10-30)

What if the new fetch() response is served from the disk cache? We wouldn't want to give the response a new padding key since it didn't go to network. And where would we get that old padding key from?

### wa...@chromium.org (2020-10-30)

If we want a stable padding coming out of http cache then I guess the network stack would have to generate it (although not sure it knows that its going to be opaque or not) or provide a random id that's stable with the cache entry that can be used to generate the padding later.

### jk...@chromium.org (2020-10-30)

Generally the net/ layers tries to avoid non-http specific stuff. E.g., it's willfully ignorant of platform stuff like cache storage. So I don't think the cache would want to generate a pad per say, but it could generate a uuid or something to identify the resource. If we always use the UUID as the key to generate the pad then it might suffice.

Note that providing the UUID from the disk cache is a relatively heavy lift in that it requires versioning the various backend caches. Also not sure if the UUID would need to be stored in in-memory metadata or if it could be kept on disk. Would have to think about that.

### wa...@chromium.org (2020-10-30)

Josh, going to assign to you to think about the http cache implications for now.  I'm happy to do fetch/cache_storage updates, but not sure I am up to extensive changes to http cache.

### jk...@chromium.org (2020-10-30)

Unassigned as I have zero cycles for this right now. Must we do the cache option? Weren't there other options where we just include more in the padding key?

### jk...@chromium.org (2020-10-30)

+cc Maks in case he has thoughts on creating a per-resource unique identifier. I had considered md5sum but we wouldn't have that for results streaming from the network until it's too late.

### wa...@chromium.org (2020-10-30)

[Comment Deleted]

### jk...@chromium.org (2020-10-30)

I don't think that's a good option, as it allows the attacker to get lots of responses from the cache and not the network.

Hmm. What about URL + Response Time as the key. Response time is already provided by the network stack. The response time has microsecond resolution and is set when headers are received. So, a revalidation request would update the time. But at least the network is involved in the revalidation.



### jk...@chromium.org (2020-10-30)

The response time might be good enough on its own, not sure.

### to...@gmail.com (2020-10-30)

> The response time might be good enough on its own, not sure.

I wouldn't count on that. Responses can be forced to be sent in a single packet; probably TLS decryption would take more than 1µs though, but I don't know whether you want to rely on that.

Am I correct to assume that including the hash of the headers and including Response Time would be mutually exclusive? If there's a header that can be altered while still getting served from cache (i.e. that request header is not part of the cache key), it would again be possible to get many random observations from the cache, right? (Response Time would remain the same, but the request headers would change)

At the same time, not including the headers as part of the key is potentially problematic for non-cached responses, as server might interpret the requests differently...


### wf...@chromium.org (2020-10-30)

Triaging to Medium based on https://crbug.com/chromium/617963. This does need an owner though, so assigning to jkarlin for now.

### mo...@chromium.org (2020-10-30)

If you want UUIDs in HttpCache, I think you would want then in HttpResponseInfo rather than backend? With potentially some decisions to be made about the 304 header-update case? Hmm, we sort of don't know when the reply is the same, though; that's something of a domain knowledge thing, isn't it?

(I think I understand the attack class, but precise rules for when padding should change would require more thought)


### jk...@chromium.org (2020-10-30)

Oh right, HttpResponseInfo is what gets stored in the backend. Yes, we could add the UUID directly to that.  Silly me.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### wa...@chromium.org (2020-11-02)

Maybe I missed why response time doesn't work, but what about this:

1. If fetch sees a response that came from network, then stamp it with a random padding value.
2. If fetch sees a response that came from cache, then stamp it with a padding value that is a hash of the response time.

Then that padding is plumbed through cache_storage, service workers, etc.

### wa...@chromium.org (2020-11-02)

The uuid in http cache would be nice and would help other things like code cache, but maybe its orthogonal.  We use response time as the cache uuid for code caching today, so maybe we can do the same here.

### to...@gmail.com (2020-11-02)

> a padding value that is a hash of the response time

I think the potential danger here is that the response time might not be unique. If an attacker could get the same response timing for a resource of known size (e.g. by sending many other requests at the same time as the target request, and then checking for responses that arrived at the same time, e.g. using the Resource Timing API), they can figure out the padding size.

If the URL is also included in the padding key, it's probably fine (unless there can be multiple cache entries for the same URL - e.g. if the request headers would be part of the cache key - in that case hash(cache key) + response time would work as padding key).

### wa...@chromium.org (2020-11-02)

Hashing response time and url when a response comes from cache seems reasonable.  I believe our http cache only supports a single resource for a single url.

### wa...@google.com (2020-11-02)

[Empty comment from Monorail migration]

### wa...@chromium.org (2020-11-03)

Ok, so I will plan to do the following:

1. Make fetch()/appcache stamp a padding on the response:
  a. When coming from http cache it hashes url and timestamp.
  b. When coming from network it picks a purely random value.  (Or maybe we just use hashed url+timestamp always?)
2. store response padding in cache_storage response (not sure if appcache needs this, but appcache is also already default off except for reverse OT)
3. make service worker respondWith() propagate the padding
4. write tests

I expect to do this in M89 in Q4.

### to...@gmail.com (2020-11-03)

Under the assumption that the timestamp is not unique, I think we need a purely random value when it comes from the network. E.g. attacker could make various POST requests to the same URL with different request bodies, and pick the padding of the one with the same timestamp as the target request.

> I believe our http cache only supports a single resource for a single url.

The security of applying the padding relies on either this assumption, or the assumption that the timestamp is unique.

I'd be happy to help out where possible; unfortunately I'm not that familiar with the Chromium code base, but writing some tests should be doable. Just let me know!

### wa...@chromium.org (2020-11-03)

Josh, Maks, can you confirm we don't support multiple responses per URL in the http cache?  I believe we only support one at a time based on what I know of simple disk_cache and my recollection of our VARY support.

### mo...@chromium.org (2020-11-03)

Multiple response variants aren't supported, yes.

There may be multiple responses for URL in the sense that the cache key is different when the URL is used in different third-party contexts.
Hmm, that may be a problem if the attacker uses multiple domains to independently probe the same URL somehow, using 3P cache splitting to get independent probes?


### wa...@chromium.org (2020-11-03)

Do 3rd party iframes make it harder to get timestamp collisions?

### to...@gmail.com (2020-11-04)

If the padding key for cached resources is URL + response time + context (such that URL + context is always unique), it would still work (and there's still a network trip needed for every new padding value). I believe this would also still be fine regardless of timestamp collisions

### wa...@chromium.org (2020-11-04)

Including some kind of context key may be difficult.

### wa...@chromium.org (2020-11-04)

Actually, some kind of context id may be possible.  Fetch() should always have a context handy.  I'll have to see if we have an identifier on it somewhere.  Probably some kind of frame id.

### [Deleted User] (2020-11-21)

wanderview: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2020-11-23)

I'm still planning to work this in M89 timeframe.

### wa...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### wa...@chromium.org (2020-12-01)

[Comment Deleted]

### wa...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### wa...@chromium.org (2020-12-07)

Thinking about this more I don't think including a context ID in a hash is a good idea.  It would seem to allow an attacker to create N contexts that each fetch the resource from http cache and then average out the padding.

It seems the thing we want here is some hash data that only changes when you move to a different http cache.  Again, a cache key would be ideal, but in lieu of that I think we could use <url>+<response time>+<network isolation key>.

mmenke@, is there a convenient way to get the NIK in blink code given an ExecutionContext?

### mm...@chromium.org (2020-12-07)

NIKs are currently never provided to the renderer - we don't trust the renderer to supply them, so we never give it a chance to.  I think Shivani was looking at keying the blink cache on the NetworkIsolationKey, though, so might have thoughts on (or done some work on) plumbing it the blink?

### sh...@chromium.org (2020-12-07)

This is the document (internal) that talks about supplying the NIK to the renderer for partitioning the blink cache. I haven't yet started work on it because there are metrics being collected at the moment to see if instead of partitioning by NIK, can we just scope the blink cache to the document. But if we plan the former, it basically talks about RenderFrameHostImpl passing the NIK to the RenderFrameImpl::CommitNavigation via NavigationClient::CommitNavigation()
https://docs.google.com/document/d/1FptmjqcuWjhezn000FQOC_pZw6NtIIR1xmC2VLAuFcg/edit?usp=sharing

### wa...@chromium.org (2020-12-14)

FYI, I'm actively working on this now.  My WIP CL is here:

https://chromium-review.googlesource.com/c/chromium/src/+/2590076

Some notes:

1) I intend to perform padding computation in the renderer.  While we don't normally like to trust the renderer, it already has excessive power over storage.  For example, it could change the type of the response to be non-opaque, inspect opaque response data, or even store arbitrary data to cache_storage.  (If an origin is not ok with this, then they can use CORP to prevent the browser process sending their opaque responses to renderers.)
2) I think I will end up computing cached response padding by hashing <url>+<response time>+<context site>.  I am going to use <context site> instead of NIK at first since it should rule out most cases of sharing an http cache.  When NIK is available in the renderer we can follow-up and change the algorithm to use NIK.  I looked briefly at trying to construct a NIK, but it seems non-trivial for worker contexts.  I think this is ok since I think an attacker would need to get multiple top-level tabs open on on different sites with an embedded 3rd party iframe that they then coordinate across to achieve a timing attack.

Let me know if there any concerns with that plan.

### wa...@chromium.org (2020-12-14)

[Empty comment from Monorail migration]

### to...@gmail.com (2020-12-17)

Perhaps it makes sense to also include whether the request was authenticated? Just to prevent that the attacker simultaneously requests the same url twice, once with and once without credentials? I presume that the same context site would be used for both requests? The requests will be over 2 different connections, so I don't know the likelihood of the responses arriving at the same time though. Padding key would then be the hash of the following: <url>+<response time>+<context site>+<authenticated>

Does <context site> refer to the including or the top-level document? I'm not sure I understand how an attacker would pull off the attack even with multiple top-level tabs open, wouldn't each tab have a different cache partition?

### wa...@chromium.org (2020-12-17)

Well, I thought it would be easier to get a timing collision with separate cache partitions.  To do it in a single http cache partition you would have to store response 1, read read response 1, and then store response 2 all within the same microsecond which seems unlikely.  It seems hard to get both a timing collision and reads from the same http cache partition for two responses with the same URL.

In regard to "simultaneously requests the same url twice, once with and once without credentials", in theory at least one of these would be coming from network and not the http cache.  In that case it would get a purely random padding.

### to...@gmail.com (2020-12-17)

Ohh, I missed the bit that when it comes over the network it gets a random padding; makes sense now.

If/when triple-keyed cache partitioning lands, the attack would probably be easier to pull off I guess? Or well, it will at least no longer require two colluding top-level documents on different origins any more.

### wa...@chromium.org (2021-01-07)

I think triple-keyed cache is the scenario I described above where you could collude with two different top-level documents to get separate http caches.  (Triple-key here means top level, frame site, and resource URL.)  Or are you thinking of a different scenario?

### wa...@chromium.org (2021-01-11)

Note, each renderer/browser process will have its own key for hashing url+response_time+site for responses coming out of http cache.  This means contexts that are in two different renderer processes may result in different padding values for the same response.  I think this is ok, though, because:

1. The difference between the padding value will not be known and therefore I don't think can be used to strip the padding away.
2. Each process will have a stable key, so it does not lend itself to a scalable averaging attack.  You would need a large number of processes (i.e. tabs) which will run into browser limitations.

Does that sound right to other folks?

If those don't hold I may need to plumb some kind of shared key between the processes which will be quite a bit harder.

### wa...@chromium.org (2021-01-11)

Also, I don't think it will be necessary to reset keys on storage wipe any more.  We will be computing padding based on response time in the cache.  If the cache is wiped, then the paddings will also get recomputed with a new value automatically.

### wa...@chromium.org (2021-01-13)

I've run into another problem.

The cache_storage subsystem can store a blob of data on the side for a response.  This is typically used to store the byte cache for a javascript resource.  Today we take into account the existence of this side data when computing a hash.  So a resource with side data will have different padding from the same resource without side data.  Presumably this is to avoid allowing sites to detect the size of the side data stored for the opaque response.

So we likely need to recompute a padding for responses once they get side data added.  There just seem to be some risks associated with this.  Consider:

1. We could always use a random padding when side data is added.  This would risk an averaging attack since a site could create N clones of a response and add them each in an install event getting side data immediately.  Depending on the side of the js it might be fast enough to average out the padding.
2. We could always use a hashed padding when side data is added.  This would risk the origin problem here of stripping the padding out.  A site could arrange two script responses with the same url+time+site, but that differ in some known way.  Once side data is applied the padding is deterministic and could be stripped off.
3. We could try using our full heuristic of choosing random-vs-hashed based on the source of the response.  This still risks the clone averaging attack in (1), though.

So I think I will have to go with:

4. Instead of replacing the existing padding for a response when side data is added we should instead add additional padding.  This padding would be a hash of url+time+site+side-data-size. This will make opaque js scripts take up another 7MB of quota on average.

I suppose we could use the hash of url+time+site+side-data-size in (2), but it would still risk that the main resource changes without changing the code cache.  This is not a normal steady state condition, but could happen.

Thoughts?

### wa...@chromium.org (2021-01-13)

Josh, Chris, do recall the source of why we recompute hash on the existence of side data in cache_storage?  Is it just to obscure the size of the code cache?  Do you have any thoughts on https://crbug.com/chromium/1143526#c60?

### jk...@chromium.org (2021-01-13)

I believe it was to obscure the size of the code cache, yes.

I also agree with your conclusion in #60, frustrating as that is to double the virtual size of scripts.

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-01-21)

Tom, do you see any reason to pad opaqueredirect responses?

https://fetch.spec.whatwg.org/#concept-filtered-response-opaque-redirect

These are responses with a redirect status code where the redirect mode was "manual" so the browser does not automatically follow the redirect.  Generally redirects will not have a body at all.

I don't believe firefox pads opaqueredirect responses, but current chrome cache_storage does.  I'm wondering if I need to maintain that.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cfb13d64c50764479e9c17c2efa718bac93809ac

commit cfb13d64c50764479e9c17c2efa718bac93809ac
Author: Ben Kelly <wanderview@chromium.org>
Date: Thu Jan 21 17:29:38 2021

CacheStorage: Factor writing entry metadata into separate method.

This CL factors out the code to write an entry's metadata into its own
method.  This is in preparation for a later CL that will need to rewrite
the metadata with an updated value.

Bug: 1143526
Change-Id: I887bbd5f631e41c19c1e863c04d531764de807c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2634124
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#845689}

[modify] https://crrev.com/cfb13d64c50764479e9c17c2efa718bac93809ac/content/browser/cache_storage/legacy/legacy_cache_storage_cache.cc
[modify] https://crrev.com/cfb13d64c50764479e9c17c2efa718bac93809ac/content/browser/cache_storage/legacy/legacy_cache_storage_cache.h


### to...@gmail.com (2021-01-22)

> Generally redirects will not have a body at all.

But the headers would still be stored? I presume that these are also included in the quota? In that case I think it's probably useful to pad it: e.g. attacker could determine length of redirected URL, or length of Set-Cookie headers etc.

### wa...@chromium.org (2021-01-22)

The location header would be present, but set-cookie headers are not present on these responses.  Its stripped prior to the response being exposed to content or cache_storage.

Also keep in mind opaqueredirects are generated even for same-origin or cors requests when you use a manual redirect mode.  Its not something restricted to no-cors requests.  I'm hesitant to impose a 7MB quota penalty for every opaqueredirect whether its same-origin, cors, etc.

That being said, I guess the safest thing to do would be to add the padding to opaqueredirect responses for now.  If it becomes onerous for folks we can try to carve out an exception for responses that are produced for same-origin or cors requests, but that would require additional plumbing.  Or maybe the amount of padding on opaqueredirects could be reduced if we are only trying to hide the size of a location header.

### wa...@chromium.org (2021-01-22)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-01-22)

I also filed a spec issue to ask if we could just open up same-origin/cors redirects:

https://github.com/whatwg/fetch/issues/1145

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5a9eb6c35e2830b3e515d211bedfd9e8a92fab78

commit 5a9eb6c35e2830b3e515d211bedfd9e8a92fab78
Author: Ben Kelly <wanderview@chromium.org>
Date: Tue Jan 26 19:26:06 2021

CacheStorage: Make LegacyCacheStorage::SizeImpl respect padding.

Previously LegacyCacheStorage::SizeImpl() would include the full padded
size of a Cache object, but it would not detect if the padding had been
invalidated for some reason.  In addition, it did not properly propagate
the size information to doomed caches.  This CL corrects those issues.

Note, this CL does not contain a test.  A follow-up CL that performs
a padding migration will include a test that exercises this path.  For
now this CL has been manually tested and verified.  This CL was split
out from the migration CL in an attempt to reduce CL size and make them
easier to understand.

Bug: 1143526
Change-Id: I049adbe4a5cc931dc079f330ffa27f9212eb2fa7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2648212
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/master@{#847262}

[modify] https://crrev.com/5a9eb6c35e2830b3e515d211bedfd9e8a92fab78/content/browser/cache_storage/legacy/legacy_cache_storage.cc
[modify] https://crrev.com/5a9eb6c35e2830b3e515d211bedfd9e8a92fab78/content/browser/cache_storage/legacy/legacy_cache_storage_cache.h


### wa...@chromium.org (2021-01-27)

While working on tests I realized we still need to include the request method in the hash when reading from http cache.  By specifying a method of HEAD instead of GET you can keep url+time+site constant, but change the size of the returned response.  This would allow stripping padding in these cases.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/386e9576e6c3846127a1780e82c9b12cc2d8b879

commit 386e9576e6c3846127a1780e82c9b12cc2d8b879
Author: Ben Kelly <wanderview@chromium.org>
Date: Tue Feb 02 15:45:09 2021

CacheStorage: Refactor opaque padding.

This CL refactors how we generate and store opaque response padding:

* Padding values are now generated immediately in fetch().
* Padding values are associated with the Response and follow it.
* Network loaded responses get a purely random pad.
* Http cache loaded responses get a hashed padding value.
* CacheStorage now stores padding values in each entry.
* CacheStorage entries with side data for code cache have a separate,
  additional padding value added.
* Many additional tests.

Bug: 1143526
Change-Id: I40b094097b64be7bab8899acad8b9baffe304d33
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2590076
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/master@{#849608}

[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/web_tests/wpt_internal/cache_storage/resources/padding-fetch-sw.js
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/web_tests/wpt_internal/cache_storage/resources/simple.js.headers
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/web_tests/wpt_internal/cache_storage/padding.https.html
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/appcache/appcache_update_job.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/platform/loader/fetch/resource_response.h
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/cache_storage/legacy/legacy_cache_storage.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/cache_storage/cache_storage_histogram_utils.h
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/core/fetch/fetch_response_data.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/core/BUILD.gn
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/web_tests/wpt_internal/cache_storage/resources/simple.js
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/appcache/appcache_database.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/storage/browser/BUILD.gn
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/cache_storage/cache_storage_manager_unittest.cc
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/test/data/cache_storage/padding_v2/0430f1a484a0ea6d8de562488c5fbeec0111d16f/index.txt
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/platform/exported/web_url_response.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/common/service_worker/service_worker_loader_helpers.cc
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/test/data/cache_storage/padding_v2/0430f1a484a0ea6d8de562488c5fbeec0111d16f/676288ed-4de0-44af-97d6-dbd75b07a8a3/4bfb34f348c2269e_0
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/renderer/loader/web_url_loader_impl.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/core/fetch/fetch_response_data.h
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/services/network/public/mojom/url_response_head.mojom
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/public/mojom/fetch/fetch_api_response.mojom
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/core/fetch/response.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/appcache/appcache_backfillers.cc
[rename] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/storage/common/quota/padding_key.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/public/platform/web_url_response.h
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/core/fetch/DEPS
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/test/data/cache_storage/padding_v2/0430f1a484a0ea6d8de562488c5fbeec0111d16f/676288ed-4de0-44af-97d6-dbd75b07a8a3/index-dir/the-real-index
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/cache_storage/legacy/legacy_cache_storage_cache.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/common/background_fetch/background_fetch_types.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/modules/service_worker/fetch_event.cc
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/storage/common/BUILD.gn
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/tools/blinkpy/presubmit/audit_non_blink_usage.py
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/cache_storage/legacy/legacy_cache_storage_cache.h
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/renderer/core/fetch/fetch_manager.cc
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/test/data/cache_storage/padding_v2/0430f1a484a0ea6d8de562488c5fbeec0111d16f/676288ed-4de0-44af-97d6-dbd75b07a8a3/index
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/storage/common/quota/padding_key.h
[add] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/third_party/blink/web_tests/wpt_internal/cache_storage/resources/padding-install-sw.js
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/cache_storage/cache_storage.proto
[delete] https://crrev.com/930ad387d39ac6fc89a4a65df098a1b9000b4989/storage/browser/quota/padding_key.h
[delete] https://crrev.com/930ad387d39ac6fc89a4a65df098a1b9000b4989/third_party/blink/web_tests/http/tests/cachestorage/padding.html
[modify] https://crrev.com/386e9576e6c3846127a1780e82c9b12cc2d8b879/content/browser/cache_storage/cache_storage_cache_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4c5180fbaa633477e782152b4aa7b6030880a427

commit 4c5180fbaa633477e782152b4aa7b6030880a427
Author: Ben Kelly <wanderview@chromium.org>
Date: Wed Feb 03 16:14:22 2021

CacheStorage: Remove padding key management code.

After the padding refactor in the previous CL we no longer need to
manage separate padding keys.  This CL removes this key management code.

Bug: 1143526
Change-Id: I0fee6ea7a6c4672e80032569b6b46a90496f4749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2658741
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/master@{#850134}

[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/content/browser/cache_storage/cache_storage_index.h
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/content/browser/cache_storage/legacy/legacy_cache_storage_cache.cc
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/content/browser/cache_storage/legacy/legacy_cache_storage_cache.h
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/content/browser/cache_storage/cache_storage_index_unittest.cc
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/content/browser/cache_storage/legacy/legacy_cache_storage.cc
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/content/browser/cache_storage/cache_storage.proto
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/storage/common/quota/padding_key.cc
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/content/browser/cache_storage/cache_storage_index.cc
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/content/browser/cache_storage/cache_storage_cache_unittest.cc
[modify] https://crrev.com/4c5180fbaa633477e782152b4aa7b6030880a427/storage/common/quota/padding_key.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d2f4f98e2e0927788115cf581a39a6874c020721

commit d2f4f98e2e0927788115cf581a39a6874c020721
Author: Ben Kelly <wanderview@chromium.org>
Date: Thu Feb 04 14:04:31 2021

Fetch: Remove Response loaded_with_credentials.

Since the opaque padding refactor in crrev.com/c/2590076 the fetch
response loaded_with_credentials attribute has been unused.  This CL
removes the stale code.

Bug: 1143526
Change-Id: I1d7ee1e546d29d180767ac9dd915185a343e8497
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2667468
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/master@{#850570}

[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/content/common/background_fetch/background_fetch_types.cc
[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/third_party/blink/renderer/core/fetch/response.cc
[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/content/browser/cache_storage/legacy/legacy_cache_storage_cache.cc
[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/content/browser/cache_storage/cache_storage_manager_unittest.cc
[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/content/browser/cache_storage/cache_storage.proto
[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/third_party/blink/renderer/core/fetch/fetch_response_data.cc
[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/third_party/blink/renderer/core/fetch/fetch_response_data.h
[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/third_party/blink/public/mojom/fetch/fetch_api_response.mojom
[modify] https://crrev.com/d2f4f98e2e0927788115cf581a39a6874c020721/content/browser/cache_storage/cache_storage_cache_unittest.cc


### aj...@google.com (2021-02-17)

Hi security marshal here - if the CLs above solve the issue could you mark the bug as Fixed - this will kick off our merging processes? (If not, ignore me)


### wa...@chromium.org (2021-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-25)

Congratulations, Tom! The VRP Panel has decided to reward you $3,000 for this report. Thank you for your efforts and engagement on this issue!

### ad...@google.com (2021-02-26)

wanderview@ your change in https://crbug.com/chromium/1143526#c68 has overridden Sheriffbot's normal policy, which would be to request merge for this severity of bug back to M89. Is it intentional that you don't feel it's appropriate to merge this back to M89? If not, please change M to M-89 and add Merge-Request-89. Thanks!

### wa...@chromium.org (2021-02-26)

Sorry, I was not aware of that.  I'm not really comfortable merging back the giant CL in https://crbug.com/chromium/1143526#c72 (and other pre-requisites).  Since this was marked as only medium I thought that was ok.  What do you think?

### am...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-10)

Hi wanderview@, re https://crbug.com/chromium/1143526#c82, that's fine, I just wanted to make sure it was intentional and you hadn't fallen victim to the sinister emergent behavior of our bot swarm.

### [Deleted User] (2021-03-12)

Not requesting merge to beta (M90) because latest trunk commit (850570) appears to be prior to beta branch point (857950). If this is incorrect, please replace the Merge-na label with Merge-Request-90. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ja...@google.com (2021-04-16)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-05-26)

This issue was migrated from crbug.com/chromium/1143526?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1150548]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053737)*
