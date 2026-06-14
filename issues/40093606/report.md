# Security: Cross origin resource size infoleak

| Field | Value |
|-------|-------|
| **Issue ID** | [40093606](https://issues.chromium.org/issues/40093606) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2018-12-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to leak cross-origin resources exact size using appcache + storage estimator.

To exploit it it is enough to have entry in cache manifest file for this cross origin resource and then receive size using storage size estimator. If some more bytes are added to these resource then returned size by storage estimator has difference by this value.

This attack doesn't work for cache API (I think some randomization of size is added to prevent from this attack)

More over it works for resources which should by protected by CORB.  

I have tested it on resource which I was not able to load by Cache API because of CORB.

This vuln is pretty usefull when exploit xs-search bugs like this <https://medium.com/@luanherrera/xs-searching-googles-bug-tracker-to-find-out-vulnerable-source-code-50d8135b7549>  

It is much easier with this appcache + estimator method, because it is possible to detected even single byte difference in response and this is reliable and don't require hard to perform timing side channels.

**VERSION**  

Chrome Version: Tested on: 68.0.3440.106,70.0.3538.77,71.0.3578.30  

Operating System: Linux

**REPRODUCTION CASE**  

PoC: <https://poc-size-leak.adami.pl/exploit-leak-size.html> (This has in example resource which should be protected by CORB)

**CREDIT INFORMATION**  

Reporter credit: Adam Iwaniuk [adamiwaniuk@gmail.com](mailto:adamiwaniuk@gmail.com)

## Attachments

- [attack.py](attachments/attack.py) (text/plain, 313 B)
- [index.html](attachments/index.html) (text/plain, 776 B)

## Timeline

### mp...@google.com (2018-12-30)

Very cool, reproduces perfectly. Assigning to the appcache owners, setting to severity medium, and adding mkwst@ and tsepez@ for some OWP input.

[Monorail components: Blink>Storage>AppCache]

### sh...@chromium.org (2018-12-31)

[Empty comment from Monorail migration]

### ev...@google.com (2019-01-02)

Attaching code for this attack, and adding jkarlin@. This is the same as https://github.com/whatwg/storage/issues/31 and crbug.com/617963 so we should be using the same padding here that we use there, and we probably should even use the same key (so you can't get two measurements by querying AppCache + Cache APIs separately).

A side comment.. the Storage spec says: https://storage.spec.whatwg.org/#usage-and-quota "This cannot be an exact amount as user agents might, and are encouraged to, use deduplication, compression, and other techniques that obscure exactly how much bytes an origin uses.". Ignoring the compression comment (I suspect that using compression in any form would be a vulnerability by itself because of CRIME/BREACH), it seems like we should just move the code from https://cs.chromium.org/chromium/src/content/browser/cache_storage/cache_storage_cache.cc to some common class that appcache and cache api share?

Also, in case it's useful for figuring out priority, since we received crbug.com/617963 we have been doing some research and we found out that this is worse for Google services than we thought when I originally filed that bug. We now know you can figure out where and when users have and will travel and live (or taken pictures with), who they communicate with, when and about what (email or chat), who they will meet and when (calendar events). Outside Google you can find out which movies users watched on Netflix, who are your friends on Facebook and Twitter.


### ev...@google.com (2019-01-02)

Just found this: crbug.com/910210 seems like it was fixed on https://chromium-review.googlesource.com/c/1359333

### ev...@google.com (2019-01-02)

Also relevant: https://bugs.chromium.org/p/chromium/issues/detail?id=582750#c12

### pw...@chromium.org (2019-01-11)

+mek@, who is helping out with AppCache bugs
+wanderview@, who is helping migrate Google properties to Service Workers
+palmer@, because we've discussed security issues as a reason to deprecate Web features

We've deprecated & removed AppCache from insecure origins on security grounds. We should assess how easy it would be to implement padding using the same algorithm as for Cache Storage. If it requires anywhere near the same amount of effort as it did for Cache Storage, I think we should just pull the plug on AppCache instead.

### pw...@chromium.org (2019-01-12)

+awhalley@ for timing.

adamiwaniuk@ - Thank you very much for the report! When are you planning to disclose this bug? Do we get 90 days from the date we acknowledged it?

### ad...@gmail.com (2019-01-12)

You have as much time as you want. This is just blocking releasing my writeup for filemanager 35c3 ctf challenge (I have found this bug while solving it and I managed to successfully solve it using this). I will not release it until this ticket will be unrestricted.

### js...@chromium.org (2019-01-15)

[Empty comment from Monorail migration]

### pw...@chromium.org (2019-01-25)

mek@ will be working on the system-level design. staphany@ will be implementing the fix.

### st...@chromium.org (2019-01-25)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-01-31)

+lukasza@, +creis@ to take a look at the CORB side of this, since this seems to affect resources which should be protected by CORB. 

### lu...@chromium.org (2019-01-31)

Thank you very much for the report and for CC-ing me on the bug!


I see that the original report applies to Chrome 71.0.3578.30.  I am actually a little bit surprised that this affects CORB (especially if it happens with --enable-features=NetworkService which AFAIK tries to ship to the stable channel in M72 [at least on some platforms]).  I hope that the following fixes would make this attack useless for Cross-Origin-Read-Blocking/CORB (or Cross-Origin-Resource-Policy) protected resources:

- r613774 which applies CORB to requests "proxied" by AppCache (see https://crbug.com/chromium/910210).  Commit 0d9f17b8... initially landed in 73.0.3631.0 and was merged (f05b630e1e3368ecb3c0933bbb60056ea0ca8f77) into 72.0.3626.9

- r624685 which verifies |request_initiator| in requests "proxied" by AppCache (see https://crbug.com/chromium/910287).  Commit 1b43ef78... initially landed in 73.0.3680.0


FWIW, the PoC from the original report doesn't seem to work in 73.0.3679.0 (i.e. the PoC says "leaked size: -12714" when I think it should report size of 1337).  OTOH, I am not sure if I understand all the moving pieces here + my experiments below show that indeed some AppCache requests are still done without CORB being enabled (and not sure if their |request_initiator| is verified):

- The fixes (the ones mentioned in the other paragraph above) assume that all requests that might need to be protected by CORB will be initiated by AppCacheSubresourceURLFactory.  I guess this might not be true for requests that aren't trigerred by the webpage - i.e. maybe the AppCache manifest triggers a *separate* URLLoaderFactory to fill the cache?

- The "old" CrossSiteDocumentBlockingTest.AppCache test doesn't cover the scenario where the "victim" subresource is covered by the AppCache manifest (I missed the fact that non-relative, cross-origin URLs are allowed in the AppCache manifest... who would have thought... :-/).  I've tried adding a test that checks what happens when a cross-origin URL is present in the AppCache manifest - results below.


The main feature of the new test is an AppCache manifest that says:

    CACHE MANIFEST
    http://some.other.origin.com/site_isolation/nosniff.json
    
    NETWORK:
    *

And it seems that the request for this cross-origin resource is indeed done without CORB:

    $ test.sh out/rel/content_browsertests \
        --gtest_filter=WithoutOut*CrossSiteDocumentBlockingTest.AppCache_CoveredResource* \
        --enable-features=NetworkService
    ...
    [17785:17828:0131/085116.854646:ERROR:url_loader.cc(354)] URLLoader::ctor;
        request.url = http://some.other.origin.com/site_isolation/nosniff.json;
        request.request_initiator = http://127.0.0.1:46869;
        factory_params_->process_id = 0;
        factory_params_->is_corb_enabled = 0



[Monorail components: Internals>Sandbox>SiteIsolation]

### aw...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### ad...@gmail.com (2019-01-31)

For me it works on Version 73.0.3679.0 (Official Build) dev (64-bit) on ubuntu 18.04 for CORB protected resources.

The PoC was tuned for one version of chrome (value from size estimator is decreased by magic value). So to verify if it works best test is:
1. check what is calculated value
2. setup size to value +1 or +10
3. check if new calculated value is changed by the same difference



### me...@chromium.org (2019-01-31)

I'm not sure what CORB has to do with this at all? I didn't think CORB was supposed to block resources from ending up in the AppCache cache itself. I.e. my understanding of CORB is that it stops the body of certain cross origin resources from ending up in the renderer, but that is completely orthogonal to what ends up being cached in appcache. Anything that ends up in the renderer, wether from the network or from the cache I'd expect to still have CORB protections.

The deal with this bug is that via quota we can determine the size of cross origin resources. So our proposed/planned fix here is to do the same as CacheStorage does, and add random and large padding (for quota purposes) to any opaque cached responses (except that since AppCache doesn't do CORS at all in this case we'll probably do this for all cross-origin resources, not just for opaque ones).

So am I misunderstanding what CORB is supposed to protect against?

### lu...@chromium.org (2019-01-31)

RE: https://crbug.com/chromium/918293#c16:

AFAIK, in the NetworkService world, CORB is *not* applied to AppCacheSubresourceURLFactory->renderer hop.  It is only applied to the NetworkService->AppCacheSubresourceURLFactory hop (for requests falling back to the network) - after r613774 AppCacheSubresourceURLFactory::CreateURLLoaderFactory uses GetNetworkFactoryWithCORBEnabled.  Therefore, I am not sure why this bug only talks about leaking content size - I assume that the whole response body would be visible to a compromised renderer (which may ignore "opaqueness" of the responses).

Applying CORB to cached-AppCache-responses -> renderer hop does seem like one to way to fix this bug.  It would require similar hooks as the ones present between network::URLLoader and network::CrossOriginReadBlocking (or between content::CrossSiteDocumentResourceHandler and network::CrossOriginReadBlocking).  The biggest required change seems to be in having to postpone returning anything to the renderer in SubresourceLoader::OnReceiveResponse (in anonymous namespace in appcache_subresource_url_factory.cc) and first letting CORB sniff the response body.

OTOH, maybe applying CORB to NetworkService -> AppCache hop might be easier to implement (it seems to just require starting using CORB-enabled factory - see how this is done by AppCacheSubresourceURLFactory::CreateURLLoaderFactory via GetNetworkFactoryWithCORBEnabled).  OTOH, maybe I miss some reasons why this alternative is incorrect or undesirable (for example, I assume that AppCache only applies to no-cors requests that are associated with a manifest from a single origin).

WDYT?

### me...@chromium.org (2019-01-31)

Yeah, it does sound like there is a separate but unrelated issue with how CORB is applied (or not applied) to appcache cached resources, but that still seems completely orthogonal to this issue? I.e. this issue is about cross origin information leaks in cases where CORB doesn't apply as well (i.e. valid cross origin images that end up being loaded in image tags; but where we still don't want uncompromised renderers to know much about the image).

So yes, it probably makes sense to file a separate issue for the CORB related issues (if there are in fact any, and it does sound like there might be). Not sure what information CORB would need to make its decisions, so not sure if that is something that can be done before resources are cached (which is a completely browser process side thing), or if it needs to be implemented when resources are served out of appcache. But either way, figuring out those details is probably better done on a separate bug, to not get even more off-topic on this one.

### lu...@chromium.org (2019-01-31)

You're right - CORB aspect does seem like a separate issue (separate from this issue which 1) applies also to non-CORB-protected responses + 2) only deals with timing).  I've opened https://crbug.com/chromium/927471 for the general CORB problem.

### pw...@chromium.org (2019-02-05)

[Empty comment from Monorail migration]

### pw...@chromium.org (2019-02-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

staphany: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-02-23)

staphany: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2019-02-25)

