# Service Worker Navigation bypass LNA checks for localhost

| Field | Value |
|-------|-------|
| **Issue ID** | [454162508](https://issues.chromium.org/issues/454162508) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>LocalNetworkAccess |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | hc...@chromium.org |
| **Created** | 2025-10-22 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
Chromium has a Local Network Access feature that displays a PNA bubble to alert users when a webpage attempts to access private addresses. However, this security restriction can be bypassed by using the Service Worker navigation feature.

VERSION
Chromium	143.0.7469.0 (Developer Build) (64-bit) 
OS	Windows 11 Version 25H2 (Build 26200.6584)

REPRODUCTION CASE
1. put the html/js into a online webserver https://domainxxx.com/
2. visit https://lna-testing.notyetsecure.com/ , select "Subframe loading" to load the url(https://xxxxx.com/poc.html) in frame

Result: The iframe navitaor to the http://locahost/xxxxx

The Service Worker Navigation function will bypass the PNA feature.

PS: If you change the URL redirect method in HTML to location.href = "http://localhost/xxxx", then the Chrome browser will pop up the PNA permission bubble.
PS: Firefox can block the request and pop up the PNA permission bubble.



## Attachments

- [poc.html](attachments/poc.html) (text/html, 450 B)
- [service_worker.js](attachments/service_worker.js) (text/javascript, 701 B)
- [414162508-browser-test-repro.json](attachments/414162508-browser-test-repro.json) (application/json, 343.8 KB)

## Timeline

### xi...@chromium.org (2025-10-23)

Thanks for the report. Seems related to https://crbug.com/40063868 and https://crbug.com/404887282. +cthomp, since you implemented the permission, could you take a look? Thanks!

### ch...@google.com (2025-10-23)

Setting milestone because of s2 severity.

### ch...@google.com (2025-10-23)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-10-24)

This V8 bug has been marked as a release blocker. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ct...@chromium.org (2025-10-24)

Thanks for the report (and also thanks for testing against Firefox too)! It looks like in ServiceWorker's WindowClient.navigate() [1](https://w3c.github.io/ServiceWorker/#dom-windowclient-navigate) we aren't tracking the necessary information to apply the LNA checks. We'll work on adding the necessary enforcement.

(Not sure why the bot thinks this is a V8 bug or a release blocker though.)

### hc...@chromium.org (2025-10-24)

I believe I reproed locally with a browser test, slightly modified due to browser test restrictions. @ct...@chromium.org, setup:

- a.com, b.com, c.com all resolve to 127.0.0.1
- `LocalNetworkAccessAllowedForURLs policy set to "\*"
- a.com (CSP treat-as-public) iframes b.com (also CSP treat-as-public, but no permission policy delegation)
- b.com starts service worker, uses WindowClient.navigate to navigate to c.com

Test passes, when test should fail. Test fails if instead we do a fetch() in the service worker of c.com.

Netlog (attached) indicates that there's no `client_security_state` for the `navigate()` call, so we're losing that somehow in the code.

So far I've traced to [`ServiceWorkerVersion::NavigateClient`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_version.cc;drc=8900162810d457b64286ce653cb61bc2009c5068;bpv=1;bpt=1;l=1887?gsn=NavigateClient&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Dc%252B%252B%3Fpath%3Dcontent%2Fbrowser%2Fservice_worker%2Fservice_worker_version.cc%233jtSmGnQ7k8LiZ5iC_on78vynswPdWofCtmvMF7Zh6c), but I haven't gotten further yet. I'm also not sure why fetch() works but `WindowClient.navigate` fails.

### hc...@chromium.org (2025-10-24)

oops attaching netlog

### hc...@chromium.org (2025-10-24)

more digging:

content/browser/service\_worker/service\_worker\_client\_utils.cc, `NavigateClient` has this [code](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_client_utils.cc;l=599-612;drc=8900162810d457b64286ce653cb61bc2009c5068):

```
  // Service workers don't have documents, so it's ok to use nullopt for
  // `initiator_base_url` in the following call.
  navigator.RequestOpenURL(
      rfhi, url, nullptr /* initiator_frame_token */,
      ChildProcessHost::kInvalidUniqueID /* initiator_process_id */,
      url::Origin::Create(script_url), /* initiator_base_url= */ std::nullopt,
      nullptr /* post_body */, std::string() /* extra_headers */,
      Referrer::SanitizeForRequest(
          url, Referrer(script_url, network::mojom::ReferrerPolicy::kDefault)),
      WindowOpenDisposition::CURRENT_TAB,
      false /* should_replace_current_entry */, false /* user_gesture */,
      blink::mojom::TriggeringEventInfo::kUnknown,
      std::string() /* href_translate */, nullptr /* blob_url_loader_factory */,
      std::nullopt, false /* has_rel_opener */);

```

specifically, there's no information about the initiator passed in to the navigator, which is a problem because when we get to the `NavigationRequest`, it builds the client state off of the `policy_container_builder_` ([NavigationRequest::BuildClientSecurityStateForNavigationFetch()](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;drc=8900162810d457b64286ce653cb61bc2009c5068;bpv=1;bpt=1;l=9998?gsn=BuildClientSecurityStateForNavigationFetch&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Dc%252B%252B%3Fpath%3Dcontent%2Fbrowser%2Frenderer_host%2Fnavigation_request.cc%23-GY5j1oEIM4jcAnuwqPLuewiUrWaL1EWIcDqKNs2aVw)), and the `policy_container_builder_` gets built off of the initiator information ([NavigationRequest constructor](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=1811-1815;drc=8900162810d457b64286ce653cb61bc2009c5068), [NavigationPolicyContainer constructor](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_policy_container_builder.h;l=49-67;drc=8900162810d457b64286ce653cb61bc2009c5068)).

What's not clear to me is why we do get the client security state passed through if instead of `WindowClient` a `fetch()` call is made (I haven't tested the `location.href` method mentioned in the report yet).

### hc...@chromium.org (2025-10-24)

@yy...@chromium.org, @si...@chromium.org

Wondering if you have any thoughts on if I'm going down the right path or how to possibly fix this bug? I notice that there is a `content/browser/service_worker/service_worker_fetch_dispatcher.h` that I'm guessing does something different which is why `fetch()` calls in service workers enforce LNA requests, but I'm not sure how that happens or if that's something we can replicate here.

### yy...@chromium.org (2025-10-27)

Re: [#comment10](https://issues.chromium.org/issues/454162508#comment10)
Your analysis in [#comment9](https://issues.chromium.org/issues/454162508#comment9) pinpoints the exact implementation flaw I suspected. The fact that `initiator_base_url` is explicitly set to `std::nullopt` when calling `navigator.RequestOpenURL` is the crux of the problem. At the same time, that was likely an understandable choice when [the CL](https://chromium-review.googlesource.com/c/chromium/src/+/4026883/33/content/browser/service_worker/service_worker_client_utils.cc) was implemented. The concept of an "initiator origin" might not be clearly defined in the HTML standard for navigations triggered via `MessagePort.postMessage()`.

Given that ambiguity, I would argue the problem is not the `std::nullopt` itself, but rather the "default-allowed" behavior (the 'fail-open') that results from it. We are missing a policy for how to handle this unknown initiator state. The fix might be to explicitly mark this `nullopt` case as untrusted and prohibit LNA by default.

By the way, your suspicion about why `fetch()` is treated differently sounds reasonable. This is likely because `fetch()` is often called from within ServiceWorker fetch handlers (i.e., `onfetch`). Those handlers intercept main resource and subresource loads, which should have a clear initiator origin.

What do you think?

### hc...@google.com (2025-10-27)

> The concept of an "initiator origin" might not be clearly defined in the HTML standard for navigations triggered via MessagePort.postMessage().

Can you say more about this? I'm not sure what `MessagePort.postMessage()` is; does this mean the hole is more wide-ranging than just the `WindowClient.navigate()` call?

> Given that ambiguity, I would argue the problem is not the `std::nullopt` itself, but rather the "default-allowed" behavior (the 'fail-open') that results from it. We are missing a policy for how to handle this unknown initiator state. The fix might be to explicitly mark this nullopt case as untrusted and prohibit LNA by default.

Doesn't the "unknown initiator" case encompass the initial navigation (e.g. if someone types in a URL in the omnibox)? If they type in a localhost address directly, that's not something that we'd want blocked.

> By the way, your suspicion about why `fetch()` is treated differently sounds reasonable. This is likely because `fetch()` is often called from within ServiceWorker fetch handlers (i.e., onfetch). Those handlers intercept main resource and subresource loads, which should have a clear initiator origin.

Is there any reason why `WindowClient.navigate` couldn't also have a clear initiator origin passed into [`NavigateClient`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_client_utils.h;l=66-73;drc=b8e124eea4aa2a53a8ff0dfa51ba30178916f559) in the same way that the initiator origin is specified for the `fetch()` calls? (I also couldn't find the code that set the initiator origin for the `fetch()` calls, could you point out where that is?)

### yy...@chromium.org (2025-10-28)

I may misunderstand but the LNA is checked for the initiator origin, and you need the initiator origin to grant/deny the request.

> Can you say more about this? I'm not sure what MessagePort.postMessage() is; does this mean the hole is more wide-ranging than just the WindowClient.navigate() call?

As far as I understand the scenario, LNA check bypass looks happen in this way:

1. navigate to an attack page, which registers a ServiceWorker.
2. the page send a post message to the service worker.
3. the service worker's message handler navigates the client sending the request to the localhost.
4. the victim client navigates to the localhost.

The `Messageport.postMessage()` I meant was Step 2.
I meant how it is called might matter. However, I feel I misunderstood things.
According to <https://wicg.github.io/local-network-access/#integration-with-workers>, at least script URL's origin should be treated as the origin used for the LNA check. I need further investigation on if we need yet another parameter or passing the script URL's origin.

> Doesn't the "unknown initiator" case encompass the initial navigation (e.g. if someone types in a URL in the omnibox)? If they type in a localhost address directly, that's not something that we'd want blocked.

That is true. We may want the way to let the callee know if we expect deny by default or allow by default.

> Is there any reason why WindowClient.navigate couldn't also have a clear initiator origin passed into NavigateClient in the same way that the initiator origin is specified for the fetch() calls? (I also couldn't find the code that set the initiator origin for the fetch() calls, could you point out where that is?)

I suppose it is because nobody considered the case and just not standardized yet. So do implementation.

Let me see how `fetch()` is treated...I can be wrong but:
Fetch might be:
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/fetch_request_data.cc;l=173;drc=c96a878b1cb45f60aac2285ffbdbd6b53dc92415>

For a request coming from ServiceWorker fetch event, it might actually come from the request:
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc;l=1588-1590;drc=c96a878b1cb45f60aac2285ffbdbd6b53dc92415>

For a request made inside the ServiceWorker, I suppose it execution context's origin:
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/request.cc;l=150;drc=c96a878b1cb45f60aac2285ffbdbd6b53dc92415>

### ct...@chromium.org (2025-10-30)

From a read of the spec, it seems like the intention was to restrict this to same-origin navigations? That would avoid the bypass entirely. However, since this has shipped and doesn't actually enforce same-origin (the promise will return null but the navigation will still occur -- e.g., the WPT for WindowClient.navigate() only checks the promise value not for the navigation side effect <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/service-workers/service-worker/windowclient-navigate.https.html>), adding this restriction now is probably a web-visible change that could break existing use cases :/

We're discussing internally what the best way to add the necessary security state here to at least allow LNA checks to work correctly.

### yy...@chromium.org (2025-10-31)

> adding this restriction now is probably a web-visible change that could break existing use cases

I think so.
We might need the measurement and PSA or I2S at least.



### ch...@google.com (2025-11-14)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-29)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-14)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-29)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-13)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ct...@chromium.org (2026-01-14)

We discussed this some within my team and our consensus was that good next steps would be: (1) check if other browsers allow cross-origin Navigate(), and (2) add metrics for how often this is used. This will allow us to determine if it's feasible to deprecate and remove this entirely, or if we need to do a more targeted LNA-specific fix.

### ch...@google.com (2026-01-29)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### hc...@chromium.org (2026-02-09)

@yy...@chromium.org

after some false starts, I think this can be fixed by having the service worker window client navigation code actually specify the initiator. Specifically, this is a small change to service\_worker\_client\_utils.cc's [navigator.RequestOpenURL call](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_client_utils.cc;l=601-603?q=content%2Fbrowser%2Fservice_worker%2Fservice_worker_client_utils.cc) to be:

```
...
  navigator.RequestOpenURL(
      rfhi, url, &(rfhi->GetFrameToken()) /* initiator_frame_token */,
      rfhi->GetProcess()->GetDeprecatedID() /* initiator_process_id */,
      url::Origin::Create(script_url), /* initiator_base_url= */ std::nullopt,
...

```

(we don't need to pass in `initiator_base_url` as per comments in [navigation\_params.mojom](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/navigation/navigation_params.mojom;l=228-236?q=initiator_base_url%20f:mojom%20-f:out))

This essentially sets the initiator of the WindowClient.navigateTo navigation to the window itself, which @ct...@chromium.org and I believe is safe since the windowclient's origin is by spec the same as the service worker.

The only possible issue here would be if the service worker JS were installed when the origin had one IP Address space, and at the time of the windowClient.navigateTo call the ip address space of the origin is something else. We think this isn't an issue because:

- if WindowClient is a main frame, I think we don't care that much as "DNS rebinding a main frame" is just DNS changing, and main frame navigations aren't in scope anyway for LNA.
- if WindowClient is a subframe. This is the example in the POC of using WindowClient.navigate() to do a sneaky LNA request. But if WindowClient is actually more private than the SW here, it would be blocked during subframe nav checks. So the only case that matter is WindowClient is less private than SW, in which case using the windowclient as initiator would be more secure, not less.
- doing it this way is (roughly) equivalent to the SW postMessage-ing the WindowClient and some logic in the WindowClient triggering a navigation

Is there anything we're missing here?

### yy...@chromium.org (2026-02-10)

The change sounds reasonable security enforcement, but there can be changes involved.

The change should bring large behavior change.  I suggest you to add a metrics UMA or UseCount to ensure the affected area, and send I2S.
Additional permission checks introduced by this change may need to be written in the SW spec.

Passing an invalid route looks started to be passed since https://chromium-review.googlesource.com/c/chromium/src/+/2090095.
I am trying to understand why it did not tried to be strict at that time.


### hc...@chromium.org (2026-02-10)

@yy...@chromium.org

ChromeStatus entry at <https://chromestatus.com/feature/5172375182245888>, with I2S email at <https://groups.google.com/a/chromium.org/g/blink-dev/c/8AK8V4fSZFU>

also sent you the CL with the fix (and a histogram) at <https://chromium-review.googlesource.com/c/chromium/src/+/7535636>

### yy...@chromium.org (2026-02-12)

Thank you for setting up the ChromeStatus and starting the I2S mail thread.
I feel my reply in #comment25 did not accurately explain my concern.  Let me join the I2S thread to clarify the part, which you have already touched in #comment23.

### yy...@chromium.org (2026-02-16)

We recently triaged the interesting ServiceWorker issue.
https://github.com/w3c/ServiceWorker/issues/1254

I thought all clients are under control but it actually not?

### hc...@chromium.org (2026-02-19)

@yy...@chromium.org

Looking at this, I don't think that issue changes the intended fix. Specifically, assuming that `includeUncontrolled: true` is talking about

<https://developer.mozilla.org/en-US/docs/Web/API/Clients/matchAll#includeuncontrolled>

then the relevant text is

```
A boolean value — if set to true, the matching operation will return all service worker clients who share the same origin as the current service worker. 
Otherwise, it returns only the service worker clients controlled by the current service worker. The default is false.

```

The important bit for us is that clients will always be same-origin as the current service worker, so the IP address space and permission are going to be the same origin as the service worker. In that issue it even talks about the polyfill of `Client.postMessage() and then modify window.location`, which is I believe also a good reason to fix this by having the initiator of the navigation be the RFH of the windowclient.

### hc...@chromium.org (2026-02-19)

@yy...@chromium.org

I was doing a bit more digging in the spec, seeing what might need to change, and I feel like this might already be specified in the spec?

Specifically, <https://w3c.github.io/ServiceWorker/#client-navigate>, step 7 substep 3 says:

`HandleNavigate: Navigate browsingContext to url, using browsingContext’s associated document`

where `browsingContext` is the `ServiceWorkerClient` context, and not the service worker's browsing context.

`Navigation` here is defined by <https://html.spec.whatwg.org/multipage/browsing-the-web.html#navigate>, where in step 6 the initiator is set.

so I think my CL might be making the `navigate()` call more spec compliant?

Am I reading this wrong?

### ct...@chromium.org (2026-02-19)

Yeah it sounds like we should already be using the [client's Document](https://w3c.github.io/ServiceWorker/#client-navigate:~:text=HandleNavigate%3A%20Navigate%20browsingContext%20to%20url%2C%20using%20browsingContext%E2%80%99s%20associated%20document%2C%20with%20exceptionsEnabled%20true.) (and Document's [policy container](https://html.spec.whatwg.org/multipage/browsers.html#policy-containers), thus the client's IP address space, because that is [added to the Document's policy container by the current LNA spec](https://wicg.github.io/local-network-access/#integration-with-html)) when doing LNA checks on the navigation fetch request.

What I'm not completely sure about is how <https://html.spec.whatwg.org/multipage/browsing-the-web.html#beginning-navigation> actually then results in a navigation fetch -- this part of the HTML spec is a bit foreign to me. When the [source snapshot params](https://html.spec.whatwg.org/multipage/browsing-the-web.html#snapshotting-source-snapshot-params) are created based on the sourceDocument this should clone the Document's policy container, and then the actual call into the Fetch spec for this would be in ["create navigation params by fetching"](https://html.spec.whatwg.org/multipage/browsing-the-web.html#create-navigation-params-by-fetching) which creates a new fetch request with mode "navigate". This should hit the all the existing LNA checks.

### jd...@chromium.org (2026-02-23)

Given that the spec stuff is blocking the blink API owner sign-off, I'm marking this as having an external dependency. Obviously, we should continue to push in github, but I'm using "external dependency" to roughly mean "Chrome's issue tracker is not the authoritative bug tracker for next steps at this moment in time".

### yy...@chromium.org (2026-02-24)

Sorry for the slow reply, as I mentioned in the chat, I think it is generally good to make the behavior aligned with the specification.  However, at the same time, since this brings the web developer-facing Chromium behavior change, we need to ensure the developers that there is a behavior change regardless of LNA.  I understand that LNA is already tightly coupled with the existing policy mechanism, it is not possible to isolate spec alignment change from the LNA-related change.

You have already sent I2S for LNA check's I2S.  However, we may need to clarify that this LNA change also brings the Client.Navigate() behavior change regardless of LNA, to make the behavior aligned with the specification.  We also need to have a Client.Navigate() use counter, and a feature flag for the change.

### hc...@chromium.org (2026-02-24)

> You have already sent I2S for LNA check's I2S. However, we may need to clarify that this LNA change also brings the Client.Navigate() behavior change regardless of LNA, to make the behavior aligned with the specification. We also need to have a Client.Navigate() use counter, and a feature flag for the change.

Added the use counter in <https://chromium-review.googlesource.com/c/chromium/src/+/7603042>.

Also added a kill switch feature flag in <https://chromium-review.googlesource.com/c/chromium/src/+/7535636>.

I'll update the I2S after we hear something on the [navigation-dev@ post](https://groups.google.com/a/chromium.org/g/navigation-dev/c/HAVTdd4NpBc)

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  main  

Author:  Hubert Chao [hchao@chromium.org](mailto:hchao@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603042>

Add use counter for windowclient.navigate

---


Expand for full commit details
```
     
    Bug: 454162508 
    Change-Id: Ie8acea4448210d9fcec816ceb5db1946fc990115 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7603042 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Auto-Submit: Hubert Chao <hchao@chromium.org> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1589802}

```

---

Files:

- M `third_party/blink/public/mojom/use_counter/metrics/web_feature.mojom`
- M `third_party/blink/renderer/modules/service_worker/window_client.idl`
- M `tools/metrics/histograms/metadata/blink/enums.xml`

---

Hash: [7c34d01d23c11959a5078e91962feb0215b27036](https://chromiumdash.appspot.com/commit/7c34d01d23c11959a5078e91962feb0215b27036)  

Date: Wed Feb 25 01:01:23 2026


---

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  Hubert Chao [hchao@chromium.org](mailto:hchao@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7535636>

[LNA] Enforce LNA checks on Service Worker's WindowClient.navigate

---


Expand for full commit details
```
     
    Change WindowClient.navigate calls 
    (https://developer.mozilla.org/en-US/docs/Web/API/WindowClient/navigate) 
    to properly set the initiator to be the WindowClient so that initiator 
    client security state is used for LNA checks. 
     
    Added test, which involved refactoring some test files. 
     
    Bypass-Check-License: moved files 
    Bug: 454162508 
    Change-Id: I735a0b3c35b901da688bbb2398fb3f567de64510 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7535636 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Commit-Queue: Hubert Chao <hchao@chromium.org> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1591100}

```

---

Files:

- M `chrome/browser/local_network_access/local_network_access_policies_browsertest.cc`
- M `chrome/browser/local_network_access/local_network_access_workers_browsertest.cc`
- D `chrome/test/data/local_network_access/fetch-from-service-worker-as-public-address.html`
- D `chrome/test/data/local_network_access/fetch-from-service-worker-as-public-address.js`
- A `chrome/test/data/local_network_access/request-from-service-worker-as-public-address.html`
- R `chrome/test/data/local_network_access/request-from-service-worker-as-public-address.html.mock-http-headers`
- A `chrome/test/data/local_network_access/request-from-service-worker-as-public-address.js`
- R `chrome/test/data/local_network_access/request-from-service-worker-as-public-address.js.mock-http-headers`
- M `content/browser/service_worker/service_worker_client_utils.cc`
- M `content/browser/service_worker/service_worker_client_utils.h`
- M `content/browser/service_worker/service_worker_version.cc`
- M `content/common/features.cc`
- M `content/common/features.h`
- M `tools/metrics/histograms/metadata/service/histograms.xml`

---

Hash: [ffbeba92237994d1bad06c7a13138620b0246f68](https://chromiumdash.appspot.com/commit/ffbeba92237994d1bad06c7a13138620b0246f68)  

Date: Thu Feb 26 22:22:40 2026


---

### ch...@google.com (2026-03-11)

hchao: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-11)

Project: chromium/src  

Branch:  main  

Author:  Hubert Chao [hchao@chromium.org](mailto:hchao@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7654155>

[LNA] enable kServiceWorkerWindowClientInitiator by default.

---


Expand for full commit details
```
     
    Approved in https://chromestatus.com/feature/5172375182245888 
     
    Bug: 454162508 
    Change-Id: I253180d2793ed43c8155583b220b5f6836d5abe0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7654155 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Hubert Chao <hchao@chromium.org> 
    Reviewed-by: Camille Lamy <clamy@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1597688}

