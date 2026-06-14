# Change on the credentials mode on redirect specified by the CORS algorithm should be propagated to net/

| Field | Value |
|-------|-------|
| **Issue ID** | [40085972](https://issues.chromium.org/issues/40085972) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HTML>Modules, Blink>Loader, Blink>SecurityFeature>CORS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dh...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2016-11-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Due to specification [1] import must fetch document in the anonymous mode to CORS and the credentials mode to same-origin.  

This works only if initial request referer to cross-origin, if we make request to same-origin and then make redirect to cross-origin - Chromium will make "credentialed" request!  

So if some origin sets "Access-Control-Allow-Origin: \*" imports allow to fetch personal data from any origin.

**VERSION**  

Chrome Version: 54.0.2840.100, 55.0.2883.44 beta, 56.0.2914.3 dev  

Operating System: GNU/Linux 4.5.4-1-ARCH

**REPRODUCTION CASE**  

0. First of all checks CORS policy on some origin:  

$ http -ph <https://private-dharrya.rhcloud.com/>  

HTTP/1.1 200 OK  

Access-Control-Allow-Origin: \*  

[...]

2. Alright, now open it to init session id: <https://private-dharrya.rhcloud.com/>
3. Check import w/o any redirects (PHPSESSID doesn't leak): <https://garbage.buglloc.com/cross-cred-import.html>
4. And finally check redirected import (PHPSESSID leaks): <https://garbage.buglloc.com/cross-cred-import.html?bypass>

As you can see, in case of redirect from same-origin import make "credentialed" request.

[1] <http://w3c.github.io/webcomponents/spec/imports/#h-fetching-import>

## Attachments

- [2016-11-16-112918.png](attachments/2016-11-16-112918.png) (image/png, 153.5 KB)

## Timeline

### me...@chromium.org (2016-11-18)

kochi: Can you please take a look?

Assigning medium severity since this is a bypass of the same origin policy with  preconditions.

[Monorail components: Blink>HTML>Modules]

### sh...@chromium.org (2016-11-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-19)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-11-21)

Let me take a look.

### ko...@chromium.org (2016-11-22)

Adding people more knowledgeable about CORS than I.

### ty...@chromium.org (2016-11-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>Loader]

### ty...@chromium.org (2016-11-22)

There's a long-lived bug in the loader. CrossOriginAccessControl::handleRedirect() updates ResourceLoaderOptions not to send credentials on same -> cross redirect. But it doesn't get reflected to the browser process. URLLoader::FollowRedirect() takes no argument. The browser process just follows the redirect with the same parameter settings when FollowRedirect() is invoked.

We've been unable to tackle this because it needs big change.

Anyway, the networking API team will take this.

### ty...@chromium.org (2016-11-30)

Started: https://codereview.chromium.org/2538073002/

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### ra...@chromium.org (2017-05-01)

Securit sheriff ping :) 

tyoshino: any update here? The CL linked seems to have stalled. 

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### dh...@gmail.com (2017-06-07)

Guys, any news? :)

### ty...@chromium.org (2017-06-07)

Sorry about the delay. I recently worked on refactoring on some related code. It's still on my Q2 OKRs and will resume working on this definitely soon.

### ko...@chromium.org (2017-06-07)

[Comment Deleted]

### ty...@chromium.org (2017-07-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fc9cdb626c7a9b95d429c88c215e9e7bba18fe55

commit fc9cdb626c7a9b95d429c88c215e9e7bba18fe55
Author: Takeshi Yoshino <tyoshino@chromium.org>
Date: Tue Jul 25 18:03:08 2017

Pass only what's needed to CheckCSPForRequest()

Since WebURLLoaderImpl or ResourceLoader never change the request
context, pass resource_->GetResourceRequest().GetRequestContext() to
CheckCSPForRequest() in WillFollowRedirect(). This is preparation for
clean up on ResourceLoader and WebURLLoaderImpl.