staphany@ is currently implementing the fix for this issue.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2b3ea54e6ea199052afe0ba2f29271b67ab3ae78

commit 2b3ea54e6ea199052afe0ba2f29271b67ab3ae78
Author: Staphany Park <staphany@chromium.org>
Date: Fri Mar 01 00:33:04 2019

CacheStorage: Extract padding key logic.

AppCache will also need to share the same key used to pad CacheStorage.

This CL also updates the singleton key's implementation from
base::LazyInstance to base::NoDestructor.

Bug: 918293
Change-Id: I792d700a445dc1bfa408564401288e6bd56918b2
Reviewed-on: https://chromium-review.googlesource.com/c/1490951
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: David Benjamin <davidben@chromium.org>
Commit-Queue: Staphany Park <staphany@chromium.org>
Cr-Commit-Position: refs/heads/master@{#636624}
[modify] https://crrev.com/2b3ea54e6ea199052afe0ba2f29271b67ab3ae78/content/browser/cache_storage/cache_storage.cc
[modify] https://crrev.com/2b3ea54e6ea199052afe0ba2f29271b67ab3ae78/content/browser/cache_storage/cache_storage_manager_unittest.cc
[modify] https://crrev.com/2b3ea54e6ea199052afe0ba2f29271b67ab3ae78/storage/DEPS
[modify] https://crrev.com/2b3ea54e6ea199052afe0ba2f29271b67ab3ae78/storage/browser/BUILD.gn
[add] https://crrev.com/2b3ea54e6ea199052afe0ba2f29271b67ab3ae78/storage/browser/quota/padding_key.cc
[add] https://crrev.com/2b3ea54e6ea199052afe0ba2f29271b67ab3ae78/storage/browser/quota/padding_key.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0e1ea5222d4a0d73c9ca0c68bc36c01141721f0a

commit 0e1ea5222d4a0d73c9ca0c68bc36c01141721f0a
Author: Staphany Park <staphany@chromium.org>
Date: Fri Mar 08 18:09:31 2019

AppCache: Avoid recalculating cache size.

Bug: 918293
Change-Id: Ifae56b8dbb81669ae81f70c12e2ef5920f737e6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1510076
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Staphany Park <staphany@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#639069}
[modify] https://crrev.com/0e1ea5222d4a0d73c9ca0c68bc36c01141721f0a/content/browser/appcache/appcache.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/66eac028ac9538ef57bc6f1874a9249ed6310cf5

commit 66eac028ac9538ef57bc6f1874a9249ed6310cf5
Author: Staphany Park <staphany@chromium.org>
Date: Tue Mar 26 21:37:55 2019

CacheStorage: Extract padding calculation logic.

Bug: 918293
Change-Id: I8e8a7e9e5ead7eca1c6712d8464ae1d63049b96c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1538977
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Staphany Park <staphany@chromium.org>
Cr-Commit-Position: refs/heads/master@{#644532}
[modify] https://crrev.com/66eac028ac9538ef57bc6f1874a9249ed6310cf5/content/browser/cache_storage/cache_storage_cache.cc
[modify] https://crrev.com/66eac028ac9538ef57bc6f1874a9249ed6310cf5/storage/browser/quota/padding_key.cc
[modify] https://crrev.com/66eac028ac9538ef57bc6f1874a9249ed6310cf5/storage/browser/quota/padding_key.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/85b389caa7d725cdd31f59e9a2b79ff54804b7b7

commit 85b389caa7d725cdd31f59e9a2b79ff54804b7b7
Author: Staphany Park <staphany@chromium.org>
Date: Wed Mar 27 00:55:29 2019

AppCache: Add padding to cross-origin responses.

Bug: 918293
Change-Id: I4f16640f06feac009d6bbbb624951da6d2669f6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1488059
Commit-Queue: Staphany Park <staphany@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#644624}
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/BUILD.gn
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache.cc
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache.h
[add] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_backfillers.cc
[add] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_backfillers.h
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_database.cc
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_database.h
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_database_unittest.cc
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_entry.h
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_service_unittest.cc
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_storage_impl_unittest.cc
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_unittest.cc
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/content/browser/appcache/appcache_update_job.cc
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/storage/browser/quota/padding_key.cc
[modify] https://crrev.com/85b389caa7d725cdd31f59e9a2b79ff54804b7b7/storage/browser/quota/padding_key.h


### pw...@chromium.org (2019-03-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4caf891ba0492a24f62a34acd99117b8ddd31ff4

commit 4caf891ba0492a24f62a34acd99117b8ddd31ff4
Author: Findit <findit-for-me@appspot.gserviceaccount.com>
Date: Wed Mar 27 06:20:01 2019

Revert "AppCache: Add padding to cross-origin responses."

This reverts commit 85b389caa7d725cdd31f59e9a2b79ff54804b7b7.

Reason for revert:

Findit (https://goo.gl/kROfz5) identified CL at revision 644624 as the
culprit for failures in the build cycles as shown on:
https://analysis.chromium.org/waterfall/culprit?key=ag9zfmZpbmRpdC1mb3ItbWVyRAsSDVdmU3VzcGVjdGVkQ0wiMWNocm9taXVtLzg1YjM4OWNhYTdkNzI1Y2RkMzFmNTllOWEyYjc5ZmY1NDgwNGI3YjcM

Sample Failed Build: https://ci.chromium.org/buildbot/chromium.linux/Linux%20Tests%20%28dbg%29%281%29%2832%29/57482

Sample Failed Step: content_unittests

Original change's description:
> AppCache: Add padding to cross-origin responses.
> 
> Bug: 918293
> Change-Id: I4f16640f06feac009d6bbbb624951da6d2669f6c
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1488059
> Commit-Queue: Staphany Park <staphany@chromium.org>
> Reviewed-by: Victor Costan <pwnall@chromium.org>
> Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#644624}

Change-Id: Iab68370e154f858ae05b9cebc0e07ce666e93a1f
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 918293
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1540723
Cr-Commit-Position: refs/heads/master@{#644692}
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/BUILD.gn
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache.cc
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache.h
[delete] https://crrev.com/a7bd1af635e0a58528421d4eb2e93e3f92ed051c/content/browser/appcache/appcache_backfillers.cc
[delete] https://crrev.com/a7bd1af635e0a58528421d4eb2e93e3f92ed051c/content/browser/appcache/appcache_backfillers.h
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache_database.cc
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache_database.h
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache_database_unittest.cc
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache_entry.h
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache_service_unittest.cc
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache_storage_impl_unittest.cc
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache_unittest.cc
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/content/browser/appcache/appcache_update_job.cc
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/storage/browser/quota/padding_key.cc
[modify] https://crrev.com/4caf891ba0492a24f62a34acd99117b8ddd31ff4/storage/browser/quota/padding_key.h


### pw...@chromium.org (2019-03-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/04aaacb936a08d70862d6d9d7e8354721ae46be8

commit 04aaacb936a08d70862d6d9d7e8354721ae46be8
Author: Staphany Park <staphany@chromium.org>
Date: Wed Mar 27 09:25:17 2019

Reland "AppCache: Add padding to cross-origin responses."

This is a reland of 85b389caa7d725cdd31f59e9a2b79ff54804b7b7

Initialized CacheRecord::padding_size to 0.

Original change's description:
> AppCache: Add padding to cross-origin responses.
>
> Bug: 918293
> Change-Id: I4f16640f06feac009d6bbbb624951da6d2669f6c
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1488059
> Commit-Queue: Staphany Park <staphany@chromium.org>
> Reviewed-by: Victor Costan <pwnall@chromium.org>
> Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#644624}

Bug: 918293
Change-Id: Ie1d3f99c7e8a854d33255a4d66243da2ce16441c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1539906
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Staphany Park <staphany@chromium.org>
Cr-Commit-Position: refs/heads/master@{#644719}
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/BUILD.gn
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache.cc
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache.h
[add] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_backfillers.cc
[add] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_backfillers.h
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_database.cc
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_database.h
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_database_unittest.cc
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_entry.h
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_service_unittest.cc
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_storage_impl_unittest.cc
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_unittest.cc
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/content/browser/appcache/appcache_update_job.cc
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/storage/browser/quota/padding_key.cc
[modify] https://crrev.com/04aaacb936a08d70862d6d9d7e8354721ae46be8/storage/browser/quota/padding_key.h


### st...@chromium.org (2019-03-27)

[Empty comment from Monorail migration]

### st...@chromium.org (2019-03-27)

Starting a conversation on whether/when it would make sense to make any documentation on this bug public. At this point, the code has been published so it would be nice for developers to learn what's going on. I'm curious to hear if anyone has thoughts on whether there are specifics that would be worth withholding.

### pw...@chromium.org (2019-03-27)

awhalley@, palmer@: Any thoughts here?

My initial reaction is that this is a security vulnerability, so we'd wait until M75 is rolled out before discussing it. The comments in CLs discuss size padding, but don't mention HEIST anywhere, so it's not necessarily clear that we've disclosed the vulnerability in the code.

OTOH, if we consider this change to be disclosed, I think we should create a chromestatus.com entry for it. It is a Web-exposed change, so it'd be nice to give developers a heads-up when the M75 blog post comes along. This is also a new talking point in favor of Service Workers + Cache Storage -- AppCache doesn't support CORS, so all CDN resources are going to be padded.

### ev...@google.com (2019-03-27)

The patch and the rollback is being actively discussed by security researchers, so I would definitely suggest being open about this.

### sh...@chromium.org (2019-03-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-03-28)

Yes, since the fix impacts the design of the API, and since security people are apparently already looking at it, I think it is acceptable, but also preferable!, to be public about it. I don't think you need to withhold any details. Thanks!

### pw...@chromium.org (2019-03-29)

Per the comments above, I filed https://www.chromestatus.com/feature/5400170344742912 and sent a PSA to blink-dev@.

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-04)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-04-04)

+ adetaylor@ (Security TPM) for M74 merge review.

### ad...@google.com (2019-04-04)

+awhalley@

I'm going to pass this decision to awhalley@ since he's got the history here.

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $500 for this report. 

A member from our finance team will be in touch shortly

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### ab...@google.com (2019-04-15)

friendly ping awhalley@ - can you please take a look and comment on the urgency for this from security side? Even though this has baked in M75 for 18 days now, it's still a fairly sizeable change and I'd prefer 75.

### aw...@google.com (2019-04-15)

Per #35 it would be good for developers not be be surprised, so it's also late for a 74 merge on that account, too. Let's track for 75 and mea culpa for letting this slip through the cracks.


### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2019-06-13)

We re-considered the reward in the context of recently added Site Isolation special rewards and bypassing CORB was an interesting attack vector which we have addressed in https://crbug.com/chromium/927471. So, we are bumping up the reward to $1,000.

### na...@google.com (2019-06-13)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2019-07-16)

We have plenty of resources in our app cache and that consumes a huge cache storage. Our resources are only 18M but due to this feature it consumes 980M.

This features will effect our customer a lot 

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/918293?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Storage>AppCache, Internals>Sandbox>SiteIsolation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093606)*
