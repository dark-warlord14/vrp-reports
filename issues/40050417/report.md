# Security: expose stored (in cache) cross-site response's size

| Field | Value |
|-------|-------|
| **Issue ID** | [40050417](https://issues.chromium.org/issues/40050417) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>CacheStorage, Blink>Storage>Quota |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ba...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2019-10-12 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

I think that there is a way to expose the size of cross-site responses using storing them in a cache.

Intro:

1. XS-Search is an attack that tried to distinguish between responses that had search results and responses that did not. Most of the known XS-Search attacks are time-based. The attack here is not Time based but Length based.
2. The vulnerable code still exists in the last version of chrome that I've checked (73.0.3683.103).

Since version 63, a padding mechanism to cross-site responses that are stored in the cache was developed and integrated. I found a way to bypass the padding mechanism to launch another XS-Search attack, by sending 2 different requests to the same URL.

In this padding mechanism, the response size saved is the sum of the actual response size plus an additional random and unpredictable amount, I refer to as PaddingSize. The padding mechanism prevents Quota Management API from revealing the response's size by adding the PaddingSize to the actual size.

The PaddingSize is calculated as follows:

1. hmac sha256 function is calculated to the request URL using a 128-bit key.
2. The first 8 bytes of the MAC are copied to an uint64 variable.
3. Modulo MAX\_PADDING is calculated to meet the constraints of max Padding Size.

The code the calculates the padding size is in cache\_storage\_cache.cc file on function ComputeResponsePadding(Last version that I've checked is 77.0.3865.112 and the code is here: <https://chromium.googlesource.com/chromium/src/+/refs/tags/77.0.3865.112/storage/browser/quota/padding_key.cc>)

In light of the above, it can be inferred that responses originating from the same URL will get the same padding size, while responses originating from different URLs will get different padding sizes.

I investigated dozens of search engines on different websites and checked which page was received when we searched a query without an authenticated user (i.e. without sending cookies that identified the user). In 95% of the observed cases, the response was a page that was similar or identical to a page that was received for an authenticated user's search query bearing 0 search results.

In the attached code, I chose to exploit YouTube watching history search interface (<https://www.youtube.com/feed/history?query=QUERY>) but it can exploit any similar search interface.

Now to the exploit steps:

1. Sample the usage using Quota API.
2. Send a request to the attacked URL without cookies and store the response in the cache. The response is a no-results page, due to the non-authentication.
3. Sample the usage using Quota API again. This discloses the sum of the response size (that bore 0 search results) and the padding size – let it be X.
4. Send a request to the same URL, this time with cookies that identify the victim, and store the response in the cache. This response holds search results from the victim's account, containing private information.
5. Sample the usage with Quota API once more. This discloses the sum of the response size that did bear search results and the padding size – let it be Y.  
   
   (note that since the URL did not change, the padding size remained the same).
6. calculate the subtraction of Y and X: Y-X.
7. Y-X is the size of the search records in the response.

Using the size of the search records we can infer how many records returned to the query and by that expose private information in that specific case - watching history.  

We can know if the user like a specific band, intersting in a specific subject, and etc.

Note that the exploit works only in versions earlier to version 67. Since version 67, CORB denies suspicious cross-site requests. The attached exploit will work only if a CORB bypass exploit will be found.  

Chrome designed with multiple layers of security protections and that why I think you should fix that vulnerability anyway.

Please feel free to contact me if you need any further information.

**VERSION**  

Chrome Version: 65.0.3325.181  

Operating System: Win 7

**REPRODUCTION CASE**  

You can use the attached files to expose YouTube watch history of logged in user  

The result is how many videos the user watched for the search query.

**CREDIT INFORMATION**  

Reporter credit: B@rMey

## Attachments

- [index.html](attachments/index.html) (text/plain, 7.8 KB)
- [k2.js](attachments/k2.js) (text/plain, 2.7 KB)

## Timeline

### aj...@google.com (2019-10-14)

Thanks for the report. I will look at reproducing it on Monday. Marking as Low as this must be combined with a CORB bypass to be effective.

### sh...@chromium.org (2019-10-14)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2019-10-14)

pwnall@ could you take a look at this report? This is not easily reproducible as CORB blocks the requests.

[Monorail components: Blink>Storage Blink>Storage>Quota]

### sh...@chromium.org (2019-10-15)

[Empty comment from Monorail migration]

### js...@chromium.org (2019-10-15)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Storage Blink>Storage>CacheStorage]

### js...@chromium.org (2019-10-15)

[Empty comment from Monorail migration]

### wa...@chromium.org (2019-10-15)

One possible solution here would be to include the credentials flag in the hash computation.  So url+no-credentials would have one stable hash and url+credentials would have a different stable hash.

This wouldn't protect against other potential cases where an attacker can force a resource to change size in a predictable way via other means, though.  Maybe that's ok, though, since logged in state is the most important piece of state to protect.

### pw...@chromium.org (2019-10-16)

Agreed that this is a good step forward in the mitigation.

wanderview@: Can you please implement this fix? Please LMK if you can't fit it on your plate, and I'll figure something out.

### wa...@chromium.org (2019-10-25)

I will try to fit this into my list for M80.  If this is not fast enough, we may need to find someone else to tackle it.

### wa...@chromium.org (2019-12-06)

CL up for review: https://chromium-review.googlesource.com/c/chromium/src/+/1956044

This CL sets a "credentialed" flag in the fetch_manager based on the request credentials mode and the tainting.  For opaque responses we will only get a credentialed state if the mode is 'include'.

The flag is then plumbed through the different fetch serialization types and down to the serialized cache_storage protobuf.  We treat older stored responses as simply non-credentialed.  I don't think its worth doing a migration of old data since this a defense in depth issue and not directly exploitable.

Finally the flag is used to add additional input to the padding hash calculation.

The CL includes both a unit test and an end-to-end web_test.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/64d2022359fed5668c631dda83cda2dfd7e956ce

commit 64d2022359fed5668c631dda83cda2dfd7e956ce
Author: Ben Kelly <wanderview@chromium.org>
Date: Mon Dec 09 23:20:56 2019

CacheStorage: Vary opaque padding based on if a response was loaded with credentials.

Bug: 1013906
Change-Id: Ib65cd440ede20c79affb063ae458dff449dd814d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1956044
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#723150}

[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/content/browser/appcache/appcache_backfillers.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/content/browser/appcache/appcache_update_job.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/content/browser/cache_storage/cache_storage.proto
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/content/browser/cache_storage/cache_storage_cache_unittest.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/content/browser/cache_storage/cache_storage_manager_unittest.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/content/browser/cache_storage/legacy/legacy_cache_storage_cache.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/content/common/background_fetch/background_fetch_types.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/storage/browser/quota/padding_key.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/storage/browser/quota/padding_key.h
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/third_party/blink/public/mojom/fetch/fetch_api_response.mojom
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/third_party/blink/renderer/core/fetch/fetch_manager.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/third_party/blink/renderer/core/fetch/fetch_response_data.cc
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/third_party/blink/renderer/core/fetch/fetch_response_data.h
[modify] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/third_party/blink/renderer/core/fetch/response.cc
[add] https://crrev.com/64d2022359fed5668c631dda83cda2dfd7e956ce/third_party/blink/web_tests/http/tests/cachestorage/padding.html


### ba...@gmail.com (2019-12-10)

Looks great.
Just to make sure we are on the same page, this mitigation is not effective against an attacker that can control the resource size via other means.

By the way, any chance for a bounty?

### pw...@chromium.org (2019-12-10)

+adetaylor@ for the bounty question

### ad...@chromium.org (2019-12-10)

bar320@ It looks like it's going to result in a fix to Chrome which we wouldn't otherwise have made, so it will go to the VRP panel for consideration. It may well take a few weeks for them to get to it. Thanks for the report!

### wa...@chromium.org (2019-12-10)

[Comment Deleted]

### wa...@chromium.org (2019-12-10)

> Just to make sure we are on the same page, this mitigation is not effective against an attacker that can control the resource size via other means.

Correct.  This protects mutation based on credentials which tends to map to logged-in state which seems the most important aspect to protect.

### wa...@chromium.org (2019-12-10)

If you feel there is another easy avenue of controlling response size, please re-open or file another bug.  Thanks.

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### ba...@gmail.com (2020-02-05)

1) When the fix will be released? I'm asking because I would like to publish my paper about cross-site search attacks.
2) Do you assign a CVE for this bug? 

### wa...@chromium.org (2020-02-05)

The fix is in M81 which will not be released to stable until around March 17, 2020.  I do not know about the CVE question, but hopefully someone from security will respond.

### ad...@chromium.org (2020-02-05)

bar320@ thanks again for the report! Once this is released in M81, it will be credited in the release notes and we'll allocate a CVE at that time.

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### is...@google.com (2020-04-14)

This issue was migrated from crbug.com/chromium/1013906?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage>CacheStorage, Blink>Storage>Quota]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050417)*
