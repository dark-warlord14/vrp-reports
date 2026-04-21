# ServiceWorkers in credentialless iframes could access long lived cookies

| Field | Value |
|-------|-------|
| **Issue ID** | [40063342](https://issues.chromium.org/issues/40063342) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>AnonymousIframe, Blink>ServiceWorker, Internals>Network>Cookies>PartitionedCookies, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2023-03-02 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description


ServiceWorkers in credentialless iframes could access long lived cookies


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

Starting from the following assumption I've tried to check if it's possible to bypass the restriction and access long-lived cookies from a `credentialless` iframe:
> "The `credentialless` attribute allows embedding third party iframes in a COEP: credentialless mode, i.e. the frame itself doesn't have cookies and all outgoing requests will be performed without credentials." 

While testing `serviceWorkers` I've discovered that if a `serverWorker` is created in a `credentialless` iframe, it is able to access long-lived cookies outside of the context of the `credentialless` iframe.

PoC:
1. Download the attached poc.zip
2. Extract poc.zip
3. Spawn terminal1 and use it to run `php -S 127.0.0.1:8000` inside the `one` folder
4. Spawn terminal2 and use it to run `php -S 127.0.0.1:8001` inside the `two` folder
5. Browse http://127.0.0.1:8000
6. Click "Set Cookie" to browse once http://127.0.0.1:8001/index.html and get a long-lived cookie set
7. Refresh http://127.0.0.1:8000 with the dev tools opened
8. Notice that a request is sent to http://127.0.0.1:8001/debug_cookie.php?js from the `credentialless` iframe which does contain the cookie `this_is_a_short_lived_cookie=1` which is set inside the iframe itself
9. Notice that a request is sent to http://127.0.0.1:8001/debug_cookie.php?sw from the `serverWorker` loaded inside the `credentialless` iframe which does contain the cookie `this_is_a_long_lived_cookie=1` which was set by http://127.0.0.1:8001/index.html



#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

A cross-origin page loaded inside a `credentialless` iframe could create a service worker and access long-lived cookies in the request and bypass the security boundary imposed by the `credentialless` flag.


---

### The cause


#### What version of Chrome have you found the security issue in?

110.0.5481.177 (Official Build) (arm64) 


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Other


#### How would you like to be publicly acknowledged for your report?

Abdel Adim `smaury` Oisfi of Shielder




## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 2.4 KB)
- [Screenshot 2023-03-03 at 9.23.42 AM.png](attachments/Screenshot 2023-03-03 at 9.23.42 AM.png) (image/png, 917.8 KB)
- [poc_new.zip](attachments/poc_new.zip) (application/octet-stream, 2.9 KB)

## Timeline

### ma...@gmail.com (2023-03-02)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2023-03-02)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-03-03)

I can't reproduce this. When I refresh the page in step 7 I see the request sent initiated by the service worker but not a request initiated by the iframe (see screenshot). Are there any further details you can provide for how to reproduce? Thanks.

### ma...@gmail.com (2023-03-03)

Sorry for that - I've uploaded an incomplete PoC :(
Here you go the final version where you have everything matching the steps I shared previously.

This is the diff FYI:
```
diff -r poc/two/simple.html poc_new/two/simple.html
19a20
>       fetch("/debug_cookie.php?js")
diff -r poc/two/sw.js poc_new/two/sw.js
2c2
<   fetch("/debug_cookie.php")
---
>   fetch("/debug_cookie.php?sw")
```

### ma...@gmail.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2023-03-06)

Thanks for the updated repro. clamy@, arthursonzogni@, could you please take a look and see if this is working as intended or not (or re-route appropriately)?

[Monorail components: Blink>SecurityFeature]

### es...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-06)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@google.com (2023-03-06)

Thanks for reporting this!
I won't have time to verify the bug today. I will have tomorrow.

We should check if the ServiceWorker can communicate with the credentialless iframe.
We rely on this test:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/html/anonymous-iframe/serviceworker-partitioning.tentative.https.window.js;bpv=1

### ad...@google.com (2023-03-06)

(I am a bot: this is an auto-cc on a security bug)

### ar...@google.com (2023-03-08)

I confirm the bug. Here is a live version:
https://shocking-abalone-soap.glitch.me/

+ AntonioSartori FYI.

### ar...@google.com (2023-03-08)

My understanding is that we do have "partitioned worker", given the test:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/html/anonymous-iframe/serviceworker-partitioning.tentative.https.window.js;bpv=0

That is to say, the iframe credentialless is talking to a dedicated service worker. The problem is that the ServiceWorker itself is using the general cookie partition.

In term of security impact: it bypasses the iframe credentialless protection for website using service worker. However Chrome does also enforce SiteIsolation inside cross-origin-isolated page on top of it, so you can't exfiltrate the data via Spectre anyway. So there should be no real security impact.

### ti...@chromium.org (2023-03-08)

> However Chrome does also enforce SiteIsolation inside cross-origin-isolated page on top of it, so you can't exfiltrate the data via Spectre anyway. So there should be no real security impact.

Is that always the case, even on low-end Android devices where we are severely memory-constrained?

### ar...@chromium.org (2023-03-08)

> Is that always the case, even on low-end Android devices where we are severely memory-constrained?

It is unclear to me, because the process selection is of considerable size.

My understanding is that:

1. Independently of the platform, the process will be marked as not suitable if it wasn't configured with crossOriginIsolation here:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_process_host_impl.cc;l=4315-4321;drc=bec0ef46974cd9a6bc0f1f1ae34baa11913f77af

2. In the event of no suitable process, we call RenderProcessHost::ShouldTryToUseExistingProcessHost(). Android has "unlimited" processes: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_process_host_impl.cc;l=1374?q=renderprocesshost%20selection&ss=chromium%2Fchromium%2Fsrc
so, it will always return false.
(The OS will start to kill some under memory pressure)

3. Whatever happens, we double-check the process is always "suitable" in case of reuse: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_process_host_impl.cc;l=4643;drc=bec0ef46974cd9a6bc0f1f1ae34baa11913f77af

4. Then we immediately goes to creating a new process:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_process_host_impl.cc;l=4646-4657;drc=bec0ef46974cd9a6bc0f1f1ae34baa11913f77af;bpv=1;bpt=1


So, I don't see any code allowing reusing an unsuitable process.

### ti...@chromium.org (2023-03-08)

That makes sense, thanks for digging. +creis@ and +alexmos@ to clear up any remaining uncertainty.

### cr...@chromium.org (2023-03-08)

titouan@ is correct that not all Android devices use Site Isolation, and even Android devices with sufficient RAM do not have full Site Isolation.  That means a "suitable" process (in terms of https://crbug.com/chromium/1420885#c16) may include cross-site pages in those cases.

For the purposes of this bug, I think that means:

1) There's not much security impact on desktop platforms, where full Site Isolation is enabled.  We should still prevent ServiceWorkers of credentialless iframes from accessing long-lived cookies, but a third-party iframe in a COI-enabled page won't live in the same process, and can't use something like Spectre to leak the cookies / data.

2) On 2GB+ Android devices, we try to use Site Isolation in cases it matters most (https://security.googleblog.com/2021/07/protecting-more-with-site-isolation.html), but not all sites are isolated.  A COI-enabled page could use this bug to access cookies of a non-isolated site in an iframe.  That seems important to fix.

3) On <2GB Android devices, Site Isolation is not enabled and this bug looks like it matters for all sites.

