# SW can intercept potential-navigation-or-subresource request

| Field | Value |
|-------|-------|
| **Issue ID** | [40089219](https://issues.chromium.org/issues/40089219) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>FetchAPI, Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2017-10-05 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/embed_fetch.html
2. Reload the page.
3. Flash is being served.

What is the expected behavior?
Fetch from embed or object tag should not intercepted by SW.

What went wrong?
Following indicate that it is bad idea to serve plug-ins through SW.
https://w3c.github.io/ServiceWorker/v1/#implementer-concerns

Protection against such case is provided by step 9 of Handle Fetch.
https://w3c.github.io/ServiceWorker/v1/#handle-fetch

But SW in chrome can intercept any request made by Embed or Object tag. This is violation of spec.

Did this work before? N/A 

Chrome version: 61.0.3163.100  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### el...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>Network>FetchAPI Blink>ServiceWorker]

### oc...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

### wf...@chromium.org (2017-10-10)

I'm not sure this is a security bug in particular, how it affects our users' security. This seems like a spec bug to me. -> jake to decide.

### el...@chromium.org (2017-10-10)

The security concern is noted in the spec: https://w3c.github.io/ServiceWorker/v1/#implementer-concerns

"Plug-ins should not load via service workers. As plug-ins may get their security origins from their own urls, the embedding service worker cannot handle it."

I believe that both Flash (See Tangled Web, pg 154) (and Java) do get security origins from their URLs, but what's less clear is how this would represent a vulnerability given the same-origin requirements around ServiceWorker.

### fa...@chromium.org (2017-10-10)

This was supposed to be covered by https://crbug.com/chromium/413094, though I see now there were no tests added and it's possible something regressed.

Is the site showing a Flash plugin running that was served by the SW? All I see is a .swf download being triggered.

Finally, the spec allows the impl to decide whether to allow SW interception or not (it's a non-normative note). According to the bug, we allowed certain object/embed types but not others.

### fa...@chromium.org (2017-10-10)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-02-09)

I did another look at this. I think this is probably a security bug, as evidenced by https://crbug.com/chromium/808838.

The test in c#0 is showing that service worker can intercept an <embed src='/'> request. The spec says not to intercept <embed> or <object> (in c#5, I was somewhat wrong: it's non-normative note pointing to a normative section of Handle Fetch).

Way back in https://crbug.com/chromium/413094, we disallowed intercepting only certain plugins (see https://codereview.chromium.org/606993002). I'm a bit confused why we went that way, there was a proposal to disallow all <object> (and <embed>?) fetches instead, but it seems we didn't take it because we wanted to allow PNaCl. See this long thread especially the comment here: https://groups.google.com/a/google.com/d/msg/chrome-serviceworker/7BLLIut176k/jaEh4TEZuN0J

My guess is https://crbug.com/chromium/800838 works because application/pdf gets handled by a plugin that was not blacklisted.

I believe PNaCl is deprecated but I am not familiar with plugins. Does anyone have a sense for whether we can just bypass the SW for all <embed> and <object> requests, as the spec says? That would seem to be the simplest solution but I don't know if it breaks web content. It would definitely break people who depended on PNaCl and application/pdf being handled by SW. Are there any other plugins?

I guess a first pass will be to check was Firefox does.

+rsleevi who is one of the last people from that thread still active around here.

### in...@chromium.org (2018-02-09)

[Empty comment from Monorail migration]

### ki...@chromium.org (2018-02-09)

Chatting with falken@ while looking into the code.  Should just removing or always setting ServiceWorkerMode::kNone in PepperURLLoaderHost::InternalOnHostMsgOpen (in pepper_url_loader_host.cc) work?

### sh...@chromium.org (2018-02-09)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-13)

M65 Stable promotion is coming VERY soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge  into the release branch ASAP. Thank you.

### fa...@chromium.org (2018-02-14)

I will investigate what other browsers do. If we find other browsers disallow SW interception of embed/object, we can probably align with them and the spec.

But one problem is I don't know where loading for embed/object lives. It seems it could go to MimeHandlerViewContainer (e.g., https://crbug.com/chromium/808838) or PepperURLLoaderHost (e.g., c#9 and https://crbug.com/chromium/413094). Maybe there are others?

### fa...@chromium.org (2018-02-14)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-02-16)

I determined that Firefox skips the service worker and Safari doesn't skip the service worker. It blocks the .swf download somehow (frame load interrupted), but if the worker simply replies with "hello world", then "hello world" is shown in the embed. I couldn't figure out how to test service workers in Edge.

### bu...@chromium.org (2018-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f1eb79c5305e19ceee013af158dd853e80e9d312

commit f1eb79c5305e19ceee013af158dd853e80e9d312
Author: Matt Falkenhagen <falken@chromium.org>
Date: Fri Feb 16 07:25:55 2018

service worker: Disallow interception for EMBED and OBJECT requests.

This matches the service worker specification and Firefox.

This change itself is probably not enough to skip all EMBED/OBJECT
requests, as some requests get initiated by PepperURLLoaderHost or
MimeHandlerViewContainer.

In implementor concerns:
https://w3c.github.io/ServiceWorker/#implementer-concerns
"Plug-ins should not load via service workers. As plug-ins may get their
security origins from their own urls, the embedding service worker cannot
handle it. For this reason, the Handle Fetch algorithm makes the
potential-navigation-or-subresource request (whose context is either <embed> or
<object>) immediately fallback to the network without dispatching fetch event."

In Handle Fetch:
https://w3c.github.io/ServiceWorker/#handle-fetch
"If request is a potential-navigation-or-subresource request, then:
Return null."


R=kinuko, yhirano

Bug: 771933
Change-Id: Ia04ae8dec8c968de6a73dca088aa88a67b21718a
Reviewed-on: https://chromium-review.googlesource.com/923445
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#537245}
[add] https://crrev.com/f1eb79c5305e19ceee013af158dd853e80e9d312/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/embed-and-object-are-not-intercepted.https.html
[add] https://crrev.com/f1eb79c5305e19ceee013af158dd853e80e9d312/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/embed-and-object-are-not-intercepted-worker.js
[add] https://crrev.com/f1eb79c5305e19ceee013af158dd853e80e9d312/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/embed-is-not-intercepted-iframe.html
[add] https://crrev.com/f1eb79c5305e19ceee013af158dd853e80e9d312/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/embedded-content-from-server.html
[add] https://crrev.com/f1eb79c5305e19ceee013af158dd853e80e9d312/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/embedded-content-from-service-worker.html
[add] https://crrev.com/f1eb79c5305e19ceee013af158dd853e80e9d312/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/object-is-not-intercepted-iframe.html
[modify] https://crrev.com/f1eb79c5305e19ceee013af158dd853e80e9d312/third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.cpp


### fa...@chromium.org (2018-02-19)

cc raymes for https://chromium-review.googlesource.com/c/chromium/src/+/923663 context

### bu...@chromium.org (2018-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a

commit 7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a
Author: Matt Falkenhagen <falken@chromium.org>
Date: Tue Feb 20 03:30:33 2018

service worker: Skip service worker for all Pepper plugins.

Back in https://crbug.com/chromium/413094, we decided to skip service worker for fetches from
Pepper plugins with "private permission" for security purposes. The
motivation was that Pepper plugins without "private permission" could be
assumed to enfore the same-origin policy. However, the spec has since
mandated skipping service workers for the request for the plugin itself,
i.e., the target URL of an EMBED or OBJECT element. This patch makes two
changes:

1) Requests *for* the target URL of EMBED or OBJECT element that load a
Pepper plugin skip service workers. This aligns with recent patches to
skip all EMBED or OBJECT element requests: r537245 skipped them for
embedded HTML content, and r537386 skipped them for MIME handler
plugins.

The code change is in ppb_nacl_private_impl.cc::CreateWebURLRequest.
This stops the requests for the manifest and pexe from being intercepted
by the service worker.

2) Requests *from* any Pepper plugin skip service workers. Previously,
we only skipped if the plugin had private permission, now we skip
regardless of permission.

