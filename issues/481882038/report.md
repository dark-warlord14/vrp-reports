# Cross-origin PDF placeholder download misclassified as browser-initiated request

| Field | Value |
|-------|-------|
| **Issue ID** | [481882038](https://issues.chromium.org/issues/481882038) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | po...@gmail.com |
| **Assignee** | lu...@google.com |
| **Created** | 2026-02-05 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Cross-origin PDF placeholder download misclassified as browser-initiated request

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/>

---

### The problem

#### Please describe the technical details of the vulnerability

#### 1. technical details

When the built-in PDF viewer is disabled and an embedded PDF falls back to a
plugin placeholder with an "Open" button, the browser process initiates a
download for the embedded PDF URL via `PluginObserver::OpenPDF`. In this
code path, the download request is constructed without setting the initiator
origin, so the network stack will treat the request as browser-initiated and
omit the cross-site relationship in Fetch Metadata headers.

In the browser process, `PluginObserver::OpenPDF` creates
`download::DownloadUrlParameters` for the embedded PDF resource but never
populates the initiator origin:

```
// chromium/src/chrome/browser/plugins/plugin_observer.cc
void PluginObserver::OpenPDF(const GURL& url) {
  content::RenderFrameHost* render_frame_host =
      plugin_host_receivers_.GetCurrentTargetFrame();
  // WebViews should never trigger PDF downloads.
  if (extensions::WebViewGuest::FromRenderFrameHost(render_frame_host))
    return;

  content::Referrer referrer;
  if (!CanOpenPdfUrl(render_frame_host, url,
                     web_contents()->GetLastCommittedURL(), &referrer)) {
    return;
  }

  net::NetworkTrafficAnnotationTag traffic_annotation =
      net::DefineNetworkTrafficAnnotation("pdf_plugin_placeholder", R"(
        semantics {
          sender: "PDF Plugin Placeholder"
          description:
            "When the PDF Viewer is unavailable, a placeholder is shown for "
            "embedded PDFs. This placeholder allows the user to download and "
            "open the PDF file via a button."
          trigger:
            "The user clicks the 'View PDF' button in the PDF placeholder."
          data: "None."
          destination: WEBSITE
        }
        policy {
          cookies_allowed: NO
          setting:
            "This feature can be disabled via 'Download PDF files instead of "
            "automatically opening them in Chrome' in settings under content. "
            "The feature is disabled by default."
          chrome_policy {
            AlwaysOpenPdfExternally {
              AlwaysOpenPdfExternally: false
            }
          }
        })");
  std::unique_ptr<download::DownloadUrlParameters> params =
      std::make_unique<download::DownloadUrlParameters>(
          url,
          render_frame_host->GetRenderViewHost()
              ->GetProcess()
              ->GetDeprecatedID(),
          render_frame_host->GetRoutingID(), traffic_annotation);
  params->set_referrer(referrer.url);
  params->set_referrer_policy(
      content::Referrer::ReferrerPolicyForUrlRequest(referrer.policy));

  web_contents()->GetBrowserContext()->GetDownloadManager()->DownloadUrl(
      std::move(params));
}

```

`DownloadUrlParameters` defaults the initiator to empty unless explicitly set,
and `CreateResourceRequest` copies this value into the `network::ResourceRequest`
that is sent to the network service:

```
// chromium/src/components/download/internal/common/download_utils.cc
std::unique_ptr<network::ResourceRequest> CreateResourceRequest(
    DownloadUrlParameters* params) {
  DCHECK_GE(params->offset(), 0);

  std::unique_ptr<network::ResourceRequest> request(
      new network::ResourceRequest);
  request->method = params->method();
  request->url = params->url();
  request->request_initiator = params->initiator();
  request->trusted_params = network::ResourceRequest::TrustedParams();
  request->has_user_gesture = params->has_user_gesture();
  ...
}

```

In the network stack, the Fetch Metadata helper interprets a missing initiator
origin on a browser-initiated request as a "no site" relation and maps it to
`Sec-Fetch-Site: none`:

```
// chromium/src/services/network/sec_header_helpers.cc
std::optional<net::OriginRelation> GetInitiatorRelation(
    const net::URLRequest& request,
    base::optional_ref<const GURL> pending_redirect_url,
    const mojom::URLLoaderFactoryParams& factory_params,
    const cors::OriginAccessList& origin_access_list) {
  // Browser-initiated requests with no initiator origin will send
  // `Sec-Fetch-Site: None`.
  if (!request.initiator().has_value()) {
    // CorsURLLoaderFactory::IsValidRequest verifies that only the browser
    // process may initiate requests with no request initiator.
    DCHECK(factory_params.process_id.is_browser());

    return std::nullopt;
  }
  const url::Origin& initiator = request.initiator().value();
  ...
}

```

As a result, when a page at origin A embeds a PDF from origin B and the user
clicks the "Open" button in the PDF placeholder, the resulting download request
to origin B carries `Sec-Fetch-Site: none` even though it was actually
triggered from a cross-origin page.

#### 2. vulnerability reproduction

The PoC is provided in `web/open_pdf_none`. It simulates a page on one origin
embedding a PDF resource served from another origin using different ports on
the same IP address.

Environment:

- Build and run the browser from this repository.
- Configure the browser so that PDF files are downloaded instead of opened in
  the built-in PDF viewer (for example via the PDF documents content setting).

Steps:

1. In a terminal, start both the attacker and PDF servers:
   
   - `cd web/open_pdf_none`
   - `python3 run_servers.py`
2. In the browser, open the attacker page from one origin:
   
   - `http://<ip-address>:8000/attacker.html`
3. Confirm that the embedded PDF area shows a gray placeholder with an "Open"
   style button instead of an inline PDF viewer.
4. Click the "Open" button inside the placeholder to trigger the download of
   the cross-origin `target.pdf`.
5. Observe the server output from `run_servers.py` for the request on port
   8001. A typical log shows:
   
   ```
   === incoming request on 8001 ===
   PATH: /target.pdf
   Host: localhost:8001
   Sec-Fetch-Site: none
   Sec-Fetch-Mode: navigate
   Sec-Fetch-Dest: empty
   Referer: http://<ip-address>:8000/
   User-Agent: ...
   ...
   =================================
   
   ```

This demonstrates that a request to the PDF origin (port 8001) is triggered
from a different origin (port 8000) but still carries `Sec-Fetch-Site: none`
instead of being classified as a cross-site request.

#### Impact analysis

Any web origin that can cause the browser to render the PDF plugin placeholder
for an embedded cross-origin PDF (for example by embedding a PDF from a
different host or port while PDF viewing is disabled) can trigger this
behavior. When a user clicks the placeholder's "Open" button, the browser
initiates a download to the cross-origin PDF URL with `Sec-Fetch-Site: none`,
even though the request was indirectly triggered by the embedding page.

Servers that rely on Fetch Metadata, and specifically on rejecting
`Sec-Fetch-Site: cross-site` for sensitive download or export endpoints, may
incorrectly treat these requests as if they were direct browser navigations
without a web initiator. This allows an embedding site to drive a user's
browser to access cross-origin PDF download or export endpoints that would
otherwise be blocked by stricter Fetch Metadata-based policies, potentially
undermining access control or CSRF-like protections that depend on accurate
site relationship classification.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7666.1/stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Cross-site request forgery (CSRF)

#### How would you like to be publicly acknowledged for your report?

Povcfe of Tencent Security Xuanwu Lab

## Attachments

- [open_pdf_none.mp4](attachments/open_pdf_none.mp4) (video/mp4, 2.1 MB)
- [open_pdf_none.zip](attachments/open_pdf_none.zip) (application/x-zip-compressed, 3.0 KB)

## Timeline

### po...@gmail.com (2026-02-05)

#### patch

```
diff --git a/chromium/src/chrome/browser/plugins/plugin_observer.cc b/chromium/src/chrome/browser/plugins/plugin_observer.cc
index 1111111111..2222222222 100644
--- a/chromium/src/chrome/browser/plugins/plugin_observer.cc
+++ b/chromium/src/chrome/browser/plugins/plugin_observer.cc
@@ -49,6 +49,7 @@ void PluginObserver::OpenPDF(const GURL& url) {
   content::RenderFrameHost* render_frame_host =
       plugin_host_receivers_.GetCurrentTargetFrame();
   // WebViews should never trigger PDF downloads.
   if (extensions::WebViewGuest::FromRenderFrameHost(render_frame_host))
     return;
@@ -77,6 +78,7 @@ void PluginObserver::OpenPDF(const GURL& url) {
               ->GetProcess()
               ->GetDeprecatedID(),
           render_frame_host->GetRoutingID(), traffic_annotation);
   params->set_referrer(referrer.url);
   params->set_referrer_policy(
       content::Referrer::ReferrerPolicyForUrlRequest(referrer.policy));
+  params->set_initiator(render_frame_host->GetLastCommittedOrigin());
 
   web_contents()->GetBrowserContext()->GetDownloadManager()->DownloadUrl(
       std::move(params));

```

### xi...@chromium.org (2026-02-05)

Thanks for the report. +lukasza@, it seems that you have fixed a similar issue in the past (<https://crbug.com/40108622>). Could you take a look?

### ch...@google.com (2026-02-06)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-06)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  main  

Author:  Lukasz Anforowicz [lukasza@chromium.org](mailto:lukasza@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7560378>

Construct `DownloadUrlParameters` directly from `RenderFrameHost`.

---


Expand for full commit details

```Construct `DownloadUrlParameters` directly from `RenderFrameHost`.

```
Before this CL, callers of the frame `DownloadUrlParameters` constructor 
had to "manually" get frame's process ID, and the routing ID. 
Additionally the callers had to consider whether a call to 
`set_initiator` may also be needed.  The downside of this was code 
duplication, and risk that the IDs and the initiator won't be correctly 
computed based on the frame. 
 
After this CL, the callers can call a new method of `RenderFrameHost` 
takes care of computing the IDs and the initiator. 
 
The refactoring in this CL has the following impact on the behavior of 
callsites that construct `DownloadUrlParameters`: 
 
* `chrome/browser/extensions/webstore_installer.cc`, 
  `content/browser/download/drag_download_file.cc`, 
  `content/browser/renderer_host/render_frame_host_impl.cc`, and 
  `content/browser/web_contents/web_contents_impl.cc` 
    - No change in behavior 
* `chrome/browser/extensions/api/downloads/downloads_api.cc` 
    - Before the CL: initiator wasn't set 
    - After the CL: initiator set based on `rfh`, or (when no frame 
      in scenarios handling service worker of an extension) to the 
      extension origin 
* `chrome/browser/plugins/plugin_observer.cc`, 
  `content/browser/download/download_browsertest.cc`, and 
  `content/browser/download/download_request_utils.cc` 
    - Before the CL: initiator wasn't set 
    - After the CL: initiator set based on `render_frame_host`. 
      This addresses https://crbug.com/481882038 and its potential 
      variants. 
* `chrome/browser/renderer_context_menu/render_view_context_menu.cc` 
    - Before the CL: initiator set based on `params_.frame_url` 
    - After the CL: initiator set based on `render_frame_host`. 
      This addresses a TODO. 
* `chrome/browser/ui/webui/downloads/downloads_dom_handler.cc` 
    - Before the CL: initiator set to `chrome://downloads` 
    - After the CL: replaying initiator of `download::DownloadItem` 
      (matching the comment) 
 
Fixed: 481882038 
Change-Id: Ie6680252643b9c82cf07f7169c8d4c3abfdc0c17 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7560378 
Reviewed-by: Min Qin <qinmin@chromium.org> 
Reviewed-by: Emilia Paz <emiliapaz@chromium.org> 
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org> 
Reviewed-by: Avi Drissman <avi@chromium.org> 
Reviewed-by: Nasko Oskov <nasko@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1587495}

```
```

---

Files:
* M       `chrome/browser/extensions/api/downloads/downloads_api.cc`
* M       `chrome/browser/extensions/webstore_installer.cc`
* M       `chrome/browser/plugins/plugin_observer.cc`
* M       `chrome/browser/renderer_context_menu/render_view_context_menu.cc`
* M       `chrome/browser/ui/webui/downloads/downloads_dom_handler.cc`
* M       `components/download/public/common/download_url_parameters.cc`
* M       `components/download/public/common/download_url_parameters.h`
* M       `content/browser/download/download_browsertest.cc`
* M       `content/browser/download/download_request_utils.cc`
* M       `content/browser/download/drag_download_file.cc`
* M       `content/browser/renderer_host/render_frame_host_impl.cc`
* M       `content/browser/renderer_host/render_frame_host_impl.h`
* M       `content/browser/web_contents/web_contents_impl.cc`
* M       `content/public/browser/render_frame_host.h`

---

Hash: [ad6cd119f61bec193122b7e082810fdee06d1e49](https://chromiumdash.appspot.com/commit/ad6cd119f61bec193122b7e082810fdee06d1e49)\
Date: Fri Feb 20 00:07:36 2026

</details>

---

```

### ts...@google.com (2026-03-11)

Impact is minimal because: You should not rely solely on Sec-Fetch-Site headers to prevent the export of controlled documents. While they are a valuable defense-in-depth mechanism against cross-origin attacks, they are not a complete solution on their own and should be part of a layered security strategy. 


### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Exploitation Mitigation Bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/481882038)*