[Monorail components: Internals>Sandbox>SiteIsolation]

### ti...@chromium.org (2023-03-08)

Thanks for clarifying! As a security sheriff, how would you rate the resulting severity of this bug?

### [Deleted User] (2023-03-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2023-03-08)

https://crbug.com/chromium/1420885#c19: I'm not a security sheriff, but I would consider this a partially-mitigated COI credentialless bypass (since it only works in the case that Site Isolation doesn't apply).

Do you know how COI credentialless bypasses are usually rated?  (They are different from Site Isolation bypasses, which would be High.)  If they're normally Medium, for example, then going down one level to Low seems like it would be right.

### ma...@gmail.com (2023-03-09)

Thanks everyone to helping clarifying the impact!

So my understanding here is that we have two different scenarios/impacts:
1. From the `credentialless` perspective we have a bypass of the security feature as a `credentialless` iframe could access the long-lived cookies if it implements a `ServiceWorker`. This is true even though COEP is not present and breaks this assumption of `credentialless` iframes: "IFrame credentialless provides a mechanism for developers to load third-party resources in <iframe>s using a new, ephemeral context. It doesn't have access to its regular origin's network, cookies, and storage data." - https://developer.mozilla.org/en-US/docs/Web/Security/IFrame_credentialless
2. From a `Site Isolation` perspective we might have some bypasses based on specific factors which are very well highlighted by creis in https://bugs.chromium.org/p/chromium/issues/detail?id=1420885#c18