```

---

Files:

- M `content/common/features.cc`

---

Hash: [3293c62a4142a17383bb592c803318725d56cb31](https://chromiumdash.appspot.com/commit/3293c62a4142a17383bb592c803318725d56cb31)  

Date: Wed Mar 11 13:13:40 2026


---

### ch...@google.com (2026-03-13)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-13)

**Merge approved:** your change passed merge requirements and is auto-approved for M147. Please go ahead and merge the CL to branch 7727 (refs/branch-heads/7727) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  main  

Author:  Hubert Chao [hchao@chromium.org](mailto:hchao@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7657966>

[LNA] WPTs for service worker navigate() calls.

---


Expand for full commit details
```
     
    Adding WPTs to cover the service worker navigate() case. Browser 
    tests were added in crrev.com/c/7535636, this adds WPTs for the same 
    cases. 
     
    Bug: 454162508 
    Change-Id: I2c2c42f78c7b9cae37ddf1083e806b4f6b91acb4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7657966 
    Reviewed-by: Chris Thompson <cthomp@chromium.org> 
    Commit-Queue: Hubert Chao <hchao@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1599066}

```

---

Files:

- M `third_party/blink/web_tests/external/wpt/fetch/local-network-access/resources/service-worker.html`
- M `third_party/blink/web_tests/external/wpt/fetch/local-network-access/resources/service-worker.js`
- M `third_party/blink/web_tests/external/wpt/fetch/local-network-access/service-worker.tentative.https.html`

---

Hash: [715514352350d4fa2d9eb5a6ad8bbb5614f49c12](https://chromiumdash.appspot.com/commit/715514352350d4fa2d9eb5a6ad8bbb5614f49c12)  

Date: Fri Mar 13 15:11:09 2026


---

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Hubert Chao [hchao@chromium.org](mailto:hchao@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7665619>

[LNA] enable kServiceWorkerWindowClientInitiator by default.

---


Expand for full commit details
```
     
    Approved in https://chromestatus.com/feature/5172375182245888 
     
    (cherry picked from commit 3293c62a4142a17383bb592c803318725d56cb31) 
     
    Bug: 454162508 
    Change-Id: I253180d2793ed43c8155583b220b5f6836d5abe0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7654155 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Hubert Chao <hchao@chromium.org> 
    Reviewed-by: Camille Lamy <clamy@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1597688} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665619 
    Reviewed-by: Hubert Chao <hchao@chromium.org> 
    Auto-Submit: Hubert Chao <hchao@chromium.org> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#277} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `content/common/features.cc`

