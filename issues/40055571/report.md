# Security: spook.js attacks on site vs origin isolation; extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40055571](https://issues.chromium.org/issues/40055571) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ge...@umich.edu |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-04-16 |
| **Bounty** | $3,000.00 |

## Description

Attached is a pre-print paper we've been sent.

From briefly scanning, it says:

* Lumping together multiple origins into a single renderer process is suboptimal, and makes them vulnerable to spectre.js type attacks. I don't think this is news.
* We also lump together extensions into a single renderer process, and so they were able to steal passwords from LastPass by writing a malicious extension.

Nasko, Devlin, it feels to me like this second part *possibly* might merit some countermeasures. Could you take a look?

I understand they aim to publish "within 90 days".


## Attachments

- [strictsiteiso-vendors-20210416.pdf](attachments/strictsiteiso-vendors-20210416.pdf) (application/pdf, 3.0 MB)

## Timeline

### ad...@google.com (2021-04-16)

Monorail ate the PDF - re-adding.

### na...@chromium.org (2021-04-16)

Adding alexmos@ for visibility.

### rd...@chromium.org (2021-04-16)

Note: I haven't had a chance to read the paper, so just going off the question from adetaylor@ in c#0.

TL;DR: Nothing new here.

> * We also lump together extensions into a single renderer process, and so they were able to steal passwords from LastPass by writing a malicious extension.

This is really the same as the previous bullet.  At their core here, extensions are very akin to origins in this situation.  Lumping them together makes them vulnerable to spectre-like attacks.  And using LastPass as an example isn't really different than using passwords.google.com - in both cases, if we happen to lump origins (either web pages or extensions) together, there's a risk of leaking data.