Does it make sense to you?

If yes - we could assume 1 is a bypass of a security boundary and 2 is just a partial bypass (as it depends on various factors), so maybe 1 should be High and 2 should be Medium or even Low?

### ti...@chromium.org (2023-03-09)

> From the `credentialless` perspective we have a bypass of the security feature as a `credentialless` iframe

Exactly.

> From a `Site Isolation` perspective we might have some bypasses

I don't think these are bypasses, but rather known limitations with Site Isolation, which is too expensive to enable on all platforms and devices. These limitations mean that the credentialless bypass reported here is only partially mitigated by Site Isolation - not fully, like https://crbug.com/chromium/1420885#c14 suggested.

> I'm not a security sheriff

Sorry, my mistake! Thanks for answering my question anyway :)

> Do you know how COI credentialless bypasses are usually rated?

I think this might be the first such bug since we shipped (arthursonzogni@, correct me if I'm wrong): https://bugs.chromium.org/p/chromium/issues/list?q=component%3ABlink%3ESecurityFeature%3EAnonymousIframe%20Type%3DBug-Security&can=1

So we get to decide the severity here and now!

Guidelines are here: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md

> High severity vulnerabilities allow an attacker to execute code in the context of, or otherwise impersonate other origins or read cross-origin data.

> Medium severity bugs allow attackers to read or modify limited amounts of information, or are not harmful on their own but potentially harmful when combined with other bugs. This includes information leaks that could be useful in potential memory corruption exploits, or exposure of sensitive user information that an attacker can exfiltrate.

In a vacuum, I think credentialless bypasses qualify as High severity. A COI page can embed some supposedly-credentialless/actually-credentialled cross-origin resources and then read their contents with Spectre. This maps to "read cross-origin data".

Now, there are several caveats in this case:

1. The SharedArrayBuffer deprecation trial on desktop is still ongoing, so an attacker need not use credentialless on those platforms
2. In any case, Site Isolation prevents the attack on desktop and some Android devices
3. The victim page must use a service worker (and credentialled data must be passed back, but that seems very likely: the SW proxies requests)

> going down one level [...] seems like it would be right

I agree that since it's partially mitigated, and the victim must use a service worker, we can downgrade it one level.

That lands on a Medium severity. Does that sound right?

[Monorail components: -Blink>SecurityFeature Blink>SecurityFeature>AnonymousIframe Blink>ServiceWorker]

### gi...@appspot.gserviceaccount.com (2023-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/472d475574faf7bc12cbf82396708c99d2157b7b

commit 472d475574faf7bc12cbf82396708c99d2157b7b
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Fri Mar 10 17:17:54 2023

Iframe credentialless: Cookie & worker regression test

Test that a request emitted from worker spawned from a
credentialless iframe does not send global cookies.

Bug: 1420885
Change-Id: I0da2d83606ba164e2986e9eefe4ac5ae45507197
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4328279
Reviewed-by: Titouan Rigoudy <titouan@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1115760}

[add] https://crrev.com/472d475574faf7bc12cbf82396708c99d2157b7b/third_party/blink/web_tests/external/wpt/html/anonymous-iframe/worker-cookies.tentative.https.window.js
[add] https://crrev.com/472d475574faf7bc12cbf82396708c99d2157b7b/third_party/blink/web_tests/external/wpt/html/anonymous-iframe/worker-cookies.tentative.https.window_worker=service_worker-expected.txt


### ti...@chromium.org (2023-03-10)

Thanks for landing the test Arthur. IIRC you were saying that the service worker seems to be correctly partitioned, but it is somehow reading unpartitioned cookies?

