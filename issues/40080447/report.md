# Do Not Cache Resources Retrieved Via Broken HTTPS in AppCache Or Service Worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40080447](https://issues.chromium.org/issues/40080447) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>ServiceWorker |
| **Reporter** | ji...@gmail.com |
| **Assignee** | mi...@chromium.org |
| **Created** | 2014-09-13 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

For the site over HTTPS with an invalid certificate (e.g., self-signed and domain mismatch), Chrome may cache the resources (e.g., pages) over broken HTTPS in HTML5 AppCache, if the site contains AppCache manifest. If the user is under an MITM attack in a public area (e.g., airport), the attacker can replace the site's page with a malicious one that contains a long-lived (e.g., one year) AppCache manifest, once the user clicks through an SSL warning. When the user returns to a safe place without under MITM attacks, and visits the same site, Chrome will directly load the malicious page in AppCache instead of issuing new requests until the long-lived manifest expires.

**VERSION**  

Chrome Version: [37.0.2062.120] + [stable] (previous versions may have the same problem.)  

Operating System: [OS X 10.9.3]

**REPRODUCTION CASE**

0. Suppose the targeted site is <https://yahoo.com>, the attacker hosts a malicious server and site, and the victim is under a MITM attack. The attacker can utilize a host of well-known MITM techniques (e.g., ARP poisoning and DNS pharming attacks) to re-route all the traffic of the victim to himself. In our experiment, we use mitmproxy to simulate the attack.
1. When the user visits <https://yahoo.com>, the attacker intercepts the connection;
2. Once the user clicks through the SSL warning raised by Chrome, the attacker can substitute the malicious page for the original one. The malicious one contains a long-lived AppCache manifest;
3. Chrome caches the malicious copy in AppCache for a long time. When the user visits <https://yahoo.com> again in a safe place, his Chrome will directly load the malicious copy from AppCache.

To simply demonstrate the caching scenario:

1. Download the attached test.html and test.appcache;
2. Host the two files on the local server that enables HTTPS with self-signed certificate;
3. Using Chrome visit test.html and click through the SSL warnings;
4. Check "chrome://appcache-internals/", and Chrome will show that test.html is cached in AppCache.

In all, Chrome caches hijacked resources over HTTPS in AppCache in the MITM scenario.  

The attached picture "yahoo1" is the malicious copy in AppCache, and the "appcache-internals" is the screenshot to show that Chrome caches replaces page over broken HTTPS in AppCache.

At present, Chrome does not cache resources over broken HTTPS connections, which is desirable for security. However, HTML5 AppCache resources over broken HTTPS connections should not be cached as well, and such security restriction has already been implemented in Safari.

## Attachments

- [test.html](attachments/test.html) (text/html, 102 B)
- [appcache-internals.png](attachments/appcache-internals.png) (image/png, 104.8 KB)
- [test.appcache](attachments/test.appcache) (application/octet-stream, 55 B)
- [yahoo1.png](attachments/yahoo1.png) (image/png, 18.8 KB)

## Timeline

### ts...@chromium.org (2014-09-16)

@palmer - care to take a stab at this one? Thanks.

### cl...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-09-16)

michaeln: Any pointers on where in the code I should start looking?

### pa...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### mi...@chromium.org (2014-09-16)

appcache_update_job.cc

### mi...@chromium.org (2014-09-16)

Look at it's URLFetcher class in particular.

### mi...@chromium.org (2014-09-16)

We need to do something similar for service workers.

### mi...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-09-17)

[Empty comment from Monorail migration]

### ji...@gmail.com (2014-09-17)

Hi, michaeln & palmer,

Do you double-check this security bug on other versions of Chrome? I've tested on 35, 36 and 37, but not sure about other versions. 
BTW, I have a suggestion to fix this bug. You can simply modify the source code to let Chrome not cache the manifest over broken HTTPS in AppCache. Thus Chrome will not store other resources listed in the manifest. Thanks.

### pa...@chromium.org (2014-09-17)

We only support the latest stable version of Chrome. The fix for this bug will go into Chrome 38.

### pa...@chromium.org (2014-09-17)

Note that according to https://code.google.com/p/chromium/issues/detail?id=78859, this bug should not be happening?! So, something very odd is going on.

### pa...@chromium.org (2014-09-23)

I'm still having a really hard time find my way around the maze of indirect function calls. I think it might be best if someone else takes this bug. Also, maybe rsleevi has some clues.

### rs...@chromium.org (2014-09-26)

David's been looking carefully at a lot of stuff, and probably can dig in further.

As for where this happens presently in the //net stack, it's https://code.google.com/p/chromium/codesearch#chromium/src/net/http/http_cache_transaction.cc&l=2628

The magic you're looking for is:
if (net::IsCertStatusError(response_.ssl_info.cert_status))

I honestly can't follow all the crazy logic in app cache / service worker either, but it seems like the correct thing to do is simply not allow an SW/AC to be installed if the document ssl_info meets the above criteria.

Pushing to Michael for app cache. I'm pretty sure the critical path is https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/appcache/appcache_update_job.cc&rcl=1411534708&l=504


### mi...@chromium.org (2014-10-02)

> net::IsCertStatusError(response_.ssl_info.cert_status)

