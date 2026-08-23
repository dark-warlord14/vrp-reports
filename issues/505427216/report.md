# Service Worker Static Routing API cache source bypasses CORP in crossOriginIsolated context (fix wiring ineffective)

| Field | Value |
|-------|-------|
| **Issue ID** | [505427216](https://issues.chromium.org/issues/505427216) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | yy...@chromium.org |
| **Created** | 2026-04-23 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

The CORP enforcement that commit `e2b91876eb013` ([crbug/497436273](https://crbug.com/497436273)) added for the Service Worker Static Routing API `cache` source is wired incorrectly and does not actually block cross-origin responses. Enabling `kServiceWorkerStaticRouterCORPCheck` (and, for completeness, `kServiceWorkerStaticRouterOpaqueCheck`) has no effect on the subresource-embed bypass. A page in a crossOriginIsolated (COEP:require-corp) context can embed a cross-origin credentialed opaque response whose bytes were stored by a Service Worker via `cache.put(...)` and routed through the Static Routing API cache source.

Root cause: `content/common/service_worker/service_worker_resource_loader.cc:99-106` passes `resource_request.url` as both the `request_url` and `original_url` arguments to `network::CrossOriginResourcePolicy::IsBlockedByHeaderValue`:

```
if (network::CrossOriginResourcePolicy::IsBlockedByHeaderValue(
        resource_request.url, resource_request.url,
        resource_request.request_initiator, corp_header_value,
        resource_request.mode, resource_request.destination,
        response->request_include_credentials, cross_origin_embedder_policy,
        is_enabled ? cross_origin_embedder_policy_reporter : nullptr,
        document_isolation_policy,
        is_enabled ? document_isolation_policy_reporter : nullptr)) {

```

`resource_request.url` is the SW-chosen cache key URL (for example `a.test/service_worker/x`), which is same-origin to the document because the attacker controls both the SW and the page. The CORP logic at `services/network/public/cpp/cross_origin_resource_policy.cc:184-186` then derives `target_origin` from `request_url` and returns `std::nullopt` (allowed) on the same-origin short-circuit:

```
url::Origin target_origin = url::Origin::Create(request_url);
if (initiator == target_origin)
  return std::nullopt;

```

The check should compare the response's actual origin. The general CacheStorage CORP check at `content/browser/cache_storage/cache_storage_dispatcher_host.cc:169-176` does this correctly:

```
return CrossOriginResourcePolicy::IsBlockedByHeaderValue(
           response->url_list.back(), response->url_list.front(),
           document_origin, corp_header_value, RequestMode::kNoCors,
           ...)

```

With the SW Static Router path using `resource_request.url` instead, the added CORP flag is a no-op for the cache source. A compromised origin in a crossOriginIsolated context still embeds cross-origin credentialed no-CORP responses as subresources, defeating the exact protection CORP was designed to enforce in COEP contexts against Spectre-style reads.

Scope distinction from the previously-addressed class: the surrounding issue family (static router cache source needs CORP/opaque enforcement) is tracked at [crbug/495999481](https://crbug.com/495999481) and [crbug/497436273](https://crbug.com/497436273). This report is not the class-level discovery. It is a defect in the CORP fix implementation that ships in current main. Turning the flag on via Finch would not close the bypass.

Reachability:

- Attacker controls origin `attacker.example`.
- Attacker's page sets `Cross-Origin-Embedder-Policy: require-corp` and `Cross-Origin-Opener-Policy: same-origin`, reaches `window.crossOriginIsolated === true`.
- Attacker SW does `fetch(victim, {mode: 'no-cors', credentials: 'include'})` and stores the opaque response in a cache.
- Attacker SW registers a router rule mapping a same-origin URL to the cache source.
- Attacker page embeds the same-origin URL as an `<img>`. The image loads. `naturalWidth` and `naturalHeight` are readable cross-origin.

With all fix flags enabled, the same attack succeeds.

Capability uplift:

1. Cross-origin credentialed image dimensions are directly readable, defeating the CORP protection Chrome is rolling out.
2. crossOriginIsolated context exposes SharedArrayBuffer and precise timers. CORP blocks cross-origin content from entering this process for Spectre-defence reasons. The bypass reopens Spectre-style side channels against any cross-origin resource the attacker chooses to cache.

VERSION

Chrome Version: built from main branch 2026-04-23, `out/fuzz_asan` with `is_asan=true`, commit tree at HEAD.
Operating System: Linux (debian bullseye sysroot), x86\_64.

REPRODUCTION CASE
REPRODUCTION CASE

Two attached files drive an end-to-end repro against stable Chrome. No Chromium build required.

Attached files:

- `POC-sw-static-router-CORP-bypass.html` — attacker client page + driver script (origin A).
- `POC-sw-static-router-CORP-bypass.sw.js` — Service Worker script, saved as `sw.js` at origin A web root.

Setup (two distinct secure origins mapped to loopback):

1. Create web roots and drop the attached files:
   
   ```
   mkdir -p /tmp/sw-poc/a /tmp/sw-poc/b
   cp POC-sw-static-router-CORP-bypass.html    /tmp/sw-poc/a/index.html
   cp POC-sw-static-router-CORP-bypass.sw.js   /tmp/sw-poc/a/sw.js
   # any 100x50 PNG works — keep the dimensions small so the leak is visible
   convert -size 100x50 xc:red /tmp/sw-poc/b/animated.png
   
   ```
2. Generate a self-signed cert with SANs for both hostnames:
   
   ```
   openssl req -x509 -newkey rsa:2048 -nodes -days 30 \
     -keyout /tmp/sw-poc/key.pem -out /tmp/sw-poc/cert.pem \
     -subj /CN=a.test \
     -addext 'subjectAltName = DNS:a.test, DNS:b.test'
   
   ```
3. Start origin A (COEP/COOP only on HTML; `sw.js` MUST NOT carry COEP or the worker inherits it and cannot fetch cross-origin):
   
   ```
   # /tmp/sw-poc/server_a.py
   import http.server, ssl
   class H(http.server.SimpleHTTPRequestHandler):
       def __init__(self, *a, **k): super().__init__(*a, directory='/tmp/sw-poc/a', **k)
       def end_headers(self):
           if self.path in ('/', '/index.html') or self.path.endswith('.html'):
               self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
               self.send_header('Cross-Origin-Opener-Policy',   'same-origin')
           super().end_headers()
   s = http.server.ThreadingHTTPServer(('0.0.0.0', 4443), H)
   ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
   ctx.load_cert_chain('/tmp/sw-poc/cert.pem', '/tmp/sw-poc/key.pem')
   s.socket = ctx.wrap_socket(s.socket, server_side=True); s.serve_forever()
   
   ```
4. Start origin B (no CORP header on the victim image):
   
   ```
   # /tmp/sw-poc/server_b.py — identical to server_a but directory=/tmp/sw-poc/b,
   # port 4444, and empty end_headers() (no COEP/COOP/CORP).
   
   ```
5. Launch Chrome against the loopback cert:
   
   ```
   google-chrome \
     --ignore-certificate-errors \
     --host-resolver-rules='MAP a.test 127.0.0.1, MAP b.test 127.0.0.1' \
     --user-data-dir=/tmp/sw-poc-profile \
     https://a.test:4443/
   
   ```
   
   `--ignore-certificate-errors` is required because Service Worker subresource fetches fail silently against untrusted certs (no interstitial bypass path inside the SW). `mkcert` + OS trust store works too.
6. In the browser: enter `https://b.test:4444/animated.png` as the victim URL and click **Run POC**. On first run the SW registers but is not yet controlling; reload the page once to finish controlling, then click Run POC again.

Expected output (runtime-confirmed on stable Chrome, 2026-04-23, all fix flags enabled via `--enable-features=ServiceWorkerStaticRouterOpaqueCheck,ServiceWorkerStaticRouterCORPCheck`):

```
isolation = {"crossOriginIsolated":true,"isSecureContext":true}

[1] register sw.js?https%3A%2F%2Fb.test%3A4444%2Fanimated.png
    SW installed + controlling

[2] control: direct <img src="https://b.test:4444/animated.png">
    {"status":"error"}

[3] attack: <img src="/service_worker/x"> (router -> cache -> victim)
    {"status":"loaded","naturalWidth":100,"naturalHeight":50}

VERDICT
    CORP BYPASS CONFIRMED — cross-origin opaque bytes embedded
    leaked dimensions: 100x50

```

DevTools network panel shows the control request blocked as
`ERR_BLOCKED_BY_RESPONSE.NotSameOriginAfterDefaultedToSameOriginByCoep` — the exact CORP defence the attack sidesteps.

Interpretation:

- `crossOriginIsolated=true` confirms the COEP context is active.
- Control (direct cross-origin `<img>`) fails with the standard CORP / defaulted-to-same-origin-by-COEP block.
- Attack (`/service_worker/x` via router → cache → victim) loads. `naturalWidth` and `naturalHeight` expose information about the cross-origin credentialed response. Result is unchanged with both fix flags enabled.

Suggested fix: at `content/common/service_worker/service_worker_resource_loader.cc:99`, pass `response->url_list.back()` (and an appropriate entry for `original_url`) instead of `resource_request.url`, matching the pattern already used at `cache_storage_dispatcher_host.cc:169-176`.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Not a crash. Cross-origin policy bypass.

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: David Bors, Catalin Iovita

## Attachments

- [POC-sw-static-router-CORP-bypass.sw.js](attachments/POC-sw-static-router-CORP-bypass.sw.js) (text/javascript, 633 B)
- [POC-sw-static-router-CORP-bypass.html](attachments/POC-sw-static-router-CORP-bypass.html) (text/html, 9.5 KB)

## Timeline

### ca...@chromium.org (2026-04-23)

crbug.com/497436273 is not marked as fixed yet, so it's likely that the remaining cases are still pending a fix.

yyanagisawa: Can you PTAL and mark this as a duplicate if it's indeed the same root cause as crbug.com/497436273 (or help further triage if it's not)? Thanks

### yy...@chromium.org (2026-04-24)

I compared content/common/service_worker/service_worker_resource_loader.cc and third_party/blink/renderer/modules/service_worker/cross_origin_resource_policy_checker.cc, and I understand the issue exist.

### ca...@chromium.org (2026-04-24)

Thanks! I'll triage this as valid then

### ch...@google.com (2026-04-25)

Setting milestone because of s2 severity.

### ch...@google.com (2026-04-25)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-27)

Project: chromium/src  

Branch:  main  

Author:  Yoshisto Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7792123>

Fix CORP bypass in Service Worker Static Router cache source

---


Expand for full commit details
```
     
    The Service Worker Static Router's cache source was incorrectly using 
    the request URL for Cross-Origin Resource Policy (CORP) checks. 
    This allowed a same-origin alias URL to bypass CORP enforcement for 
    cross-origin responses stored in the cache. 
     
    This change updates ServiceWorkerResourceLoader::IsValidStaticRouterResponse 
    to use the actual response URL list (url_list.back() and url_list.front()) 
    for the CORP check, ensuring that cross-origin responses are correctly 
    identified and blocked when required by COEP/CORP. 
     
    Bug: 505427216 
    Change-Id: I8b555e6f23c3db8a1b8b3c6811bf4adec5bb7863 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7792123 
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org> 
    Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1620918}

```

---

Files:

- M `content/common/service_worker/service_worker_resource_loader.cc`
- M `content/common/service_worker/service_worker_resource_loader_unittest.cc`
- M `content/test/content_test_bundle_data.filelist`
- A `content/test/data/service_worker/static_router_corp.html`
- A `content/test/data/service_worker/static_router_corp.html.mock-http-headers`
- A `content/test/data/service_worker/static_router_corp.js`

---

Hash: [b67101170bed56c56034903c773a228beee0b5ef](https://chromiumdash.appspot.com/commit/b67101170bed56c56034903c773a228beee0b5ef)  

Date: Mon Apr 27 06:53:04 2026


---

### ct...@chromium.org (2026-04-28)

[shepherd] Is this a dupe of [Issue 497436273](https://issues.chromium.org/issues/497436273)?

### yy...@chromium.org (2026-04-30)

The fix provided for Issue 497436273 had an issue.  This bug pointed out that.

### dx...@google.com (2026-05-01)

Project: chromium/src  

Branch:  main  

Author:  Yoshisto Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7794699>

Strengthen security for Service Worker Static Router

---


Expand for full commit details
```
     
    This CL addresses a security vulnerability where Cross-Origin Resource 
    Policy (CORP) could be bypassed when using the Service Worker Static 
    Routing API's cache source. 
     
    1. Ensure coverage for RaceNetworkAndCache 
       The CORP check condition is expanded to include 
       kRaceNetworkAndCache. This ensures that even when the static router 
       is in race mode and the cache source wins, the resulting response 
       is correctly validated before being committed. 
       (The feature is under construction but just in case) 
     
    2. Prevent "poisoned" synthesized responses 
       A CHECK is added to ensure that synthesized responses (those with 
       an empty url_list) are never marked as kOpaque. This prevents 
       potential attack vectors where a response claims to be 
       cross-origin/opaque while hiding its actual origin. 
     
    Bug: 505427216 
    Change-Id: Ifba499a8ca5742679aef26a6d6c80416e448ff1e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7794699 
    Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1623731}

```

---

Files:

- M `content/browser/service_worker/service_worker_main_resource_loader.cc`
- M `content/common/service_worker/service_worker_resource_loader.cc`
- M `content/renderer/service_worker/service_worker_subresource_loader.cc`

---

Hash: [5046d3cddfac35b34e15bcf4afea7e85d17c30c5](https://chromiumdash.appspot.com/commit/5046d3cddfac35b34e15bcf4afea7e85d17c30c5)  

Date: Fri May 1 06:49:27 2026


---

### ch...@google.com (2026-05-01)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505427216)*