Bug: 665766
Change-Id: Ieea49d745eeb63c008ed24f3de2a47751d66e7f6
Reviewed-on: https://chromium-review.googlesource.com/583207
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Takeshi Yoshino <tyoshino@chromium.org>
Cr-Commit-Position: refs/heads/master@{#489365}
[modify] https://crrev.com/fc9cdb626c7a9b95d429c88c215e9e7bba18fe55/third_party/WebKit/Source/core/loader/BaseFetchContext.cpp
[modify] https://crrev.com/fc9cdb626c7a9b95d429c88c215e9e7bba18fe55/third_party/WebKit/Source/core/loader/BaseFetchContext.h
[modify] https://crrev.com/fc9cdb626c7a9b95d429c88c215e9e7bba18fe55/third_party/WebKit/Source/core/loader/BaseFetchContextTest.cpp
[modify] https://crrev.com/fc9cdb626c7a9b95d429c88c215e9e7bba18fe55/third_party/WebKit/Source/platform/loader/fetch/FetchContext.h
[modify] https://crrev.com/fc9cdb626c7a9b95d429c88c215e9e7bba18fe55/third_party/WebKit/Source/platform/loader/fetch/ResourceFetcher.cpp
[modify] https://crrev.com/fc9cdb626c7a9b95d429c88c215e9e7bba18fe55/third_party/WebKit/Source/platform/loader/fetch/ResourceLoader.cpp
[modify] https://crrev.com/fc9cdb626c7a9b95d429c88c215e9e7bba18fe55/third_party/WebKit/Source/platform/loader/testing/MockFetchContext.h


### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d0c5d35b403299a6777918c5ed32bec25f65aca4

commit d0c5d35b403299a6777918c5ed32bec25f65aca4
Author: Takeshi Yoshino <tyoshino@chromium.org>
Date: Thu Jul 27 23:13:27 2017

Build a ResourceRequest with net::RedirectInfo applied in ResourceLoader::WillFollowRedirect()

Currently, the WebURLLoaderImpl builds a WebURLRequest, applies
net::RedirectInfo and passes it to the ResourceLoader and holds the
built WebURLRequest also in it. This back and forth data passing is
confusing and misleading. People often think that data modified on the
WebURLRequest in ResourceLoader are propagated to net/ which is not
true.

The WebURLLoaderImpl::Context also holds the initial WebURLRequest
passed to Start() in |request_|. It's wasteful as the Resource also
holds copies of ResourceRequests for the whole redirect chain including
the initial one.

Bug: 665766
Change-Id: Ie13776f03c5f64ad577e20f7b32c68ceb73f94d2
Reviewed-on: https://chromium-review.googlesource.com/583107
Commit-Queue: Takeshi Yoshino <tyoshino@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#490075}
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/content/child/web_url_loader_impl.cc
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/content/child/web_url_loader_impl.h
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/content/child/web_url_loader_impl_unittest.cc
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/third_party/WebKit/Source/platform/loader/fetch/ResourceLoader.cpp
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/third_party/WebKit/Source/platform/loader/fetch/ResourceLoader.h
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/third_party/WebKit/Source/platform/loader/fetch/ResourceRequest.h
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/third_party/WebKit/Source/platform/testing/weburl_loader_mock.cc
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/third_party/WebKit/Source/platform/testing/weburl_loader_mock.h
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/third_party/WebKit/Source/platform/testing/weburl_loader_mock_factory_impl.cc
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/third_party/WebKit/Source/platform/testing/weburl_loader_mock_factory_impl.h
[modify] https://crrev.com/d0c5d35b403299a6777918c5ed32bec25f65aca4/third_party/WebKit/public/platform/WebURLLoaderClient.h


### bu...@chromium.org (2017-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e2e05a05d39d82f3fcbd70bf4da3180455c9d537

commit e2e05a05d39d82f3fcbd70bf4da3180455c9d537
Author: Takeshi Yoshino <tyoshino@chromium.org>
Date: Fri Jul 28 12:16:49 2017

Make it clear where and why the parameters in the ResourceRequest for the initial request are used

- Rename the local variable |request| to |initial_request| in
  ResourceLoader::WillFollowRedirect() which holds
  resource_->GetResourceRequest().
- Perform DCHECKs after FetchContext::PrepareRequest() and
  FetchContext::DispatchWillSendRequest() on the invariant parameters
- Use GetResourceRequest() than LastResourceRequest() where possible

As a bonus pass kFollowedRedirect to CanRequest() call in
WillFollowRedirect() as it's clear that it's kFollowRedirect there.

Bug: 665766
Change-Id: I5acaabdbbbac6503156305c6c107c75a378c5858
Reviewed-on: https://chromium-review.googlesource.com/588869
Commit-Queue: Takeshi Yoshino <tyoshino@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#490367}
[modify] https://crrev.com/e2e05a05d39d82f3fcbd70bf4da3180455c9d537/third_party/WebKit/Source/platform/loader/fetch/ResourceLoader.cpp


### bu...@chromium.org (2017-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b5cc78139a0259853a9d35ecd7a0037d6b6f9d31

commit b5cc78139a0259853a9d35ecd7a0037d6b6f9d31
Author: Takeshi Yoshino <tyoshino@chromium.org>
Date: Tue Aug 01 06:38:07 2017

Clarify which ResourceRequest is used in ResourceLoader::DetermineCORSStatus()

Follow up for https://chromium-review.googlesource.com/c/588869/.

Bug: 665766
Change-Id: Iee79d525c3d3ff9afa98fe0a5cc52c0ee8921540
Reviewed-on: https://chromium-review.googlesource.com/592007
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Takeshi Yoshino <tyoshino@chromium.org>
Cr-Commit-Position: refs/heads/master@{#490887}
[modify] https://crrev.com/b5cc78139a0259853a9d35ecd7a0037d6b6f9d31/third_party/WebKit/Source/platform/loader/fetch/ResourceLoader.cpp


### bu...@chromium.org (2017-08-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c8cc6281f4f0a7b581a6451b35db3574109985ce

commit c8cc6281f4f0a7b581a6451b35db3574109985ce
Author: Takeshi Yoshino <tyoshino@chromium.org>
Date: Tue Aug 22 06:39:50 2017

Add a comment explaining why ResourceFetcher::PrepareRequest() needs to use ResourceRequest::GetRedirectStatus()

Bug: 665766
Change-Id: Iec7a76fcd49d39d32197a5df1ea307ea095d3253
Reviewed-on: https://chromium-review.googlesource.com/620514
Commit-Queue: Takeshi Yoshino <tyoshino@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#496234}
[modify] https://crrev.com/c8cc6281f4f0a7b581a6451b35db3574109985ce/third_party/WebKit/Source/platform/loader/fetch/ResourceFetcher.cpp


### ty...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>CORS]

### da...@chromium.org (2017-09-01)

+cbentzel, the net stack team really needs someone more familiar with web platform bits. I shouldn't be the point of contact for everything.

### ty...@chromium.org (2017-09-14)

https://crbug.com/chromium/665766#c25: Yeah, I just CC-ed you as I referred this bug so that you can view this.

### ty...@chromium.org (2017-09-14)

Renaming the summary to describe what we're actually working on.

### yh...@chromium.org (2017-10-04)

[Empty comment from Monorail migration]

### ty...@chromium.org (2017-10-12)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-11-04)

friendly ping from the security sheriff!

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-11-29)

Any update on this year-old bug? I see various CLs have landed; is this bug Fixed, or is there more work left to do?

### ty...@chromium.org (2017-11-29)

Current plan is that toyoshim@ will fix it in the context of moving CORS logic out of Blink. He's actively working on that project.

### to...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### fe...@chromium.org (2018-02-14)

hi toyoshim@, how is the project going? we're doing a security bug triage and are checking that bug status is up to date.

### to...@chromium.org (2018-02-16)

Tens of CLs were already landed to make this happen, but it still need more works to start experiments. See the https://crbug.com/chromium/736308 and 803766 for details of recent progress.

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### to...@chromium.org (2019-05-09)

updates: OOR-CORS is enabled by default, but it does not include this fix yet.

### sh...@chromium.org (2019-05-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-23)

toyoshim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2019-05-24)