We've chatted in the past about different ways we might potentially address this - essentially, trying to be "smarter" about which extensions we join together.  We've come up with a few different ideas - grouping extensions based on install source (e.g. policy installed together, component together, user-installed together), allowing extensions to specify a key in their manifest (`"isolate_me": true`), etc.  We haven't found anything that is scalable and also solved the majority of cases, so haven't invested heavily in it (though I'd still be supportive).

I also vaguely thought we were looking at different ways we could identify "high value" origins in general, and avoid having those share processes (or be stricter about what's allowed to share with them) - is there still work on that front?  If so, it seems like we could just include extensions in that mechanism (and, ideally, things would "just work").

### na...@chromium.org (2021-04-16)

I haven't read the full paper in depth yet, but skimming over there is one worrisome part - they claim they can extract HttpOnly cookies from the renderer process memory:

"Next, as the user was previously authenticated through the university’s single sign-on screen, the housing’s portal iframe automatically accessed the university’s HttpOnly login cookie,  ringing it to the memory address space of the renderer process, without any user interaction."

If this is correct, then we likely have a bug on our hands as we don't allow renderers to access HttpOnly cookies.



### na...@chromium.org (2021-04-16)

As a follow up, https://crbug.com/chromium/1019732 is where we tracked to work to ensure HttpOnly cookies do not propagate to the renderer process.

### al...@chromium.org (2021-04-17)

I also haven't read the full paper yet, but I'm curious if we could ask the authors for deanonymized links to their code?  The paper already includes all the authors' names, so I'm assuming they aren't worried about anonymity w.r.t. Chrome, and it might be useful for us to try out some of the links they mention (e.g., https://web.dpt.uni.edu/∼user/) as we investigate this in more detail.
 
+1 to everything Devlin said in https://crbug.com/chromium/1199865#c3.  We've considered various ways of grouping different kinds of extensions in separate processes (privileges, source, etc.), but this hasn't been prioritized so far.  I thought we had a bug filed for that, but so far I can't find it.  We will soon have a new mechanism with SiteInstanceGroups (https://crbug.com/chromium/1195535), which might allow doing this quite easily.
 
Re: avoiding process sharing for "high-value" origins within a particular site: in general, our hands are tied by document.domain compatibility, but we've recently shipped Origin-Agent-Cluster (https://web.dev/origin-agent-cluster/, M89+) which allows origins to opt-in to origin-level (rather than site-level) isolation (and willingly opt out of using document.domain).  Origins can also hint at this and get stronger protection with COOP+COEP headers (https://web.dev/coop-coep/).

### [Deleted User] (2021-04-17)

[Empty comment from Monorail migration]

### al...@chromium.org (2021-04-21)

The paper's authors have confirmed that we only leak HttpOnly cookies to the renderer if DevTools had been previously opened.

Adding some DevTools folks: caseq@, jarhar@, or yangguo@, can you confirm whether this is expected, and share any thoughts about fixing it?  Basically, the paper shared with us here shows how to use Spectre to leak HttpOnly cookies to a same-site cross-origin document in the same process.

I found https://crbug.com/chromium/849483, where the description includes "stop routing sensitive data (e.g. HTTP-only cookies) through renderer", so it seems like this is a known issue?  That issue is marked fixed, but with a final comment by jarhar@ "We don't currently have any more plans to move network instrumentation from the renderer process to the browser process", so it's a bit unclear what has and hasn't been fixed, and what the current state of HttpOnly cookies with DevTools is (and whether we need to file a new bug for this).

### ca...@chromium.org (2021-04-22)

It looks like the https://crbug.com/chromium/849483 has been closed a bit prematurely (re-opened that now). While the new instrumentation has actually been implemented, we're apparently still reporting the raw headers to renderer as well. I've no idea why this hasn't been removed back then, but I assume it might have been left temporarily for compatibility reasons (jarhar@ may have more context here). I think we should be able to drop URLResponseHead::raw_request_response_info altogether now.


### ja...@chromium.org (2021-04-22)

HttpOnly cookies should only be sent over the secure Network.*ExtraInfo CDP events, right...?
Upon further inspection, I found that Network.responseReceived actually includes HttpOnly cookies...

Since we are already excluding cookies for cross origin requests as of https://crbug.com/chromium/868407, I figured HttpOnly cookies would have also been excluded - I guess I was wrong.
I think it would make sense to start excluding HttpOnly cookies from Network.responseRecieved now, since we should already be getting them in the secure Network.*ExtraInfo requests.

Removing report_raw_headers, which I created https://crbug.com/chromium/1017836 to track, is blocked by https://crbug.com/chromium/1004979, which is that shared workers aren't fully instrumented like service workers and don't get the ExtraInfo events, which means that they need report_raw_headers in order to get more useful headers.

I started working on shared worker instrumentation but it became an enormous refactor I never quite completed. We could probably just remove report_raw_headers since it's not that likely anyone actually cares about more accurate headers for shared worker requests anyway...

tldr:
We can either filter out HttpOnly cookies from Network.responseReceived when report_raw_headers is enabled which shouldn't break anything, OR we could delete report_raw_headers entirely, which could theoretically lose DevTools some headers for shared worker network requests.

### ja...@chromium.org (2021-04-22)

The reason why I'm not that concerned about providing more detailed shared worker request info is because the issue for auto attach on shared workers only has three stars: https://crbug.com/chromium/851323

### ad...@google.com (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-22)

[Empty comment from Monorail migration]

### cr...@chromium.org (2021-04-27)

sroettger@: You may be interested in the paper in https://crbug.com/chromium/1199865#c1, to evaluate how it compares to leaky.page.

jarhar@: It would be great to proceed with removing report_raw_headers in https://crbug.com/chromium/1017836 if possible!  I'll list that as a blocking bug here, since it's one of the main new findings from the paper (with the mitigating factor that it requires opening DevTools for the data to leak).

### aj...@google.com (2021-04-27)

Tentatively setting a severity - feel free to adjust.

### ja...@chromium.org (2021-04-28)

I started a CL here: https://chromium-review.googlesource.com/c/chromium/src/+/2856099
It might end up more complicated than I described due to the SecurityState given back from report_raw_headers among other things...

### ja...@chromium.org (2021-04-28)

It looks like disabling report_raw_headers would be more challenging than I thought:
1. Network.responseReceived's securityState and securityDetails appear to only be reported when report_raw_headers is true, so we would either have to report this from the network stack regardless of report_raw_headers, or move it to Network.responseReceivedExtraInfo [1].
2. It appears that the response HTTP status code can change based on report_raw_headers [1]? I suppose we would also need to move that to Network.responseReceivedExtraInfo...
3. The last time I checked, due to the way Puppeteer is architected, it doesn't use Network.*ExtraInfo CDP events, which means that it is completely relying on report_raw_headers for just about everything, and removing it would definitely make its users unhappy. The reason it can't use ExtraInfo events is because not every request that chrome "makes" actually includes ExtraInfo events - the ones which don't make it all the way to the network stack or stay in the renderer don't get these events. In order for this to be addressed, Puppeteer should probably be using the CDP Fetch domain or something instead...? Maybe we could work around this by letting Puppeteer use report_raw_headers while making chrome not use report_raw_headers...?

The other option, which would exclude HttpOnly cookies from the raw response info sent back to the renderer, requires more knowledge of the network stack than I have. It looks like we could filter them out here [2], but I don't know how to take an actual string of header information, parse the cookies out if it, and determine if each cookie was HttpOnly or not...

I also want to make sure I understand the issue completely:

> The paper's authors have confirmed that we only leak HttpOnly cookies to the renderer if DevTools had been previously opened.

> Basically, the paper shared with us here shows how to use Spectre to leak HttpOnly cookies to a same-site cross-origin document in the same process.

I understand that allowing HttpOnly cookies into the renderer is a problem in and of itself, but what exactly is a "same-site cross-origin document" and how does it affect the scenario? Is HttpOnly cookies in a renderer process for its own site the *only* concern here?

[1] https://test-results.appspot.com/data/layout_results/linux-rel/677426/blink_web_tests%20%28with%20patch%29/layout-test-results/results.html
[2] https://source.chromium.org/chromium/chromium/src/+/master:services/network/url_loader.cc;l=339-355;drc=221e331b49dfefadbc6fa40b0c68e6f97606d0b3

### [Deleted User] (2021-04-29)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-29)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-01)

nasko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@chromium.org (2021-05-03)

At this point the only issue requiring action on this bug is the leaking of HttpOnly cookies through DevTools, which this bug is already dependent on. Therefore I'll assign this to jarhar@ to resolve once the DevTools issue is fixed or pass along to whoever will work on it.

### ja...@chromium.org (2021-05-07)

Upon further investigation of puppeteer, I found (and remembered) that it already uses the CDP Fetch domain. If it can (or already does) get good header information out of Fetch events, then it will definitely be easier for us to remove report_raw_headers

### rd...@chromium.org (2021-05-18)

[Empty comment from Monorail migration]

### ja...@chromium.org (2021-05-18)

I am still working on removing report_raw_headers here: https://chromium-review.googlesource.com/c/chromium/src/+/2856099
I also have another patch which should help puppeteer move off of report_raw_headers: https://chromium-review.googlesource.com/c/chromium/src/+/2898747

### cr...@chromium.org (2021-05-28)

https://crbug.com/chromium/1199865#c24: Glad to hear!  Please keep us updated, since we're still hopeful to get the HttpOnly issue resolved quickly if possible.

In the meantime, I've added a "Strict Extension Isolation" feature to chrome://flags in https://crbug.com/chromium/1209417 (r887395, disabled by default), so that we can experiment with the impact on the process count.  If that works out performance-wise, we may be able to prevent the extension sharing discussed in the paper.  (Again, that was a prior known issue, but it would be great to get it resolved.)

[Monorail components: Platform>Extensions]

### ya...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-02)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2021-06-10)

[Empty comment from Monorail migration]

### wj...@chromium.org (2021-06-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

Setting FoundIn-91 (which may be a bit approximate, but is good enough for Sheriffbot)

### gi...@appspot.gserviceaccount.com (2021-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7d3da352d7833e4e8966c87321ef063f9d0dad31

commit 7d3da352d7833e4e8966c87321ef063f9d0dad31
Author: Joey Arhar <jarhar@chromium.org>
Date: Tue Aug 03 22:32:36 2021

[DevTools] Remove report_raw_headers from network::ResourceRequest

This patch also removes raw response info from
network::mojom::URLResponseHead.

report_raw_headers has been used by DevTools to get "raw" headers for
network request debugging. However, the renderer process shouldn't have
access to raw headers, because then it would have access to cross-origin
cookies, HttpOnly cookies, etc.

In order to fix this security issue but still make headers debuggable
for DevTools, a trusted channel to the DevTools frontend which goes
through the browser process instead of the renderer process was made,
and I plumbed an ID, called "devtools_request_id", through this channel
in crrev.com/648335 so DevTools has required context to debug the
network request.

Now that DevTools doesn't need report_raw_headers in order to debug
network headers anymore, we're removing it along with the related raw
header code in order to simplify things and strengthen security.

I waited longer than I should have to do this because shared worker
request debugging still relies on report_raw_headers, but in light of
recent security issues, in addition to lack of perceived interest in
shared worker request debugging, and *significant* complexity of
updating shared worker code, I am going for it now.

Bug: 1142014
Fixed: 1199865, 1017836, 849483
Change-Id: I903770a0038bfed1ad8d5ebba6a44a8b5eefe5a7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2856099
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Benoit L <lizeb@chromium.org>
Reviewed-by: Ryan Sturm <ryansturm@chromium.org>
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Reviewed-by: Sean Topping <seantopping@chromium.org>
Reviewed-by: Junbo Ke <juke@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/heads/master@{#908142}

[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/chrome/browser/android/customtabs/detached_resource_request.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/chrome/browser/prefetch/search_prefetch/base_search_prefetch_request.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/chrome/browser/prefetch/search_prefetch/search_prefetch_from_string_url_loader.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/chrome/browser/prefetch/search_prefetch/search_prefetch_service_browsertest.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/chrome/browser/prefetch/search_prefetch/streaming_search_prefetch_url_loader.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/chromecast/net/connectivity_checker_impl.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/content/browser/devtools/network_service_devtools_observer.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/content/browser/devtools/protocol/network_handler.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/content/browser/loader/navigation_url_loader_impl.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/content/browser/service_worker/service_worker_fetch_dispatcher.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/content/browser/web_package/prefetched_signed_exchange_cache.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/content/browser/web_package/signed_exchange_prefetch_handler.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/content/browser/web_package/signed_exchange_request_handler.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/content/renderer/service_worker/service_worker_subresource_loader.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/headless/test/headless_devtools_client_browsertest.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/cors/preflight_controller.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/cors/preflight_controller_unittest.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/network_service_network_delegate.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/network_service_unittest.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/public/cpp/resource_request.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/public/cpp/resource_request.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/public/cpp/url_request_mojom_traits.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/public/cpp/url_request_mojom_traits.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/public/cpp/url_request_mojom_traits_unittest.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/public/mojom/BUILD.gn
[delete] https://crrev.com/bd9851d3b929544f5e4dd91265ccad5ce203fad7/services/network/public/mojom/http_raw_request_response_info.mojom
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/public/mojom/url_request.mojom
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/public/mojom/url_response_head.mojom
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/test/test_url_loader_factory_unittest.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/test/test_utils.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/test/test_utils.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/url_loader.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/url_loader.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/services/network/web_bundle_url_loader_factory.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/public/BUILD.gn
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/public/devtools_protocol/browser_protocol.pdl
[delete] https://crrev.com/bd9851d3b929544f5e4dd91265ccad5ce203fad7/third_party/blink/public/platform/web_http_load_info.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/public/platform/web_url_request.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/public/platform/web_url_response.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/core/inspector/inspector_network_agent.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/BUILD.gn
[delete] https://crrev.com/bd9851d3b929544f5e4dd91265ccad5ce203fad7/third_party/blink/renderer/platform/exported/web_http_load_info.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/exported/web_url_request.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/exported/web_url_response.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/BUILD.gn
[delete] https://crrev.com/bd9851d3b929544f5e4dd91265ccad5ce203fad7/third_party/blink/renderer/platform/loader/fetch/resource_load_info.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/resource_loader.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/resource_loader.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/resource_request.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/resource_request.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/resource_response.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/resource_response.h
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/url_loader/request_conversion.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/url_loader/web_url_loader.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/renderer/platform/loader/fetch/url_loader/worker_main_script_loader.cc
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/disabled-cache-navigation-expected.txt
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/disabled-cache-navigation.js
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/multiple-headers-expected.txt
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/multiple-headers.js
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/navigation-xfer-size.js
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/raw-headers-after-navigation-expected.txt
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/raw-headers-after-navigation.js
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/raw-headers-for-protected-document-expected.txt
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/raw-response-headers-expected.txt
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/raw-response-headers.js
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/request-interception-raw-headers-expected.txt
[modify] https://crrev.com/7d3da352d7833e4e8966c87321ef063f9d0dad31/third_party/blink/web_tests/http/tests/inspector-protocol/network/request-interception-raw-headers.js


### [Deleted User] (2021-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-04)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-11)

The VRP Panel has decided to award $2000 this report. We appreciate folks doing this research and sharing this information with us! 

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### cr...@chromium.org (2021-08-25)

As part of the extension discussions here, we also investigated a feature to prevent different extensions from sharing a process with each other in https://crbug.com/chromium/1209417.  We monitored the performance impact and have just enabled it by default on M92 stable!

### am...@google.com (2021-09-02)

The VRP Panel has reassessed this reward amount based on other data provided and have decided to extend an additional $1000 for a total reward amount of $3000. 

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/27342986eec43029804afd89042fd0bcf329213b

commit 27342986eec43029804afd89042fd0bcf329213b
Author: Joey Arhar <jarhar@chromium.org>
Date: Tue Oct 19 22:26:26 2021

[DevTools] Add responseReceived.emittedExtraInfo

Design doc which discusses more background and other options:
https://docs.google.com/document/d/1NM30Wg_aM3-RFZaD_lQuWQj8my8XoR9YpMi60QH1lHU/edit

The new responseReceived.emittedExtraInfo flag indicates whether or not
requestWillBeSentExtraInfo and responseReceivedExtraInfo events were
also emitted for the same network request.

With this knowledge, CDP clients like puppeteer can know whether or not
to wait for the pairing of responseReceived and ExtraInfo events.
Without this knowledge, they currently can't expose the information in
ExtraInfo events because they would get hung up waiting for ExtraInfo
events for requests which don't emit them.
The information in ExtraInfo events is very important because they have
significantly more accurate HTTP headers, among other things.

This also addresses a regression for puppeteer when I removed
report_raw_headers from ResourceRequest in http://crrev.com/908142.
Puppeteer relies on report_raw_headers because it can't lazily wait for
ExtraInfo events like the DevTools frontend does. However, with this new
flag, Puppeteer can actually start using ExtraInfo events.

In order to implement the flag, I am plumbing it through the network
service interface. Alternatively, we could try to guess whether network
service will emit ExtraInfo events, but based on my prototyping I
couldn't get this to work with the limited information we have in the
renderer process.

Bug: 1199865, 1017836, 849483
Change-Id: I986ae119b4b077b71c31298370b6e091dd9d15c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2898747
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#933202}

[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/renderer/core/inspector/inspector_network_agent.cc
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/public/devtools_protocol/browser_protocol.pdl
[add] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/web_tests/http/tests/inspector-protocol/network/extra-info-emitted.js
[add] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/web_tests/http/tests/inspector-protocol/network/redirect-has-extra-info.js
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/renderer/platform/loader/fetch/url_loader/web_url_loader.cc
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/renderer/platform/exported/web_url_response.cc
[add] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/web_tests/http/tests/inspector-protocol/network/extra-info-emitted-expected.txt
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/web_tests/http/tests/inspector-protocol/network/multiple-redirects-extrainfo-expected.txt
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/services/network/url_loader.h
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/services/network/public/mojom/devtools_observer.mojom
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/public/platform/web_url_response.h
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/services/network/url_loader.cc
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/services/network/public/mojom/url_response_head.mojom
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/services/network/public/cpp/devtools_observer_util.cc
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/web_tests/http/tests/inspector-protocol/network/multiple-redirects-extrainfo.js
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/content/browser/devtools/protocol/network_handler.cc
[add] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/web_tests/http/tests/inspector-protocol/network/redirect-has-extra-info-expected.txt
[modify] https://crrev.com/27342986eec43029804afd89042fd0bcf329213b/third_party/blink/renderer/platform/loader/fetch/resource_response.h


### [Deleted User] (2021-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-01-31)

[Comment Deleted]

### gm...@google.com (2022-01-31)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1199865?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Extensions]
[Monorail blocked-on: crbug.com/chromium/1017836, crbug.com/chromium/1209417]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055571)*
