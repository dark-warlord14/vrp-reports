# Security: Same origin bypass with Service Workers + PDF plugin

| Field | Value |
|-------|-------|
| **Issue ID** | [40090387](https://issues.chromium.org/issues/40090387) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Network>FetchAPI, Blink>ServiceWorker, Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2018-02-04 |
| **Bounty** | $4,500.00 |

## Description

**VULNERABILITY DETAILS**  

Service workers can be used to intercept same-origin requests and respond with a cross-origin response.  

Chrome's built-in PDF viewer component allows web pages to read the content of same-origin PDF files.  

An attacker can bypass this same origin policy by loading a remote PDF file via a same-origin URL that is intercepted via a Service Worker.

This bug is possibly caused by SW-unawareness of the mimeHandlerPrivate API (used by the PDF plugin).

**VERSION**  

Chrome Version: 64.0.3282.119 (stable) + 66.0.3339.0 (canary)

**REPRODUCTION CASE**

1. Visit <https://robwu.nl/s/service-worker-pdf/?pdfUrl=https%3A%2F%2Fbitcoin.org%2Fbitcoin.pdf>
2. Observe that the page reads and shows the content of a PDF file at a different origin.

For future reference, I have attached the two files for the exploit.  

Service Workers are only enabled on HTTPS, so these files must be served over HTTPS (if serving over localhost, use the --allow-insecure-localhost flag).

## Attachments

- [index.html](attachments/index.html) (text/plain, 1.4 KB)
- [serviceworker.js](attachments/serviceworker.js) (text/plain, 358 B)

## Timeline

### ro...@robwu.nl (2018-02-04)

ccing raymes because he fixed https://crbug.com/chromium/520422 (not assigning because he seems OOO).

[Monorail components: Blink>Network>FetchAPI Blink>ServiceWorker]

### el...@chromium.org (2018-02-04)

Lots of interest in ServiceWorker this year. 

### ro...@robwu.nl (2018-02-04)

@#2 Can you cc me on https://crbug.com/chromium/808334 ?

### mk...@chromium.org (2018-02-05)

falken@: Can you triage this?

Cross-origin reads feel "high" severity to me. Could be convinced it's "medium" since (I assume?) the exploit is limited to PDFs?

### sh...@chromium.org (2018-02-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-05)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-02-06)

See also https://crbug.com/chromium/413094 and https://crbug.com/chromium/771933.  I think requests from plugins/embed are supposed to skip the service worker.

### ro...@robwu.nl (2018-02-12)

I've investigated this a bit more, and this is indeed an inssue in mimeHandlerPrivate.

There are two ways to solve this bug:
1. Propagate the actual URL of the response through the mimeHandlerPrivate API. That can be done by replacing "request->url()" with a look up for "response->head.url_list_via_service_worker" (and falling back to request->url() if needed).
  at https://chromium.googlesource.com/chromium/src/+/e600d04d75a74dbbcf8660670955d158525688e8/content/browser/loader/resource_dispatcher_host_impl.cc#555

2. Hiding the request from SW by calling request.SetServiceWorkerMode at the construction of the URLRequest in MimeHandlerViewContainer::OnReady
   at https://chromium.googlesource.com/chromium/src/+/c1a6eba72be450170ba3947bd5504c7db20afcec/extensions/renderer/guest_view/mime_handler_view/mime_handler_view_container.cc#158


Since plugins requests are supposed to be hidden from SW, I have submitted a patch that implements the second idea:
https://chromium-review.googlesource.com/c/chromium/src/+/914150

### ro...@robwu.nl (2018-02-13)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-02-13)

Thanks Rob for taking this and investigating.

The solution proposed in #1 looks a bit scary: it's changing RDHI which could affect things beyond MimeHandler/PDF. The real solution there would probably involve plumbing ResourceResponseInfo::FetchResponseType to the delegate, so it knows whether the response is opaque or not. You could have a cross-origin, non-opaque response if CORS was enabled.

The solution proposed in #2 looks more palatable and simpler but it possibly breaks existing content on the web. Would you be able to see whether PDFs skip the service worker for Firefox/Edge/Safari? If so I think we could go ahead and just do #2.

### ro...@robwu.nl (2018-02-14)

@#11 I opened the PoC from the report in Firefox, and did not see a PDF file.
Additionally, I visited about:debugging in Firefox, switched to the Worker tab, launched the debugger and put a breakpoint inside the "fetch" event and upon refreshing the page, it was triggered once (for the HTML page, not for the embedded PDF).

I haven't tested Safari nor Edge, but since plugin requests are expected to bypass the SW (mentioned twice in the spec, at [1] and [2]), I don't expect compat issues.

In my patch I provided an implementation-specific regression test; while it is possible to write a WPT test (based on my PoC), I don't think that is really useful, because there is no guarantee that the implementation is able to render the application/pdf MIME type. With my implementation-specific test, I do not only verify that the SW cannot observe plugin requests, I also verify that the plugin is actually loaded.

Can anyone with access to https://crbug.com/chromium/808334 cc me there? It is marked as a blocker for this bug, but without access I cannot judge whether it should be.

[1] https://www.w3.org/TR/service-workers-1/#handle-fetch
[2] https://www.w3.org/TR/service-workers-1/#implementer-concerns

### fa...@chromium.org (2018-02-14)

Thanks, that all makes sense. The service worker spec and impls evolved in parallel over the years and often there is a mismatch, so it's good to have confirmation that at least Firefox is matching.

https://crbug.com/chromium/808334 isn't really a blocker, it's a tracking meta bug for this class of bug (service worker allows cross-origin access).

### bu...@chromium.org (2018-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505

commit e89b9003df8c7bd7822e5b6c0a76e726a6ed1505
Author: Rob Wu <rob@robwu.nl>
Date: Fri Feb 16 19:46:08 2018

Skip Service workers in requests for mime handler plugins

BUG=808838
TEST=./browser_tests --gtest_filter=*/ServiceWorkerTest.MimeHandlerView*

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: I82e75c200091babbab648a04232db47e2938d914
Reviewed-on: https://chromium-review.googlesource.com/914150
Commit-Queue: Rob Wu <rob@robwu.nl>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#537386}
[modify] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/browser/chrome_service_worker_browsertest.cc
[modify] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/browser/extensions/service_worker_apitest.cc
[add] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/test/data/extensions/api_test/service_worker/mime_handler_view/background.js
[add] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/test/data/extensions/api_test/service_worker/mime_handler_view/manifest.json
[add] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/test/data/extensions/api_test/service_worker/mime_handler_view/mime_handler.html
[add] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/test/data/extensions/api_test/service_worker/mime_handler_view/mime_handler.js
[add] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/test/data/extensions/api_test/service_worker/mime_handler_view/page_with_embed.html
[add] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/test/data/extensions/api_test/service_worker/mime_handler_view/sw.js
[add] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/chrome/test/data/extensions/api_test/service_worker/mime_handler_view/well-known-mime.ics
[modify] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/extensions/renderer/guest_view/mime_handler_view/mime_handler_view_container.cc
[modify] https://crrev.com/e89b9003df8c7bd7822e5b6c0a76e726a6ed1505/testing/buildbot/filters/mojo.fyi.network_browser_tests.filter


### ro...@robwu.nl (2018-02-17)

Verified fixed in 66.0.3351.0 using the STR from the report.
When I look in the console, I see the following error that indicates that the request was not intercepted by the Service Worker, but handled directly by the server instead:

GET https://robwu.nl/s/service-worker-pdf/fake_same_origin 404 (Not Found)

Merge request for e89b9003df8c7bd7822e5b6c0a76e726a6ed1505. The fix itself is a single line of code, the rest of the commit are unit tests and comments.

### sh...@chromium.org (2018-02-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-17)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-17)

 awhalley@ (Security TPM) for M65 merge review.

### fa...@chromium.org (2018-02-19)

It might make sense to wait for M66, so this change and the others disabling EMBED/OBJECT requests (https://chromium-review.googlesource.com/923445 and https://chromium-review.googlesource.com/c/chromium/src/+/923663) will all be together in 66 and we can make a chromestatus.com entry saying we've done this, as it's conceivable it can break web content (I still think we should make the change and taking the risk, just not sure we need to put it in 65).

I've reached out to a Blink API owner for their thoughts.

### go...@chromium.org (2018-02-19)

M65 is very close to Stable promotion and we're only taking truly critical and safe merges in. So if this can wait for M66 will be great.

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-20)

Thanks falken@ - let's wait until 66.

### aw...@chromium.org (2018-02-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-26)

Nice one Rob, the VRP Panel decided to award $4,500 for this report.

### aw...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/808838?no_tracker_redirect=1

[Multiple monorail components: Blink>Network>FetchAPI, Blink>ServiceWorker, Internals>Plugins>PDF]
[Monorail blocked-on: crbug.com/chromium/808334]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090387)*