my budget for CORS was used for another security work, but now that work was finished, this will be the next target.

### to...@chromium.org (2019-05-24)

remove people who already left the project from CC

### to...@chromium.org (2019-05-28)

I confirmed that this issue was already solved only when OOR-CORS is enabled.
Since OOR-CORS will be fully enabled at m75, I will change the status to be Fixed.

### to...@chromium.org (2019-05-28)

For a record, here is the step I tried:

1. access http://alt-yuri.twintail.org/chrome/cors/set_cookie.cgi
2. access http://alt-yuri.twintail.org/chrome/cors/test.cgi to see if the cookie was set as expected
3. access http://yuri.twintail.org/chrome/cors/665766.html?bypass to see if the cookie wasn't sent as expected
 (this will make a request to /chrome/cors/redirect.cgi, that results in a redirect to http://alt-yuri.twintail.org/chrome/cors/test.cgi)
3. cookie is empty like this 
> Private data:
> test content, cookie=

### sh...@chromium.org (2019-05-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-29)

Not requesting merge to M75 because latest trunk commit (489365) appears to be prior to beta branch point (652427). If this is incorrect, please replace the Merge-na label with Merge-Request-75. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

Hi  dharrya@ - how would you like to be credited in the chrome release notes?

### dh...@gmail.com (2019-06-04)

Hi awhalley@ - "Andrew Krasichkov, Yandex Security Team", would ge great :)

### to...@chromium.org (2019-06-04)

Note that OOR-CORS ship is postponed to m76.
So, this behavior change happens on m76 actually, and still it's a plan.

Can you track the progress by crbug.com/905971

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### dh...@gmail.com (2019-06-05)

Hi guys, I'm a little bit confused:
  - in release notes your mention this issue as resolved in 75.0.3770.80: https://chromereleases.googleblog.com/2019/06/stable-channel-update-for-desktop.html
  - toyoshim@ says that OOR-CORS is postponed to m76

Who is right?)

P.S. I just update  my Chromium to 75.0.3770.80, OOR-CORS are disabled by default and issue sucessfully reproduced. 

### aw...@google.com (2019-06-05)

Ah, yes - for the release notes I was going off the https://crbug.com/chromium/665766#c54 and the notes were already in flight by the time https://crbug.com/chromium/665766#c62 was made. Looks like M76 is correct.

### na...@google.com (2019-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-06-13)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-13)

Congrats! The Panel decided to reward $1,000 for this report!

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2020-07-09)

Hello  dharrya@ - this reward has gone unclaimed for over a year. Please get in touch immediately if you still wish to receive the award, otherwise it will be donated to charity.

### aw...@google.com (2020-07-23)

This reward will be donated to charity.

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/665766?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>Modules, Blink>Loader, Blink>SecurityFeature>CORS]
[Monorail blocked-on: crbug.com/chromium/736308]
[Monorail mergedwith: crbug.com/chromium/653765]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085972)*
