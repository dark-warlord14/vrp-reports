# Security: UAF in ProtocolHandlerThrottle using PlzDedicatedWorker

| Field | Value |
|-------|-------|
| **Issue ID** | [40058379](https://issues.chromium.org/issues/40058379) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Loader, Blink>Workers |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2021-12-31 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

When spawning a dedicated worker, WorkerScriptFetcher::CreateScriptLoader would be invoked and calls to CreateContentBrowserURLLoaderThrottles that creates several throttles [1]. These throttles are owned by WorkerScriptFetcher, and the comment says the fetcher is responsible for deleting itself at proper time [2].

One of these throttles is ProtocolHandlerThrottle, and it stores a raw pointer to ProtocolHandlerRegistry [3]. ProtocolHandlerRegistry is a KeyedService that will be freed if the BrowserContext is gone. When the fetcher receive a redirect response from web server, it will call to ProtocolHandlerThrottle::WillRedirectRequest, and if ProtocolHandlerRegistry has already been freed at this time due to browser Profile destruction, the codes would access the dangling pointer to ProtocolHandlerRegistry at [4], thus causing UAF.

NOTE:  

This bug is similar to [crbug.com/1283544](https://crbug.com/1283544), but I file two seperate issue because the code path to trigger UAF exist in two separate modules. And the possible fix is to use some smart pointers to manage those URLLoaders ownership instead of making them self-owned.

```
base::RepeatingCallback<WebContents\*()> wc_getter =  
    base::BindRepeating([]() -> WebContents\* { return nullptr; });  
std::vector<std::unique_ptr<blink::URLLoaderThrottle>> throttles =  
    CreateContentBrowserURLLoaderThrottles(        // ===> [1]  
        \*resource_request, browser_context, wc_getter,  
        nullptr /\* navigation_ui_data \*/,  
        RenderFrameHost::kNoFrameTreeNodeId);  
  
// This fetcher will delete itself. See the class level comment.  
auto\* script_fetcher = new WorkerScriptFetcher(    // ===> [2]  
    std::make_unique<WorkerScriptLoaderFactory>(  
        worker_process_id, worker_token, trusted_isolation_info,  
        service_worker_handle, browser_context_getter,  
        std::move(url_loader_factory), worker_source_id),  
    std::move(resource_request),  
    base::BindOnce(DidCreateScriptLoader, std::move(callback),  
                    std::move(subresource_loader_factories),  
                    initial_request_url));  
script_fetcher->Start(std::move(throttles));  
  
class ProtocolHandlerThrottle : public blink::URLLoaderThrottle {  
 // skip...  
 private:  
  void TranslateUrl(GURL\* url) {  
    if (!protocol_handler_registry_->IsHandledProtocol(url->scheme()))   // ===> [4]  
      return;  
    GURL translated_url = protocol_handler_registry_->Translate(\*url);  
    if (!translated_url.is_empty())  
      \*url = translated_url;  
  }  
  
  raw_ptr<custom_handlers::ProtocolHandlerRegistry> protocol_handler_registry_; // ===> [3]  
};  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/worker_script_fetcher.cc;l=405;drc=7b628df4aeff8da0d9f94f01632d08e0d5a0b7ea>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/worker_script_fetcher.cc;l=417;drc=7b628df4aeff8da0d9f94f01632d08e0d5a0b7ea>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=4542;drc=ed107284677e5a88e9356b8a6f10010f8be1d855>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=4571;drc=ed107284677e5a88e9356b8a6f10010f8be1d855>

**VERSION**  

I tested the poc on version 99.0.4763.1

**REPRODUCTION CASE**

1. Setup a HTTP server using nodejs  
   
   node ./server.js
2. Run following command, the browser should crash in a few seconds  
   
   out/Asan/chrome --user-data-dir=/tmp/xxx/ --enable-features=PlzDedicatedWorker <http://localhost:8000/poc.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log for details

## Attachments

- poc.html (text/plain, 250 B)
- server.js (text/plain, 673 B)
- asan.log (text/plain, 24.9 KB)

## Timeline

### [Deleted User] (2021-12-31)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-01-04)

Yes we might dupe this into  crbug.com/1283544, but for now CC'ing the same people.

[Monorail components: Blink>Workers]

### [Deleted User] (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### ba...@chromium.org (2022-01-06)

I guess that it's better to fix CreateContentBrowserURLLoaderThrottles() so that throttles can be aware of BrowserContext destruction, rather than fixing UAF in service/dedicated workers.

kouhei@, nhiroki@: Do you have any ideas to fix it from loading team's perspective?

Let me tentatively assign this to kouhei@ to route this bug to an appropriate owner.

[Monorail components: Blink>Loader]

### ko...@chromium.org (2022-01-12)

asamidoi: Would you take a look? (PlzDedicatedWorker)

### as...@chromium.org (2022-01-12)

Thank you for filing this!

This is just a quick guess. My refactoring CL may have changed the lifetime of WorkerScriptFetcher and it causes this bug.
https://chromium-review.googlesource.com/c/chromium/src/+/3110167

### nh...@chromium.org (2022-01-20)

[Empty comment from Monorail migration]

### ra...@chromium.org (2022-01-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a

commit 4ab4f4f136e755d5979b8c59dfc62692f2d7c23a
Author: Asami Doi <asamidoi@chromium.org>
Date: Tue Jan 25 15:30:28 2022

Revert "PlzDedicatedWorker: Enable feature with modified expectation files"

This reverts commit c8900237101eff877c5eee2c1b17928c7f1abab9.

Reason for revert: https://bugs.chromium.org/p/chromium/issues/detail?id=1283546 and https://buganizer.corp.google.com/issues/214777310

Original change's description:
> PlzDedicatedWorker: Enable feature with modified expectation files
>
> This CL does:
> - move expectation files in /web_tests/virtual/plz-dedicated-worker
> to the non-virtual directory.
> - delete dedicated-worker-service-worker-interception.html that is not
> spec-compatible behavior which was added at
> https://chromium-review.googlesource.com/c/chromium/src/+/1059979
> - delete dedicated-worker-reporting.html because COEP reports are sent
> to worker's ReportingObserver API after PlzDedicatedWorker. Before
> PlzDedicatedWorker, reports are sent to ancestor frame's
> ReportingObserver but it's not spec compatible.
> - delete use-counter-out-of-scope-worker.html, which was used for
> measuring the impact of PlzDedicatedWorker ship for intent-to-ship.
> - update "resource.type: other" to "resource.type: script".
> - delete/merge "virtual/plz-dedicated-worker" expectation lines in
> TestExpectations.
>
> I'll delete third_party/blink/web_tests/virtual/plz-dedicated-worker/
> directory in another CL.
>
> Bug: 906991
> Change-Id: I71729be21bf6358004d0ce4afae4b30e0f20c176
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3260679
> Reviewed-by: Koji Ishii <kojii@chromium.org>
> Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
> Commit-Queue: Asami Doi <asamidoi@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#958472}

Bug: 906991, 1283546, b/214777310
Change-Id: I477c24bbc6f6e8c5e6588626308fb72648aabed6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3410433
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Auto-Submit: Asami Doi <asamidoi@chromium.org>
Reviewed-by: Titouan Rigoudy <titouan@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#962996}

[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/service-worker-interception-static-import-worker.js
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/scope2/empty.js
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/use-counter-out-of-scope-worker.html
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/common/features.cc
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/service-workers/service-worker/clients-get-client-types.https-expected.txt
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/devtools/network/network-worker-fetch-expected.txt
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/fast/workers/sandbox-origin-setup-crash-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/security/cross-origin-embedder-policy/resources/empty-coep.php
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/devtools/network/network-worker-fetch-parallel-expected.txt
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/chrome/browser/net/private_network_access_browsertest.cc
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/service-worker-interception-dynamic-import-worker.js
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/devtools/network/network-worker-fetch-blocked-expected.txt
[delete] https://crrev.com/51889e820250eccc127d9413684f9c8b37e7dd10/third_party/blink/web_tests/wpt_internal/origin_trials/coep_credentialless/driver-without-coep.https-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/html/cross-origin-embedder-policy/dedicated-worker-cache-storage.https-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/dedicated-worker-service-worker-interception.html
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/content/browser/renderer_host/private_network_access_browsertest.cc
[delete] https://crrev.com/51889e820250eccc127d9413684f9c8b37e7dd10/third_party/blink/web_tests/external/wpt/service-workers/service-worker/clients-matchall-frozen.https-expected.txt
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/service-workers/service-worker/worker-interception-redirect.https-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/new-worker-window.html
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/html/cross-origin-embedder-policy/credentialless/cache-storage.tentative.https.window_dedicated_worker-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/virtual/change-service-worker-priority-when-client-foreground-state-change/external/wpt/service-workers/service-worker/worker-interception.https-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/html/cross-origin-embedder-policy/dedicated-worker.https-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/service-workers/service-worker/clients-matchall-blob-url-worker.https-expected.txt
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/service-workers/service-worker/worker-interception.https-expected.txt
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/workers/worker-redirect-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/create-in-scope-worker.html
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/security/cross-origin-embedder-policy/dedicated-worker-reporting.html
[modify] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/service-workers/service-worker/local-url-inherit-controller.https-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/service-workers/service-worker/client-url-of-blob-url-worker.https-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/create-out-of-scope-worker.html
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/service-worker-interception-network-worker.js
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/scope1/create-out-of-scope-worker.html
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/http/tests/serviceworker/resources/service-worker-interception-service-worker.js
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/html/cross-origin-embedder-policy/credentialless/dedicated-worker.tentative.https.window-expected.txt
[add] https://crrev.com/4ab4f4f136e755d5979b8c59dfc62692f2d7c23a/third_party/blink/web_tests/external/wpt/service-workers/service-worker/dedicated-worker-service-worker-interception.https-expected.txt


### as...@chromium.org (2022-01-26)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-27)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6dc87207095542e5562044c8599ed3c220b5753e

commit 6dc87207095542e5562044c8599ed3c220b5753e
Author: Asami Doi <asamidoi@chromium.org>
Date: Thu Jan 27 13:22:43 2022

[M99] Revert "PlzDedicatedWorker: Enable feature with modified expectation files"

This reverts commit c8900237101eff877c5eee2c1b17928c7f1abab9.

Reason for revert: https://bugs.chromium.org/p/chromium/issues/detail?id=1283546 and https://buganizer.corp.google.com/issues/214777310

Original change's description:
> PlzDedicatedWorker: Enable feature with modified expectation files
>
> This CL does:
> - move expectation files in /web_tests/virtual/plz-dedicated-worker
> to the non-virtual directory.
> - delete dedicated-worker-service-worker-interception.html that is not
> spec-compatible behavior which was added at
> https://chromium-review.googlesource.com/c/chromium/src/+/1059979
> - delete dedicated-worker-reporting.html because COEP reports are sent
> to worker's ReportingObserver API after PlzDedicatedWorker. Before
> PlzDedicatedWorker, reports are sent to ancestor frame's
> ReportingObserver but it's not spec compatible.
> - delete use-counter-out-of-scope-worker.html, which was used for
> measuring the impact of PlzDedicatedWorker ship for intent-to-ship.
> - update "resource.type: other" to "resource.type: script".
> - delete/merge "virtual/plz-dedicated-worker" expectation lines in
> TestExpectations.
>
> I'll delete third_party/blink/web_tests/virtual/plz-dedicated-worker/
> directory in another CL.
>
> Bug: 906991
> Change-Id: I71729be21bf6358004d0ce4afae4b30e0f20c176
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3260679
> Reviewed-by: Koji Ishii <kojii@chromium.org>
> Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
> Commit-Queue: Asami Doi <asamidoi@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#958472}

(cherry picked from commit 4ab4f4f136e755d5979b8c59dfc62692f2d7c23a)

Bug: 906991, 1283546, b/214777310
Change-Id: I477c24bbc6f6e8c5e6588626308fb72648aabed6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3410433
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Auto-Submit: Asami Doi <asamidoi@chromium.org>
Reviewed-by: Titouan Rigoudy <titouan@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Camille Lamy <clamy@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#962996}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3412464
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Cr-Commit-Position: refs/branch-heads/4844@{#78}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/service-worker-interception-static-import-worker.js
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/scope2/empty.js
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/use-counter-out-of-scope-worker.html
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/common/features.cc
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/service-workers/service-worker/clients-get-client-types.https-expected.txt
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/devtools/network/network-worker-fetch-expected.txt
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/fast/workers/sandbox-origin-setup-crash-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/security/cross-origin-embedder-policy/resources/empty-coep.php
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/devtools/network/network-worker-fetch-parallel-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/service-worker-interception-dynamic-import-worker.js
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/chrome/browser/net/private_network_access_browsertest.cc
[delete] https://crrev.com/a550d849b53b21967e555606d3c90e68fd433ecc/third_party/blink/web_tests/wpt_internal/origin_trials/coep_credentialless/driver-without-coep.https-expected.txt
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/devtools/network/network-worker-fetch-blocked-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/html/cross-origin-embedder-policy/dedicated-worker-cache-storage.https-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/dedicated-worker-service-worker-interception.html
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/content/browser/renderer_host/private_network_access_browsertest.cc
[delete] https://crrev.com/a550d849b53b21967e555606d3c90e68fd433ecc/third_party/blink/web_tests/external/wpt/service-workers/service-worker/clients-matchall-frozen.https-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/new-worker-window.html
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/service-workers/service-worker/worker-interception-redirect.https-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/html/cross-origin-embedder-policy/credentialless/cache-storage.tentative.https.window_dedicated_worker-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/virtual/change-service-worker-priority-when-client-foreground-state-change/external/wpt/service-workers/service-worker/worker-interception.https-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/service-workers/service-worker/clients-matchall-blob-url-worker.https-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/html/cross-origin-embedder-policy/dedicated-worker.https-expected.txt
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/service-workers/service-worker/worker-interception.https-expected.txt
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/workers/worker-redirect-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/create-in-scope-worker.html
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/security/cross-origin-embedder-policy/dedicated-worker-reporting.html
[modify] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/service-workers/service-worker/local-url-inherit-controller.https-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/service-workers/service-worker/client-url-of-blob-url-worker.https-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/create-out-of-scope-worker.html
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/service-worker-interception-network-worker.js
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/scope1/create-out-of-scope-worker.html
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/http/tests/serviceworker/resources/service-worker-interception-service-worker.js
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/html/cross-origin-embedder-policy/credentialless/dedicated-worker.tentative.https.window-expected.txt
[add] https://crrev.com/6dc87207095542e5562044c8599ed3c220b5753e/third_party/blink/web_tests/external/wpt/service-workers/service-worker/dedicated-worker-service-worker-interception.https-expected.txt


### as...@chromium.org (2022-01-28)

Revert CLs were landed to ToT and M99.

### [Deleted User] (2022-01-28)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-01)

The reverted CL https://crrev.com/c/3260679 isn't present in M96 so marking as not applicable.

### wf...@chromium.org (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-02-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-04)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. Thanks for you for this report and excellent finding! 

### am...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7f28b068d62936c56bd3846fec401bbf55a0422c

commit 7f28b068d62936c56bd3846fec401bbf55a0422c
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Tue Nov 15 23:32:11 2022

DanglingPtr: Prevent ProtocolHandlerThrottle from having a dangling ptr

This CL prevents ProtocolHandlerThrottle from having a dangling ptr to
ProtocolHandlerRegistry by replacing raw_ptr with base::WeakPtr.

Bug: 1283546, 1291138
Change-Id: I939525e99c79a16a221eb696357ddde8e86fc9a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4028756
Reviewed-by: Javier Fernandez <jfernandez@igalia.com>
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1071905}

[modify] https://crrev.com/7f28b068d62936c56bd3846fec401bbf55a0422c/components/custom_handlers/protocol_handler_registry.cc
[modify] https://crrev.com/7f28b068d62936c56bd3846fec401bbf55a0422c/components/custom_handlers/protocol_handler_registry.h
[modify] https://crrev.com/7f28b068d62936c56bd3846fec401bbf55a0422c/components/custom_handlers/protocol_handler_throttle.h
[modify] https://crrev.com/7f28b068d62936c56bd3846fec401bbf55a0422c/components/custom_handlers/protocol_handler_throttle.cc


### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1283546?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Blink>Workers]
[Monorail blocking: crbug.com/chromium/906991]
[Monorail mergedwith: crbug.com/chromium/1283544]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058379)*
