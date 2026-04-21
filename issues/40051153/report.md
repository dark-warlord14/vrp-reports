# Leaking size of cross-origin resource by caching it twice

| Field | Value |
|-------|-------|
| **Issue ID** | [40051153](https://issues.chromium.org/issues/40051153) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>CacheStorage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2020-01-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Currently, opaque resources are added to the cache with random padding to avoid leaking their actual size (<https://crbug.com/chromium/617963>).

Although the padding is random for each different resource, it remains the same if you try to add the same resource multiple times to the cache. The way Chrome detects whether resources are different is by checking their URL.

This means that if you try to cache the following resource twice:  

<https://victim.com/resource>

You will get (response\_size + same\_padding) \* 2 on navigator.storage.estimate().

This also means that if the response\_size on <https://victim.com/resource> changes in between the first and second time of caching, it would be possible to retrieve their size difference.

1. Cache <https://victim.com/resource>
2. Cache\_size\_1 = response\_size + same\_padding.
3. Size of <https://victim.com/resource> increases in 1337 bytes.
4. Cache <https://victim.com/resource>
5. Cache\_size\_2 = response\_size + 1337 + same\_padding.
6. Doing (Cache\_size\_2 - Cache\_size\_1) results in 1337.

Following the steps mentioned above, we can leak that there was a 1337 bytes increase on that particular resource. The clear downside is that an attacker would have to be able to affect the resource's response size to be able to leak how many bytes increased or decreased from the response.

Fortunately, that can be accomplished without interacting with the application in any way. That is possible by abusing requests made with the HEAD and GET methods.

1. Cache the response of HEAD request to <https://victim.com/resource>
2. Cache\_size\_1 = headers\_size + same\_padding.
3. Cache the response of GET request to <https://victim.com/resource>
4. Cache\_size\_2 = headers\_size + body\_size + same\_padding.
5. Doing (Cache\_size\_2 - Cache\_size\_1) results in body\_size.

By following the steps above we would be able to leak the size of the response's body (assuming that the size of the headers didn't change). There is one small inconvenience, which is that navigator.storage.estimate (which we use to retrieve the number of bytes in the cache) also pads the number of stored bytes to multiples of 256.

This would imply that it is only possible to get a resolution of 256 bytes on the size difference of the same resource. However, I also noticed that the URL of the request is stored inside the cache and that it can be leveraged as padding to discover the real size (with a resolution of 3 bytes) that is stored.

I provided a PoC with 256-bytes resolution rather than the 3-bytes one because it would be significantly more complex to implement and I didn't feel it was necessary to understand the core idea behind this bug.

The vulnerability allows leaking the size of cross-origin resources that are not CORB'd with a 3-bytes resolution.

**VERSION**  

Version 79.0.3945.88 (Official Build) (64-bit)

**REPRODUCTION CASE**

1. Go to <https://lbherrera.me/chrome/cache-leak/index.php>
2. Type <https://victim.lbherrera.me/size.php?size=1337> in the input field and click on the button.
3. A message saying the number of bytes of the cross-origin resource should be displayed.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.html](attachments/index.html) (text/plain, 2.7 KB)

## Timeline

### mb...@chromium.org (2020-01-08)

cmumford: Could you take a look at this or help find another owner?

[Monorail components: Blink>Storage>CacheStorage]

### sh...@chromium.org (2020-01-09)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-22)

cmumford: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-02-06)

cmumford: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@gmail.com (2020-02-18)

Hi, friendly ping on this issue!

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### he...@gmail.com (2020-07-07)

Hi, friendly ping on this issue!

### [Deleted User] (2020-07-14)

cmumford: Uh oh! This issue still open and hasn't been updated in the last 188 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@chromium.org (2020-07-15)

Am no longer on storage team. Returning to available and cc'ing wanderview@ for awareness.

### wa...@chromium.org (2020-07-15)

I believe this is the same as https://crbug.com/chromium/1013906, but using varying request method instead of credentials.  The most straightforward solution would be to include the request method in the padding hash as well.

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### wa...@chromium.org (2020-07-16)

I've started a WIP CL here:

https://chromium-review.googlesource.com/c/chromium/src/+/2303770

So far it only includes a test that provokes the problem.

### wa...@chromium.org (2020-07-17)

One tricky thing here is we can't just hash the http method string directly.  An attacker could use arbitrary methods and some servers will just treat it as a GET.  This would allow an attacker to average out the padding.  So we will likely hash well known methods individually and treat all other methods as a single "other" bucket.

### wa...@chromium.org (2020-07-21)

> One tricky thing here is we can't just hash the http method string directly.  An attacker could use arbitrary methods and some servers will just treat it as a GET.

Testing showed this was not a valid concern.  The spec only permits GET, HEAD, and POST for no-cors requests.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cf53a83ff3663068ba94c8b420e727c1954ec230

commit cf53a83ff3663068ba94c8b420e727c1954ec230
Author: Ben Kelly <wanderview@chromium.org>
Date: Tue Jul 21 14:27:16 2020

CacheStorage: Vary opaque padding on http request method.

This CL consists of the following changes:

 * Plumbing to remember the request method used to load a fetch
   Response.
 * Storing the request method alongside the Response in cache_storage.
 * Using this information in the padding computation.
 * Black box http web test.

Bug: 1039882
Change-Id: Ifcf4a638b1de857260bf44e5683224410dc7bf26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2303770
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/master@{#790370}

[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/content/browser/appcache/appcache_backfillers.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/content/browser/appcache/appcache_update_job.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/content/browser/cache_storage/cache_storage.proto
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/content/browser/cache_storage/cache_storage_cache_unittest.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/content/browser/cache_storage/cache_storage_manager_unittest.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/content/browser/cache_storage/legacy/legacy_cache_storage_cache.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/content/common/background_fetch/background_fetch_types.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/storage/browser/quota/padding_key.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/storage/browser/quota/padding_key.h
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/third_party/blink/public/mojom/fetch/fetch_api_response.mojom
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/third_party/blink/renderer/core/fetch/fetch_manager.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/third_party/blink/renderer/core/fetch/fetch_response_data.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/third_party/blink/renderer/core/fetch/fetch_response_data.h
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/third_party/blink/renderer/core/fetch/response.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/third_party/blink/renderer/modules/service_worker/fetch_event.cc
[modify] https://crrev.com/cf53a83ff3663068ba94c8b420e727c1954ec230/third_party/blink/web_tests/http/tests/cachestorage/padding.html


### wa...@chromium.org (2020-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-27)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-30)

Congratulations! The VRP panel has decided to award $2,000 for this report.

### ad...@google.com (2020-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-04)

Not requesting merge to beta (M86) because latest trunk commit (790370) appears to be prior to beta branch point (800218). If this is incorrect, please replace the Merge-na label with Merge-Request-86. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-11-03)

This issue was migrated from crbug.com/chromium/1039882?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051153)*