### ar...@google.com (2023-03-13)

> Thanks for landing the test Arthur. IIRC you were saying that the service worker seems to be correctly partitioned,

Yes, given test: third_party/blink/web_tests/external/wpt/html/anonymous-iframe/serviceworker-partitioning.tentative.https.window.js

> but it is somehow reading unpartitioned cookies?

Yes, given test:
third_party/blink/web_tests/external/wpt/html/anonymous-iframe/worker-cookies.tentative.https.window_worker=service_worker-expected.txt
SharedWorker and DedicatedWorkers seems fine.

### ma...@gmail.com (2023-03-13)

Quick question - maybe it's worth raising to Pri-1 to match the Severity?

### ar...@chromium.org (2023-03-14)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-03-15)

Sending this over to wanderview@ for triage, as this seems to reveal a bug in the partitioned serviceworker implementation.

### wa...@chromium.org (2023-03-15)

How do credentialless iframes request the partitioned cookie jar from the network stack code?

In service workers we have the storage key which includes the appropriate nonce.  In terms of storage partitioning this is primarily used to partition the service worker database of registrations.  I don't see comments suggesting that it is broken here.

We are also attempting to populate the NIK (or whatever it's called these days) appropriately, but perhaps we are missing something.  I believe this would ensure that site-for-cookies is set properly.  But it sounds like the issue here is with something other than site-for-cookies?

In particular, we only really know the storage key has a nonce.  I'm not sure if this looks the same as a sandboxed iframe with an opaque origin or if we can distinguish a credentialless iframe.  So if there is some kind of special logic required for credentialless we might need some additional plumbing.

Happy to help more, but routing this back for questions.

### ti...@chromium.org (2023-03-16)

> How do credentialless iframes request the partitioned cookie jar from the network stack code?

I believe they use a nonce which is plumbed into the relevant keys (see 10. in the design doc [1]), including the storage key.

> We are also attempting to populate the NIK (or whatever it's called these days) appropriately, but perhaps we are missing something.  I believe this would ensure that site-for-cookies is set properly.  But it sounds like the issue here is with something other than site-for-cookies?

Not sure if `net::CookiePartitionKey` is derived automatically from the NIK, but in my (inexperienced) eyes, it sounds like the cookie partition key is wrong: even though the service worker is partitioned (in the database, per the first test in https://crbug.com/chromium/1420885#c26), it seems to have access to the unpartitioned cookie jar.

> In particular, we only really know the storage key has a nonce.  I'm not sure if this looks the same as a sandboxed iframe with an opaque origin or if we can distinguish a credentialless iframe.  So if there is some kind of special logic required for credentialless we might need some additional plumbing.

I think the nonce is all you need - credentialless documents set it, and AFAICT share that logic with e.g. fenced frames.

Arthur, please correct me if I'm wrong!

[1] https://docs.google.com/document/d/1poI75BaQ9aqcMGJn_K01-QHsQQbEOwRWvg3Af4VWTmY/edit#heading=h.e14quei5uc0

### wa...@chromium.org (2023-03-16)

Looks like we don't set the top-level site on the NIK now?

https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_host.cc;l=151;drc=425ab488f26e70965a5109675a57ef38e504d344

cc'ing awillia who has been active on https://crbug.com/chromium/1147281.

### aw...@chromium.org (2023-03-17)

[Empty comment from Monorail migration]

### mm...@chromium.org (2023-03-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2023-03-19)

I investigated whether the code from https://crbug.com/chromium/1420885#c32 could be the issue, but it doesn't appear to be. Thinking about what partitions cookies, from talking with mmenke@ about this, SiteForCookies is used for SameSite=Strict cookies and initiator is used for SameSite=Lax cookies. From a quick look it doesn't seem like the PoC uses SameSite=Strict cookies, so maybe the initiator is being used in a way that doesn't correctly factor in whether a credentialless iframe is being used?

### wa...@chromium.org (2023-03-20)

[Empty comment from Monorail migration]

### mi...@chromium.org (2023-03-20)

[Empty comment from Monorail migration]

### bi...@chromium.org (2023-03-20)

To clarify some cookie concepts:

Samesite is orthogonal to partitioning, it deals with when to make cookies accessible in cross-site contexts. There can appear to be some behavioral overlaps (for example, a SameSite=Strict will never be shown in a 3rd party iframe which could make it look like it's partitioned to its origin) but SameSite and partitioning are different. 

The SiteForCookies is used as one piece of information to determine if SameSite=Strict or SameSite=Lax cookies should be accessible. When the SiteForCookies is null, neither Lax nor Strict cookies are accessible. But, SameSite=none cookies are accessible.

As for actually partitioning cookies, by default cookies are "partitioned" by the domain setting them. By default I mean any simple cookie: `Set-Cookie: foo=bar`. 
Any cookie set by the same domain is in the same partition. This has been the case for many years. This is slightly muddied by the `Domain` attribute, but it's "correct enough" to say they're partitioned by their domain.

Recently however we added a new concept of partitioning which uses the partitioned attribute: `Set-Cookie: foo2=bar2; partitioned; ...(some other attributes)...`
This opt-in attribute will partition the cookie by its domain as well as the top level site setting it (or nonce for anonymous frames). These partitioned cookies live alongside the "normal" cookies and it's possible for a given site to have both simultaneously.


### ti...@chromium.org (2023-03-21)

Thanks for the explanation! How can a context be prevented from accessing unpartitioned cookies, then?

### aw...@chromium.org (2023-03-21)

The tests show that dedicated workers and shared workers created from credentialless iframes don't have this problem - is there already a mechanism to restrict cookies for those contexts?

Anyway, assigning back to Arthur for further investigation.

### ti...@chromium.org (2023-03-21)

AIUI, credentialless iframes' nonce shared an implementation with fenced frames. If so, then this suggests that service workers created by fenced frames might also have access to unpartitioned cookies? @shivanisha, do you have any tests for this by any chance?

### bi...@chromium.org (2023-03-21)

> How can a context be prevented from accessing unpartitioned cookies, then?

I'm curious how credentialless iframes' cookies are handled in a simple embedding scenerio now (i.e.: Without service workers). Looking at https://developer.mozilla.org/en-US/docs/Web/Security/IFrame_credentialless I don't see any requirement for cookies to be marked with the `partitioned` attribute so unless that's happening behind the scenes somewhere I'm not sure how empheral cookies are being set at all.

Can someone from the credentialless iframe team shed some light?

### ti...@chromium.org (2023-03-21)

I believe setting a nonce in `net::CookiePartitionKey` restricts the context to only partitioned cookies with a matching nonce [1]. This again suggests that the `CookiePartitionKey` for service workers created from credentialless iframes or fenced frames is missing the nonce?

[1] https://source.chromium.org/chromium/chromium/src/+/main:net/cookies/cookie_monster.cc;l=133-148;drc=cb95e30fa939a18bc0845b57b0946a102b86cf9d

### bi...@chromium.org (2023-03-21)

Right, but the CookiePartitionKey requires the (opt-in only) `partitioned` attribute. So if a credentialless iframe sets a simple `foo=bar` cookie I don't think it'll be a partitioned cookie?

 dylancutler@, am I understanding CHIPs correctly?

### dy...@google.com (2023-03-21)

No the credentialless iframe should be using a nonced partitioned key, so it makes sense that a simple "foo=bar" cookie is partitioned.

The interaction between CHIPS and service workers is still WIP, but given this bug I think I should prioritize getting that wrapped up and tested. Thanks for pointing this out to me, Steven.

### bi...@chromium.org (2023-03-21)

Ah thanks, so it sounds like for credentialless iframes all cookies are partitioned by default. That answers my question.

### ti...@chromium.org (2023-03-22)

Thanks Steven for cc-ing Dylan, and thanks Dylan for confirming. Do you have a bug tracking work to integrate SWs with partitioned cookies? Otherwise, would you be willing to take a stab at this bug?

[Monorail components: Internals>Network>Cookies>PartitionedCookies]

### dy...@google.com (2023-03-26)

Yes, I just created https://crbug.com/1427879 to track this issue. Until storage partitioning ships partitioned workers, this bug is, unfortunately, WAI. Once partitioned workers ship and we close crbug/1427879 then this bug will be fixed as a result.

### ti...@chromium.org (2023-03-30)

[Empty comment from Monorail migration]

### dx...@google.com (2023-04-03)

[Empty comment from Monorail migration]

### dx...@google.com (2023-04-03)

it's late for M111, given it's still block, 114?

### ti...@chromium.org (2023-04-06)

I'm waiting for news from dylancutler@ on crbug.com/1427879.

### [Deleted User] (2023-04-20)

titouan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dy...@google.com (2023-04-20)

https://crbug.com/1427879 is fixed, so this bug *should* be fixed when storage partitioning ships in 113.

Once that is the case, service workers will be partitioned on StorageKey, which includes the nonce from the credentialless frame context. This should prevent workers registered by credentiallless, anonymous, or fenced frames from accessing unpartitioned cookies.

### dy...@google.com (2023-04-20)

Actually, one minor correction, the code patching crbug.com/1427879 will not go to stable until 114. So this bug should be patched then :)

### ar...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-04-25)

Thanks Dylan for the update!

I'm confused, though, since it seems that the test Arthur wrote is not fixed [1]. Indeed, your WPT CL [2] explicitly calls out that it does not test the same thing.

Is this bug really fixed by your changes?

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/html/anonymous-iframe/worker-cookies.tentative.https.window_worker%3Dservice_worker-expected.txt;drc=472d475574faf7bc12cbf82396708c99d2157b7b

### ti...@chromium.org (2023-04-25)

[2] https://crrev.com/c/3674179

### ti...@chromium.org (2023-05-09)

Status here is that Dylan is making progress on fixing SW use of unpartitioned cookies in crbug.com/1427879.

### ti...@chromium.org (2023-05-09)

[Empty comment from Monorail migration]

### dy...@google.com (2023-05-22)

This should be fixed now that https://crbug.com/1427879 is closed.

### ti...@chromium.org (2023-05-23)

Thanks for working on this Dylan! I'm still confused, because even though I see you've improved things, the test that Arthur wrote still fails [1]. Do you know why?

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/html/anonymous-iframe/worker-cookies.tentative.https.window_worker%3Dservice_worker-expected.txt;drc=472d475574faf7bc12cbf82396708c99d2157b7b

### dy...@google.com (2023-05-23)

That test passes on tip of tree now. The test expectations you linked are from a previous (now outdated) commit.

### ti...@chromium.org (2023-05-23)

Oh, indeed, my bad. I got confused by the UI showing me I was on `main`, when I was not! Thanks for confirming!

### [Deleted User] (2023-05-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations, smaury! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### ma...@gmail.com (2023-06-09)

Thanks for the reward amyressler@!
Just a quick question in case you want to reassess: on top of the very specific vulnerability this report also led to the discovery that the whole CHIPS implementation was partial as it was not considering any of the workers. This means that before the fixes when a worker was in use the the cookies were not partitioned with obvious impacts on the Site Isolation. I fell like that based on this and the fact that on average Site Isolation related bugs are paid 3.000$+ (I did a very quick search on the disclosed ones), maybe this one needs a re-assessment.

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-05)

Gentle nudge :)

### am...@chromium.org (2023-07-05)

Thank you for the nudge, smaury! We did re-evaluate this issue a few weeks ago, but it appears I did not provide that update here. Please accept my sincere apologies for the delay! 

The VRP Panel decided this reward amount was sufficient for this issue. As site isolation bypasses go, most that you point to are site isolation bypasses that are mitigated. This issue is more of one that is most impactful on devices that do not employ site isolation, so this would not be considered a site isolation bypass for the most part. In the aspects that this would be considered a site isolation bypass of a kind, it is fairly mitigated. 

In terms of assessment, based on mitigation (partially-mitigated COI credital-less bypass) and impact, this reward amount was considered appropriate for this issue. 

### ma...@gmail.com (2023-07-06)

Thanks for the update and for sharing the rationale behind the decision!

### [Deleted User] (2023-08-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1420885?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>AnonymousIframe, Blink>ServiceWorker, Internals>Network>Cookies>PartitionedCookies, Internals>Sandbox>SiteIsolation]
[Monorail blocked-on: crbug.com/chromium/1427879]
[Monorail mergedwith: crbug.com/chromium/1439267]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063342)*