The code change is in url_request_info_util.cc::CreateWebURLRequest.

One thing I'm not so sure about is PepperPluginInstanceImpl::Navigate
which apparently does a navigation in a frame. This is also changed to
to skip service workers (by changing the utility function
CreateWebURLRequest), but it's unclear whether that's needed.

You might ask why we don't change the service worker interception code
to just skip plugins, instead of changing the plugin callsites. This is
because at the SW interception site, we don't know whether the request
came from a plugin or not: for the manifest request, the
RequestContextType is "INTERNAL", and the ResourceType is "SUBRESOURCE".

It's also worth nothing that NetworkService/S13nServiceWorker already
skip the service worker for all these requests, since we don't hook in
at the URLRequestJob level anymore. In NS/S13nSW, we likely won't
need to set skip service worker at these callsites.

R=kinuko
TBR=bradnelson

Bug: 771933,413094
Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: I09db0eda46f2e7d9372495a6205f5cb0026de6c7
Reviewed-on: https://chromium-review.googlesource.com/923663
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Raymes Khoury <raymes@chromium.org>
Cr-Commit-Position: refs/heads/master@{#537706}
[modify] https://crrev.com/7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a/chrome/browser/chrome_service_worker_browsertest.cc
[modify] https://crrev.com/7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a/chrome/test/data/nacl/pnacl_url_loader/pnacl_url_loader.cc
[modify] https://crrev.com/7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a/chrome/test/data/nacl/pnacl_url_loader/pnacl_url_loader.html
[modify] https://crrev.com/7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a/components/nacl/renderer/ppb_nacl_private_impl.cc
[modify] https://crrev.com/7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a/content/renderer/pepper/pepper_url_loader_host.cc
[modify] https://crrev.com/7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a/content/renderer/pepper/url_request_info_util.cc
[modify] https://crrev.com/7031e8b8346db6c33a2f6a592fd7f6eaeec82e3a/testing/buildbot/filters/mojo.fyi.network_browser_tests.filter


### fa...@chromium.org (2018-02-20)

Now service workers are skipped for the following requests.
1) Requests for the target URL of an EMBED/OBJECT that embeds HTML content (r537245, c#15)
2) Requests for the target URL of an EMBED/OBJECT that is handled by the MIME plugin handler (r537386, https://crbug.com/chromium/808838).
3) Requests for the target URL of an EMBED/OBJECT that is a Pepper plugin (r537706, c#17)
4) Requests issued by Pepper plugins (r537706, c#17).

These changes are all in M66.

Previously, we skipped service worker only for requests issued by Pepper plugins with private permission (r297396, https://crbug.com/chromium/413094, c#13). We also skipped service worker for requests from NPAPI plugins (r297616, https://crbug.com/chromium/413094, c#14), but I believe Chrome no longer supports those.

I think now all requests for or from EMBED/OBJECT elements skip service workers, which matches the specification.

### el...@chromium.org (2018-02-20)

Re #18: what about image requests? The OBJECT element has a special hack whereby if the URL looks like that of an image, the load goes through ImageLoader. Until now, it's had a RequestContext of "image", but I'm about to change that to "object", but it will still be going through the ImageLoader. 

### fa...@chromium.org (2018-02-20)

I see. Probably image requests are going to service workers still. If the RequestContext is "object" it'll probably be easier to detect this and other such requests.

When S13nSW ships there will be less room for bugs like this, since we'll know exactly where requests get routed to the service worker. Right now we intercept when the browser is making a network request.

### go...@chromium.org (2018-02-20)

+ awhalley@ (Security TPM)

### bu...@chromium.org (2018-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/59ad2dcbe6dd5c5d846944258e6cd26a700ade83

commit 59ad2dcbe6dd5c5d846944258e6cd26a700ade83
Author: Matt Falkenhagen <falken@chromium.org>
Date: Wed Feb 21 05:40:22 2018

service worker: Disable interception when OBJECT/EMBED uses ImageLoader.

Per the specification, service worker should not intercept requests for
OBJECT/EMBED elements.

R=kinuko

Bug: 771933
Change-Id: Ia6da6107dc5c68aa2c2efffde14bd2c51251fbd4
Reviewed-on: https://chromium-review.googlesource.com/927303
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#538027}
[modify] https://crrev.com/59ad2dcbe6dd5c5d846944258e6cd26a700ade83/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/embed-and-object-are-not-intercepted.https.html
[modify] https://crrev.com/59ad2dcbe6dd5c5d846944258e6cd26a700ade83/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/embed-and-object-are-not-intercepted-worker.js
[add] https://crrev.com/59ad2dcbe6dd5c5d846944258e6cd26a700ade83/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/embed-image-is-not-intercepted-iframe.html
[modify] https://crrev.com/59ad2dcbe6dd5c5d846944258e6cd26a700ade83/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/embed-is-not-intercepted-iframe.html
[add] https://crrev.com/59ad2dcbe6dd5c5d846944258e6cd26a700ade83/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/object-image-is-not-intercepted-iframe.html
[modify] https://crrev.com/59ad2dcbe6dd5c5d846944258e6cd26a700ade83/third_party/WebKit/Source/core/loader/ImageLoader.cpp


### fa...@chromium.org (2018-02-21)

Now I've told ImageLoader to skip service worker when loading for an EMBED/OBJECT. Let me know if you know of more moles to whack...

### sh...@chromium.org (2018-02-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-23)

Requesting merge to 65 - if approved I recommend we merge on Monday to get a few more days of Dev coverage.

### sh...@chromium.org (2018-02-23)

This bug requires manual review: We are only 10 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-23)

[Comment Deleted]

### go...@chromium.org (2018-02-23)

[Comment Deleted]

### go...@chromium.org (2018-02-23)

Sorry taking merge approval back. There are multiple cls are listed here, which cl exactly you're requesting a merge for?

### aw...@google.com (2018-02-24)

Thank you for spotting, govind@, I must admit I only looked at the last change before requesting.

inferno@ - you marked this as ReleaseBlock-Stable - do you still consider that to be the case?

falken@ - what's your view on the stability risk of merging all the required CLs to 65? It would make the final beta, but with very little time to do anything if there is an issue found.



### fa...@chromium.org (2018-02-26)

Per an email thread, I was planning on letting all the CLs here and in https://crbug.com/chromium/808838 land in M66 and not merge. My main concern is web compatibility risk, e.g., a site relying on service workers to serve PDFs offline. If all CLs are kept together, we could have a single chromestatus.com entry saying "OBJECT/EMBED requests skip service workers in Chrome 66". 

I don't fully understand the security impact of this bug. The POC in https://crbug.com/chromium/771933#c0 just shows a plugin being downloaded and not run on my system. The POC in https://crbug.com/chromium/808838 is a clear problem: it shows a cross-origin PDF access.

I'd be mostly scared of cross-origin access of HTML embedded content inside OBJECT, e.g., you have <object data="myobject"> and have a service worker intercept the request and respond with "https://cross-origin.com/hello", and show that the page can access the contents via object.contentWindow. In my limited environment now (away from my workstation) I haven't been able to show this is possible pre-Chrome 65, but I'm not sure if it's just that the server is being clever.

As for stability risk, I think it's quite low. The CLs should be safe to merge. It's just the behavior change summarized in https://crbug.com/chromium/771933#c18 (plus the CL that came after in https://crbug.com/chromium/771933#c22) that I'm not so sure about, so wanted more bake time in Canary/Dev/Beta to see if authors complain.

### aw...@google.com (2018-02-26)

Thank you for the details falken@  OK to leave this until 66.

### aw...@google.com (2018-02-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-13)

Thanks for the report s.h.h.n.j.k@! The VRP Panel decided to award $500, but said they would consider a higher amount if you could provide a proof of concept that more explicitly shows the cross origin attack.

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@google.com (2018-12-20)

SW is supported on all platforms (except iOS, where we get Safari's implementation).

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/771933?no_tracker_redirect=1

[Multiple monorail components: Blink>Network>FetchAPI, Blink>ServiceWorker]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089219)*