Yup, that looks like the 'magic' that was missing.

### mi...@chromium.org (2014-10-02)

We should probably reject any resource with a cert error, URLFetcher probably can error out early in...

https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/appcache/appcache_update_job.cc&rcl=1411534708&l=163

### cl...@chromium.org (2014-10-10)

michaeln@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-10-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3ec982d993b769efc893d4f3a0fa28eea95b69d0

commit 3ec982d993b769efc893d4f3a0fa28eea95b69d0
Author: michaeln <michaeln@chromium.org>
Date: Thu Oct 16 22:53:02 2014

Do not AppCache responses with SSL cert errors.

BUG=414026

Review URL: https://codereview.chromium.org/645123003

Cr-Commit-Position: refs/heads/master@{#299999}

[modify] https://chromium.googlesource.com/chromium/src.git/+/3ec982d993b769efc893d4f3a0fa28eea95b69d0/content/browser/appcache/appcache_update_job.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/3ec982d993b769efc893d4f3a0fa28eea95b69d0/content/browser/appcache/appcache_update_job.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/3ec982d993b769efc893d4f3a0fa28eea95b69d0/tools/metrics/histograms/histograms.xml


### cl...@chromium.org (2014-10-18)

michaeln@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### mi...@chromium.org (2014-10-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### do...@chromium.org (2014-10-21)

CC horo. https://crbug.com/chromium/425396 sounds related?

### ho...@chromium.org (2014-10-21)

Yes https://crbug.com/chromium/425396 is related this issue.
I think we should add net::IsCertStatusError() check in ServiceWorkerWriteToCacheJob::OnResponseStarted().

### bu...@chromium.org (2014-10-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a8ac964e0cf580c4e72028f81f1cda335436659d

commit a8ac964e0cf580c4e72028f81f1cda335436659d
Author: horo <horo@chromium.org>
Date: Wed Oct 22 07:13:11 2014

[ServiceWorker] Don't register ServiceWorker with an invalid HTTPS certificate.

BUG=425396,414026

Review URL: https://codereview.chromium.org/643773004

Cr-Commit-Position: refs/heads/master@{#300644}

[modify] https://chromium.googlesource.com/chromium/src.git/+/a8ac964e0cf580c4e72028f81f1cda335436659d/content/browser/service_worker/service_worker_write_to_cache_job.cc


### bu...@chromium.org (2014-10-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2a744d445b7dde718c85f392bc24c3ddc7e7f987

commit 2a744d445b7dde718c85f392bc24c3ddc7e7f987
Author: horo <horo@chromium.org>
Date: Thu Oct 23 11:15:37 2014

[ServiceWorker] Add unittests for ServiceWorkerWriteToCacheJob.

BUG=425396, 414026

Review URL: https://codereview.chromium.org/660253004

Cr-Commit-Position: refs/heads/master@{#300867}

[modify] https://chromium.googlesource.com/chromium/src.git/+/2a744d445b7dde718c85f392bc24c3ddc7e7f987/content/browser/service_worker/service_worker_provider_host.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/2a744d445b7dde718c85f392bc24c3ddc7e7f987/content/browser/service_worker/service_worker_storage.h
[add] https://chromium.googlesource.com/chromium/src.git/+/2a744d445b7dde718c85f392bc24c3ddc7e7f987/content/browser/service_worker/service_worker_write_to_cache_job_unittest.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/2a744d445b7dde718c85f392bc24c3ddc7e7f987/content/content_tests.gypi


### mi...@chromium.org (2014-10-23)

horo found more magic, net::HttpNetworkSession::Params.ignore_certificate_errors should be looked at too

### do...@chromium.org (2014-10-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-30)

Let it roll into M40

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c65cc9c7b1afe7f53bb18707bc711dc32ddffad0

commit c65cc9c7b1afe7f53bb18707bc711dc32ddffad0
Author: michaeln <michaeln@chromium.org>
Date: Fri Nov 14 01:40:39 2014

Do not AppCache responses with SSL cert errors unless running with the --ignore-certificate-errors flag.

BUG=414026

Review URL: https://codereview.chromium.org/725573004

Cr-Commit-Position: refs/heads/master@{#304140}

[modify] https://chromium.googlesource.com/chromium/src.git/+/c65cc9c7b1afe7f53bb18707bc711dc32ddffad0/content/browser/appcache/appcache_update_job.cc


### pa...@chromium.org (2014-12-02)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congratulations - $500 for this report! Notes from panel: "User would have to click through bad HTTPS to trigger,. reducing the reward amount to $500".

We've credited you in our release notes as "jiayaoqijia" - let me know if you want to use a different name/handle.

Someone should be in touch within a few weeks to collect payment details.

### ji...@gmail.com (2015-01-23)

Hi, tim,

Thanks for the reward. The name can be changed to Yaoqi Jia. Thanks.

### cl...@chromium.org (2015-01-27)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-11)

Updated your name for credit: http://googlechromereleases.blogspot.com/2015/01/stable-update.html

You should also receive an email shortly regarding payment.

### ji...@gmail.com (2015-03-18)

Hi, tim,

Got it. Thanks. :)

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/414026?no_tracker_redirect=1

[Multiple monorail components: Blink>ServiceWorker, Blink>Storage>AppCache]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080447)*
