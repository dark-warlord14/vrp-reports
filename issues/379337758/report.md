# Service workers allowing redirects to data: URLs.

| Field | Value |
|-------|-------|
| **Issue ID** | [379337758](https://issues.chromium.org/issues/379337758) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 130.0.0.0 |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-11-16 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

This issue is split from <https://issues.chromium.org/40064165> someone provided a hosted PoC <https://crbug40064165.glitch.me/>

# index.html

```
<script>
  navigator.serviceWorker.register('swredirect.js');
  setTimeout(() => {
    location.reload();
  }, 1000);
</script>

```
# swredirect.js

```
self.addEventListener('fetch', function(event) {
    event.respondWith(Response.redirect('data:text/html,<script>prompt("Test")</script>'));
});

```

Now doing `open()` to the HTTP URL of the service worker you will get redirected to a top-level data: URL.

# Problem Description

Top-level navigations of this type are also not normally allowed. <https://blog.mozilla.org/security/2017/11/27/blocking-top-level-navigations-data-urls-firefox-59/>
This navigation inherits from the opener as shown for the origin in the protocol confirmation dialog and also leaks the victims CSP.

```
const observer = new ReportingObserver(
  (reports, observer) => {
    reports.forEach((violation) => {
      console.log(violation);
      console.log(JSON.stringify(violation));
    });
  },
  {
    types: ["csp-violation"],
    buffered: true,
  },
);

observer.observe();

```

CSP leak includes nonce values but with a migration of needing to comply with the victims CSP to abuse it, however a data: URL allows for custom HTML which is a larger attack surface.

# Summary

Service workers allowing redirects to data: URLs.

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Timeline

### es...@chromium.org (2024-11-18)

Ben, do you still own Service Workers/fetch? If not, do you know who does? Thanks!

### ah...@google.com (2024-11-18)

deleted

### ca...@chromium.org (2024-11-18)

This reproduces for me in M129, setting found in

### pe...@google.com (2024-11-19)

Setting milestone because of s2 severity.

### pe...@google.com (2024-11-19)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### yy...@chromium.org (2024-11-20)

Response.redirect should be:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/response.idl;l=16;drc=6fee5a4abe42c99bfd2670c0e5d255ee630324f6

### yy...@chromium.org (2024-11-20)

For banned cases, people might see https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/blocked_scheme_navigation_throttle.cc;l=85;drc=dc43046192ba8877992169fd58c6cc0decf778f1 ?

### yy...@chromium.org (2024-11-20)

Looking at the data URL block mechanism ... filesystem scheme might also be blocked?
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/blocked_scheme_navigation_throttle.cc;l=96;drc=4bd1a7baff509ad8514cd2fe53b3814c228dba51

### yy...@chromium.org (2024-11-20)

As far as I understand from https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_throttle_runner.cc;l=194;drc=4bd1a7baff509ad8514cd2fe53b3814c228dba51,
Chrome blocks navigation to the data URL scheme if it is from the renderer initiated navigation.  However, it does not care if it is the browser initiated navigation.

### yy...@chromium.org (2024-11-20)

Hmm, as far as I checked with Chromium commit e453bbbd376ae99e63acbea6d590f08f769a38ff, I saw ERR_UNSAFE_REDIRECT, and cannot open the demo page.

### nd...@protonmail.com (2024-11-20)

The issue only affects chrome builds, it does not work with chromium by its self.

### yy...@chromium.org (2024-11-20)

133.0.6847.0 (Official Build) canary (arm64) is affected but #comment11 is not?

### nd...@protonmail.com (2024-11-20)

That's what was hard when trying to bisect it seems only official chrome builds have the problem.

### yy...@chromium.org (2024-11-20)

Re: #comment12
Thanks for the information.
Then, it sounds more like the configuration issue instead of Chromium issue?
Let me dig into more details.
Note that on Chromium, redirect to data URL scheme is rejected by https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=1140;drc=6420d743079b4d60da566a6d5978ee8983b212e6

### yy...@chromium.org (2024-11-20)

My best guess is that CHROMECAST_BUILD is set for this case.
https://source.chromium.org/chromium/chromium/src/+/main:content/public/common/url_utils.cc;l=88;drc=4bd1a7baff509ad8514cd2fe53b3814c228dba51 


### nd...@protonmail.com (2024-11-20)

Think so seems chrome specific, the chromium autoreloader may not work I think just had the service worker registered and got confused.

### nd...@protonmail.com (2024-11-20)

Looks like IsSafeRedirectTarget is also used in extensions/browser/api/web_request/web_request_proxying_url_loader_factory.cc may explain why extensions can do the same redirect attack.
Not sure why CHROMECAST_BUILD would be set when not on a chromecast maybe its for support but then universal allowing doesn't make sense.

### yy...@chromium.org (2024-11-21)

With the official build configuration (https://www.chromium.org/developers/gn-build-configuration/#official-chrome-build), I could reproduce the issue.
As far as I investigated, the root cause sounds like Extension code.

In #comment12, I pointed out that https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=1140;drc=6420d743079b4d60da566a6d5978ee8983b212e6 is not executed. I mean even if the URL is unsafe, the ERROR is not set.
The reason is not CHROMECAST_BUILD but bypass_redirect_checks_.  bypass_redirect_checks_ is true due to the following reason:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=1538;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34
bypass_redirect_checks is passed through like https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=1634;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34.
ContentBrowserClient::WillCreateURLLoaderFactory() should be a virtual function and we need to find the actual implementation.
The actual implementation should be https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=6662;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34
Here, if there is web_request_api and use proxy for the web request, then bypass_redirect_checks_ is set:
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=6686;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34

I mean WebRequestAPI::MaybeProxyURLLoaderFactory() returns true.
https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/web_request/web_request_api.cc;l=381;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34

### yy...@chromium.org (2024-11-21)

As far as I observed MayHaveProxies() returns false on Chromium build while the official build is not.
https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/web_request/web_request_api.cc;l=394;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34

Anyway, since the bypass redirect check decision is made in the extension code, let me delegate this to the extension team in case.

### me...@google.com (2024-11-27)

This is a duplicate of [bug 378361792](https://issues.chromium.org/issues/378361792) which is four days older than this, so I'm going to merge it there. There's a lot of information here though, so I'll carry over the assignee and the labels to that bug and add a note about this bug.

### nd...@protonmail.com (2024-11-27)

This issue was originally reported in  https://issues.chromium.org/40064165 is it still a dupe?

### me...@google.com (2024-11-27)

Thanks for pointing that out. [Comment #39](https://issues.chromium.org/issues/379337758#comment39) of [bug 40064165](https://issues.chromium.org/issues/40064165) indeed has the same PoC.

Reopening this and marking the other bug as a dupe.

### pe...@google.com (2024-12-05)

devlin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### rd...@chromium.org (2024-12-09)

Hmm... this is unusual.

In effect, we're bypassing the redirect checks in [NavigationUrlLoaderImpl](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=1138;drc=6420d743079b4d60da566a6d5978ee8983b212e6) if we [proxy the request for WebRequest](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=6685-6692;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34). This is *not* the right logic, since proxying the request for web request doesn't mean the request will be touched by extensions at all:

- If any extension uses the web request API, we'll proxy the request
- If extension telemetry is active, we'll proxy the request

We should instead only bypass redirect checks if an extension *really did* redirect the request, which is a per-request determination.

Beyond that, though, we must be doing something different here in service worker cases vs non-SW cases. ~Every user with a content filtering extension (like an ad blocker) would have their requests proxied through web request, but we don't bypass all redirect checks in all cases for those users. yyanagisawa@, do you know what's different in the service worker case?

cduvall@, it looks like you touched this code back in the day (network service and mojoification), can you shed some light on what's supposed to be happening here?

### cd...@chromium.org (2024-12-09)

It's been a few years since I looked at any of this code so not sure how much help I'll be, but I think this case is supposed to be handled by the check [here](https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/web_request/web_request_proxying_url_loader_factory.cc;l=1446;drc=616d60fca655937c2b730db94fd32d37ddff3bb5). If that check is not getting hit in this case, there may be something service worker-specific that is causing this to be bypassed.

### yy...@chromium.org (2024-12-12)

Since the judge is actually happens in NavigationURLLoader, which I believe is used for every navigation, I do not think this is specific to ServiceWorker.
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=1538;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34

When `WebRequestProxyingURLLoaderFactory::InProgressRequest::OnReceiveRedirect()` will be called?
https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/web_request/web_request_proxying_url_loader_factory.cc;l=460;drc=0e516eb08aa56163bfe649cebbba13da1fcf5f3c

As you can see in https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/web_request/web_request_api.cc;l=394;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34, if MayHavProxies() is true, the function should always return true.
I am not sure when the extension's functions are interecepted, but if `IsSafeRedirect()` (https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/web_request/web_request_proxying_url_loader_factory.cc;l=1446;drc=0e516eb08aa56163bfe649cebbba13da1fcf5f3c) is expected to be called, I assume `WebRequestProxyingURLLoaderFactory::InProgressRequest::OnReceiveRedirect()` must be called after the end of NavigationURLLoaderImpl::OnReceiveRedirect()?
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=1170;drc=0e516eb08aa56163bfe649cebbba13da1fcf5f3c

### pe...@google.com (2024-12-24)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### nd...@protonmail.com (2025-04-16)

Any progress with this or the related https://issuetracker.google.com/40064165
Maybe they should be merged.

### rd...@chromium.org (2025-05-23)

andreaorru@, mind adding this to your list?

### nd...@protonmail.com (2025-06-18)

I'm sure we are all wondering will the assignee [an...@chromium.org](mailto:an...@chromium.org) go back to [an...@google.com](mailto:an...@google.com) again personally really interested to see how this develops.

### an...@chromium.org (2025-06-18)

That's funny. =) I apologize for the noise, I'll be sticking to my @chromium.org account from here on.

I don't have an update on this yet, but I just finished a chunk of unrelated work and should have some spare cycles to look into it.

### an...@chromium.org (2025-06-27)

I was a bit confused at first when I read this thread.

If the official Chrome configuration had `CHROMECAST_BUILD` enabled, as was floated somewhere in this thread, then [this check](https://crsrc.org/c/content/browser/loader/navigation_url_loader_impl.cc;drc=0a85e65a7ce1238a95e62031a05b93bd11fbec0f;l=1257) would not be true, regardless of `bypass_redirect_checks_` (and regardless of extensions). Therefore, the bad redirect would not be blocked. As an aside, I think it's dubious to have `kDataScheme` listed as safe anywhere at all, and I'm surprised [this CL](https://crrev.com/c/1818460) didn't get more scrutiny.

If, as I suspect, `CHROMECAST_BUILD` is not enabled for Chrome/Chromium desktop, then the issue still presents itself if there's an extension that can proxy requests, as Devlin pointed out. I was able to verify this by compiling Chromium and installing e.g. uBlock Origin Lite, which was enough to reproduce the bug. So let's focus on this.

A possible solution is to add a flag inside [`UrlResponseHead`](https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/mojom/url_response_head.mojom;bpv=1;bpt=1;l=38?q=url_response_head.mojom&ss=chromium&gsn=URLResponseHead&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Dmojom%23network.mojom.URLResponseHead) to track whether a particular request was proxied. That flag can then be checked inside [`NavigationURLLoaderImpl::OnReceiveRedirect()`](https://crsrc.org/c/content/browser/loader/navigation_url_loader_impl.cc;drc=0a85e65a7ce1238a95e62031a05b93bd11fbec0f;l=1257) in lieu of `bypass_redirect_checks_`.

rdevlin.cronin@, yyanagisawa@, do you have any thoughts?

### nd...@protonmail.com (2025-06-27)

That <https://chromium-review.googlesource.com/c/chromium/src/+/1818460/2> patch got merged with the reason `Whoa. Okay for chromecast-only change...` on the bug <https://issuetracker.google.com/141260084> I'm still not using a chromecast.

### rd...@chromium.org (2025-06-30)

> A possible solution is to add a flag inside UrlResponseHead to track whether a particular request was proxied. That flag can then be checked inside NavigationURLLoaderImpl::OnReceiveRedirect() in lieu of bypass_redirect_checks_.

Hmm... I'm not quite sure I follow.  If we *just* use a new flag to tell whether a response was proxied and then use that in lieu of bypass_redirect_checks_, don't we have the same issue?  (We'll proxy requests in lots of situations, but that doesn't mean we should always bypass redirect checks.)

### an...@chromium.org (2025-06-30)

I meant whether a response was redirected, not just proxied. Apologies.

### rd...@chromium.org (2025-06-30)

Ah, gotcha.  Yeah, in that case, I think that's what we'd want.  Feel free to throw a CL together and send it out for review.  Thanks, Andrea!

### yy...@chromium.org (2025-07-01)

Re: #comment33
Sorry for the slow reply.
If my memory is correct, the issue happens only on the official build, and I assumed that there are default extensions installed for the official build.  That is why the Chromium is not affected without installing any extensions.  Upon my investigation in the past #comment15-19 and #comment27, CHROMECAST_BUILD should not be the reason that brought the difference.

Providing another check in NavigationURLLoaderImpl::OnReceiveRedirect() sounds reasonable to me.  Currently, the code does not provide any redirect checks for extensions.

### dx...@google.com (2025-07-10)

Project: chromium/src  

Branch:  main  

Author:  Andrea Orru [andreaorru@chromium.org](mailto:andreaorru@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6692491>

[Extensions] Determine whether to bypass redirect checks per request

---


Expand for full commit details
```
     
    This change introduces the BypassRedirectChecksPerRequest feature flag, 
    which is enabled by default. This flag allows redirect checks to be 
    bypassed only if the specific request was redirected by the extensions 
    layer. 
     
    Bug: 379337758 
    Change-Id: I995620efe045ca6eba6a02c3a64e91d18188af6b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6692491 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Commit-Queue: Andrea Orru <andreaorru@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1485110}

```

---

Files:

- M `chrome/browser/extensions/api/web_request/web_request_apitest.cc`
- A `chrome/test/data/service_worker/service_worker_data_redirect.js`
- A `chrome/test/data/service_worker/service_worker_setup_data_redirect.html`
- M `content/browser/loader/navigation_url_loader_impl.cc`
- M `content/public/common/content_features.cc`
- M `content/public/common/content_features.h`
- M `extensions/browser/api/web_request/web_request_proxying_url_loader_factory.cc`
- M `services/network/public/mojom/url_response_head.mojom`

---

Hash: 2b49489ea2cbc9b795dfdc847e9bc1aa9b9815f2  

Date: Thu Jul 10 18:31:11 2025


---

### sp...@google.com (2025-07-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
report of moderate impact web platform privilege escalation 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### nd...@protonmail.com (2025-07-22)

Thanks :)

### an...@chromium.org (2025-07-31)

Thank you for reporting :)

### ch...@google.com (2025-10-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of moderate impact web platform privilege escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/379337758)*