---

Hash: [44b74d11d164d11dfdf71d45ab6170cb5eaf31e1](https://chromiumdash.appspot.com/commit/44b74d11d164d11dfdf71d45ab6170cb5eaf31e1)  

Date: Fri Mar 13 21:15:57 2026


---

### pe...@google.com (2026-03-13)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### hc...@chromium.org (2026-03-16)

1. Bug has been present since we launched LNA, so M142+
2. No.

### vi...@google.com (2026-03-18)

Hi. I've labeled `LTS-NotApplicable-138` because, like mentioned in [#43](https://buganizer.corp.google.com/issues/454162508#comment43), the bug has been present since launched LNA, so M142+.

### vi...@google.com (2026-04-14)

I've been looking into backporting the CLs "[LNA] Enforce LNA checks on Service Worker's WindowClient.navigate" and "[LNA] enable kServiceWorkerWindowClientInitiator by default" to M144.

However, these changes appear to be too intertwined with subsequent LNA development that occurred after the M144 release. For example, my attempt to try the first CL (<https://ci.chromium.org/ui/p/chromium-m144/builders/try/win-rel/6061/overview>) failed because of an "use of undeclared identifier 'https\_public\_server'" error, which stems from further bulk LNA work that affected both the `//content` and `//services/network` layers (see <https://chromium-review.git.corp.google.com/c/chromium/src/+/7262373> and <https://chromium-review.git.corp.google.com/c/chromium/src/+/7254070>).

Given this complexity, I am currently labeling this as `LTS-NotApplicable-144`. Please let me know if you believe there is another approach I should consider.

### hc...@google.com (2026-04-16)

The merge conflicts are likely just with the tests, so if you ignored the tests you could probably get the merge in pretty cleanly. That being said:

- tests are probably good to have
- merging the tests in w/o these other changes is non-trivial
- this issue is probably not worth the effort to get it merged into LTS

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Universal Cross Site Scripting (includes Site Isolation bypass).


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/454162508)*
