# 	SharedWorker same-origin check bypass for chrome-extension:// — DedicatedWorker hardening (8bde565) not applied to sibling SharedWorker path

| Field | Value |
|-------|-------|
| **Issue ID** | [504073872](https://issues.chromium.org/issues/504073872) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Workers |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tr...@gmail.com |
| **Assignee** | yy...@chromium.org |
| **Created** | 2026-04-19 |
| **Bounty** | $3,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

## VULNERABILITY DETAILS

A compromised renderer hosting a `chrome-extension://` document can construct a `SharedWorker` whose main-script URL is cross-origin to the extension. The creator scheme `chrome-extension` is unconditionally whitelisted in `ChromeContentBrowserClient::DoesSchemeAllowCrossOriginSharedWorker`, bypassing the same-origin check in `SharedWorkerServiceImpl::ConnectToWorker`. The resulting bidirectional `MessagePort` enables asset exfiltration (cookies, history, bookmarks, storage) from the extension context to an attacker origin.

This is the sibling of the DedicatedWorker hardening landed 2026-04-14 (commit `8bde565f45a8baf9b84c129905eb53c9abe108d2`, *"DedicatedWorker: Enforce same-origin check for IWA and Extensions"*). The commit message explicitly scopes the hardening to *"worker-related destinations (DedicatedWorker, SharedWorker, ServiceWorker)"* but the fix only covers DedicatedWorker. ServiceWorker is safe via pre-existing `AllOriginsMatchAndCanAccessServiceWorkers`. **SharedWorker remains unpatched.**

Upstream bug reference: `crbug/496253755`.

## VERSION

**Chrome Version**:

- `147.0.7727.101` stable — SharedWorker vulnerable; DedicatedWorker also passes (pre-patch)
- Trunk `HEAD fdd8e3060ddaa` @ 2026-04-19 (contains `8bde565`) — SharedWorker vulnerable; DedicatedWorker **blocked** via `DWH_INVALID_SCRIPT_URL_ORIGIN` renderer kill

**Operating System**: Linux (Kali 6.19.11, x86\_64). Behavior is OS-independent; Linux tested.

**Reproduction rate**: 100%

## REPRODUCTION CASE

Attached files (directly, per template instructions — no archive):

- `manifest.json` — MV3 test extension
- `popup.html`
- `popup.js`
- `worker.js` — served by the attacker HTTP server
- `server.py` — python3 stdlib only, serves `/worker.js` + `POST /collect` + `GET /collected`
- `F009_shared_worker_cross_origin_extension_bypass.md` — full finding with root-cause analysis, `file:line` references, and suggested patch

### Steps

1. `python3 server.py` — listens on `127.0.0.1:8000`
2. `chrome://extensions/` → Developer mode → **Load unpacked** → select the directory containing `manifest.json` / `popup.html` / `popup.js`
3. Click the extension icon to open the popup
4. Popup log shows:
   - `[F009] cross-origin SharedWorker constructed (should have been blocked)`
   - `[F009] server confirmed receipt: [...]`
5. `curl http://127.0.0.1:8000/collected` confirms the exfiltrated payload reached the attacker origin

### Complementary DedicatedWorker control probe

Proves the patch ignores CSP and isolates the SharedWorker inconsistency.

Uncomment the block at `popup.js:36-42` (`new Worker(attacker)`) and reproduce on a trunk/Canary build. The browser process terminates the renderer:
ERROR:render\_process\_host\_impl.cc:6197] Terminating render process for bad Mojo message:
Received bad user message: DWH\_INVALID\_SCRIPT\_URL\_ORIGIN
ERROR:bad\_message.cc:29] Terminating renderer for bad IPC message, reason 123

Same URL, same manifest, same extension origin as the SharedWorker case — only the worker type differs.

### Related test coverage

`third_party/blink/web_tests/http/tests/security/cross-origin-shared-worker-allowed.html` exercises the permissive path affected by this report. Resolving F009 will require updating this test to reflect the new same-origin enforcement for `chrome-extension://` creators (or gating its current assertions behind a non-extension context).

## FOR CRASHES

N/A — not a crash. The vulnerability is a missing same-origin check enabling cross-origin data exfiltration. No memory corruption, no stack trace.

## CREDIT INFORMATION

## Reporter credit: *VEZEKA*

## Finding (full analysis)

# SharedWorker same-origin check bypass via `DoesSchemeAllowCrossOriginSharedWorker` whitelist — asset exfiltration from `chrome-extension://` context

**Reporter finding ID** : F009
**Date** : 2026-04-19
**Status** : Confirmed on Chrome Stable

---

## Summary

Chrome enforces a same-origin check on `SharedWorker` main-script URL only when the creator scheme is not in a hard-coded allowlist. The allowlist currently contains `chrome-extension://`. A compromised renderer executing within a `chrome-extension://` security context can therefore instantiate a `SharedWorker` whose main script is attacker-controlled (`https://attacker.example/worker.js`), and use the bidirectional `MessagePort` to exfiltrate data accessible from the extension context (cookies, history, bookmarks, storage) to an attacker origin.

This is the direct sibling of the DedicatedWorker hardening landed on 2026-04-14 (commit `8bde565f45a8baf9b84c129905eb53c9abe108d2`, *"DedicatedWorker: Enforce same-origin check for IWA and Extensions"*). That commit explicitly scopes the hardening to *"worker-related destinations (DedicatedWorker, SharedWorker, ServiceWorker)"*, but only the DedicatedWorker path was patched. `ServiceWorker` is protected by pre-existing same-origin enforcement (`AllOriginsMatchAndCanAccessServiceWorkers`) — `SharedWorker` is not.

## Affected versions

| Channel | Version | SharedWorker cross-origin | Sibling DedicatedWorker (control) |
| --- | --- | --- | --- |
| Stable | 147.0.7727.101 | Vulnerable (constructed + exfil) | Also passes — `8bde565` not yet shipped |
| Dev / Trunk | main @ 2026-04-19 (HEAD `fdd8e3060ddaa`, contains `8bde565`) | **Vulnerable (constructed + exfil)** | **Blocked** via `DWH_INVALID_SCRIPT_URL_ORIGIN` bad-message kill |
| Beta | to be confirmed | Expected vulnerable | Expected blocked once `8bde565` reaches Beta |

The Dev/Trunk row is the decisive evidence: on a binary that contains the DedicatedWorker hardening (`kEnforceDedicatedWorkerSameOriginCheck` is `FEATURE_ENABLED_BY_DEFAULT`), SharedWorker still constructs and exfiltrates cross-origin from a `chrome-extension://` creator under the same manifest, same attacker origin, same script URL. The inconsistency is structural, not configuration-dependent.

## Component

`Blink > Workers > SharedWorker`
`content/browser/worker_host/shared_worker_service_impl.cc`
`chrome/browser/chrome_content_browser_client.cc`

## Threat model

Compromised renderer hosting a `chrome-extension://` document. This is the exact threat model the sibling DedicatedWorker fix addresses (commit message: *"security hardening to prevent asset exfiltration from these contexts by compromised renderer processes"*). A renderer can be compromised by any V8 / Blink RCE (example recent class: `CVE-2024-xxxx` type-confusion in V8). Extensions ship to hundreds of millions of users with `host_permissions: ["<all_urls>"]` (password managers, ad blockers, shopping assistants, translators), therefore the post-compromise primitive has broad impact.

CSP is **not** a mitigation under this threat model: a compromised renderer executes native code outside CSP enforcement. The same observation justified the DedicatedWorker fix.

---

## Root cause

### Entry point

`SharedWorkerConnector.Connect` Mojo call from renderer → `SharedWorkerConnectorImpl::Connect` (`content/browser/worker_host/shared_worker_connector_impl.cc:51`) → `SharedWorkerServiceImpl::ConnectToWorker`.

### Defective check

`content/browser/worker_host/shared_worker_service_impl.cc:167-175`

```
// Enforce same-origin policy.
// data: URLs are not considered a different origin.
bool is_cross_origin = !info->url.SchemeIs(url::kDataScheme) &&
                       url::Origin::Create(info->url) != storage_key.origin();
if (is_cross_origin &&
    !GetContentClient()->browser()->DoesSchemeAllowCrossOriginSharedWorker(
        storage_key.origin().scheme())) {
  ScriptLoadFailed(std::move(client), /*error_message=*/"");
  return;
}

```

The same-origin check is bypassed whenever `DoesSchemeAllowCrossOriginSharedWorker(creator_scheme)` returns `true`.

### Defective allowlist

`chrome/browser/chrome_content_browser_client.cc:3288-3298`

```
bool ChromeContentBrowserClient::DoesSchemeAllowCrossOriginSharedWorker(
    const std::string& scheme) {
#if BUILDFLAG(ENABLE_EXTENSIONS_CORE)
  // Extensions are allowed to start cross-origin shared workers.
  if (scheme == extensions::kExtensionScheme) {
    return true;
  }
#endif
  return false;
}

```

`chrome-extension://` is unconditionally whitelisted. Any cross-origin `SharedWorker` main-script URL is accepted when the creator is an extension document.

### Why the sibling `ServiceWorker` and `DedicatedWorker` paths are safe

- **DedicatedWorker** — patched on 2026-04-14 at `content/browser/worker_host/dedicated_worker_host_factory_impl.cc:136-150` with an explicit scheme rejection (`mojo::ReportBadMessage("DWH_INVALID_SCRIPT_URL_ORIGIN")`) covering `isolated-app` and `chrome-extension`.
- **ServiceWorker** — registration goes through `AllOriginsMatchAndCanAccessServiceWorkers` in `service_worker_container_host.cc:140-150`, which requires scope, script URL, and storage key origin to match exactly. No scheme allowlist bypass exists.

`SharedWorker` is therefore the only remaining worker surface still exposing the pre-hardening behavior.

### Related surfaces audited and not vulnerable

- `isolated-app://` — not present in `DoesSchemeAllowCrossOriginSharedWorker` (only `chrome-extension`).
- Worklet hosts (`AuctionWorkletManager`, AnimationWorklet / PaintWorklet / LayoutWorklet / AudioWorklet) — no equivalent scheme-based bypass.
- `SharedStorageWorkletHost` — partitioned by `data_origin`; separate analysis required but outside this report.

---

## Reproduction

PoC is provided as separate files per the 2026-03 VRP formatting rules.

```
poc/
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
└── attacker/
    ├── server.py     # Python HTTP server (serves worker.js and /collect endpoint)
    └── worker.js     # Cross-origin SharedWorker script

```
### Steps

1. `cd poc/attacker && python3 server.py` — serves `http://127.0.0.1:8000/`.
2. In Chrome Stable 147.0.7727.101: `chrome://extensions/` → Developer mode → Load unpacked → select `poc/extension/`.
3. Note the extension id printed for reference in the report (`chrome-extension://<EXT_ID>/`).
4. Click the extension icon to open the popup.
5. Observe the popup log: cross-origin `SharedWorker` is constructed, extension-accessible data is sent via `MessagePort.postMessage`, and the server's `/collected` endpoint confirms reception.

### Observed output

```
creator origin = chrome-extension://<EXT_ID>
creator scheme = chrome-extension:
SharedWorker constructor returned without throwing
postMessage sent
worker reply: {"hello":"from attacker worker","url":"http://127.0.0.1:8000/worker.js"}
server collected endpoint: [{"exfil_secret":"...","origin":"chrome-extension://<EXT_ID>","ts":...}]

```

`self.location.href` inside the worker resolves to `http://127.0.0.1:8000/worker.js`, proving the main-script executed cross-origin without a same-origin violation.

### Caveat on the PoC manifest

The manifest contains `"content_security_policy": { "extension_pages": "script-src 'self'; object-src 'self'; worker-src http://127.0.0.1:8000" }` purely as a test-harness convenience so the PoC is driveable from a benign extension popup. Under the intended threat model (compromised renderer), CSP is bypassed natively and the permissive `worker-src` is not a precondition for exploitation. This aligns with the rationale of the DedicatedWorker fix, which does not rely on CSP either.

### Complementary validation — control vs variant on the same binary

To rule out any CSP / manifest-opt-in interpretation, the PoC was extended with a control probe that attempts `new Worker(attacker)` immediately before the SharedWorker construction, using the exact same URL, manifest, and extension origin. On a Debug build of trunk `HEAD` (contains `8bde565`, `kEnforceDedicatedWorkerSameOriginCheck` enabled by default):

```
[Test A] about to test DedicatedWorker cross-origin to: http://127.0.0.1:8000/worker.js
[Test A] new Worker() returned without JS throw
ERROR:render_process_host_impl.cc:6197] Terminating render process for bad Mojo message:
    Received bad user message: DWH_INVALID_SCRIPT_URL_ORIGIN
ERROR:bad_message.cc:29] Terminating renderer for bad IPC message, reason 123
[renderer killed — extension popup crashed]

```

In a separate run (control probe commented out), `new SharedWorker(attacker)` from the same extension popup succeeded, the worker's `self.location.href` resolved to `http://127.0.0.1:8000/worker.js`, and the attacker server's `/collected` endpoint recorded the exfiltrated payload. Only the worker type differs; DedicatedWorker is killed by the browser process, SharedWorker is not checked at all. This demonstrates the bypass is independent of CSP (the patch enforces the check server-side regardless of `worker-src`) and confirms the hardening is missing specifically on the `SharedWorker` path.

---

## Impact

Primitive: from a compromised `chrome-extension://` renderer, open a `MessagePort` to an arbitrary cross-origin script URL and exchange data bidirectionally without tripping any browser-process check.

With typical extension `host_permissions`:

| Data source | API | Exfiltrable |
| --- | --- | --- |
| Cookies (all domains) | `chrome.cookies.getAll({})` | Yes |
| Browser history | `chrome.history.search({text:""})` | Yes |
| Bookmarks | `chrome.bookmarks.getTree()` | Yes |

Classification: cross-origin data leak reachable from a compromised renderer in an extension context — Site Isolation / UXSS-class primitive.

---

## Suggested patch

Align `SharedWorkerServiceImpl::ConnectToWorker` with the DedicatedWorker hardening landed in `8bde565f45a8b`, gated by a new feature flag for staged rollout.

```
// content/browser/worker_host/shared_worker_service_impl.cc
// After the existing is_cross_origin check at line ~175:

if (base::FeatureList::IsEnabled(
        features::kEnforceSharedWorkerSameOriginCheck) &&
    !info->url.SchemeIs(url::kDataScheme)) {
  constexpr char kIsolatedAppScheme[] = "isolated-app";
  constexpr char kExtensionScheme[] = "chrome-extension";
  const std::string& creator_scheme = storage_key.origin().scheme();
  const std::string& script_scheme = url::Origin::Create(info->url).scheme();
  const bool involves_restricted_scheme =
      creator_scheme == kIsolatedAppScheme ||
      creator_scheme == kExtensionScheme ||
      script_scheme == kIsolatedAppScheme ||
      script_scheme == kExtensionScheme;
  if (involves_restricted_scheme &&
      url::Origin::Create(info->url) != storage_key.origin()) {
    bad_message::ReceivedBadMessage(
        host, bad_message::SWSI_CROSS_ORIGIN_SCRIPT_URL);
    return;
  }
}

```

Alternative, more surgical: drop `chrome-extension` from `DoesSchemeAllowCrossOriginSharedWorker`. This carries a small risk of breaking Manifest V2 extensions relying on cross-origin `SharedWorker`; the feature-flag approach is recommended.

A new `bad_message` enum entry (e.g. `SWSI_CROSS_ORIGIN_SCRIPT_URL`) should be added to `content/browser/bad_message.h`, mirroring `DWH_INVALID_SCRIPT_URL_ORIGIN`.

---

## Bisect

The permissive behavior has existed as long as `DoesSchemeAllowCrossOriginSharedWorker` has whitelisted `chrome-extension` (predates the current main branch history window; introduced for Manifest V2 compatibility). The defect became security-relevant on 2026-04-14 when the sibling DedicatedWorker path was hardened, creating an inconsistency in the worker security posture.

- Hardening commit (reference): `8bde565f45a8baf9b84c129905eb53c9abe108d2` — *"DedicatedWorker: Enforce same-origin check for IWA and Extensions"* — `refs/heads/main@{#1614854}`.
- Vulnerable code path (SharedWorker): present at main `HEAD` as of 2026-04-19.

---

## References

- Sibling fix: `8bde565f45a8baf9b84c129905eb53c9abe108d2`
- DedicatedWorker enforcement: `content/browser/worker_host/dedicated_worker_host_factory_impl.cc:136-150`
- ServiceWorker pre-existing protection: `content/browser/service_worker/service_worker_container_host.cc:140-150` → `AllOriginsMatchAndCanAccessServiceWorkers`
- Defective allowlist: `chrome/browser/chrome_content_browser_client.cc:3288-3298`
- Defective check site: `content/browser/worker_host/shared_worker_service_impl.cc:167-175`

---

## Reporter notes

- PoC verified on 2026-04-19 (Linux Kali 6.19.11, x86\_64) against:
  - **Chrome Stable 147.0.7727.101** (Google-signed binary): SharedWorker cross-origin from `chrome-extension://` constructed + exfil reached attacker origin. DedicatedWorker also passes (pre-patch baseline — `8bde565` not yet shipped to Stable).
  - **Chrome Dev / `google-chrome-unstable` 149.0.7795.2** (Google-signed binary): same SharedWorker behavior observed.
  - **Local Debug build of trunk `HEAD fdd8e3060ddaa`** (contains `8bde565`, `kEnforceDedicatedWorkerSameOriginCheck = FEATURE_ENABLED_BY_DEFAULT`): SharedWorker cross-origin still constructs and exfiltrates; DedicatedWorker cross-origin triggers `mojo::ReportBadMessage("DWH_INVALID_SCRIPT_URL_ORIGIN")` and terminates the renderer (`render_process_host_impl.cc:6197`, bad\_message reason 123). Captured in the same run, same PID, within ~5 ms — isolating worker type as the only variable.
- Evidence attached to the tracker issue:
  - `kill_signature.txt` — 4-line extract of the DedicatedWorker kill + SharedWorker construction.
  - `trunk_debug_kill_context.log` — 71-line context window around the kill event.
  - `attacker_collected.json` — full dump of the attacker server's `/collected` endpoint.
  - `trunk_debug_both_workers.log` / `trunk_debug_dedicated_worker_kill.log` — full stderr logs (6.2–6.6 MB each) available on request.
  - Screenshots of the extension popup log, the `/collected` response, and the Chromium renderer-crash notification triggered by the DedicatedWorker bad-message kill.
- No third-party code is involved.
- No embargo requested.

## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 465 B)
- [popup.html](attachments/popup.html) (text/html, 210 B)
- [popup.js](attachments/popup.js) (text/javascript, 2.7 KB)
- [server.py](attachments/server.py) (text/x-python, 2.3 KB)
- [worker.js](attachments/worker.js) (text/javascript, 701 B)
- [attacker_collected.json](attachments/attacker_collected.json) (application/json, 4.3 KB)
- [kill_signature.txt](attachments/kill_signature.txt) (text/plain, 995 B)
- [trunk_debug_kill_context.log](attachments/trunk_debug_kill_context.log) (text/plain, 15.1 KB)
- [poc.zip](attachments/poc.zip) (application/zip, 4.1 KB)

## Timeline

### ar...@google.com (2026-04-20)

The poc.zip described above.

### ar...@google.com (2026-04-20)

I can reproduce

> [EXFIL RECEIVED] {'origin': 'chrome-extension://fhmdnpfodpnkpiaimepoohpfjkddfhhp', 'scheme': 'chrome-extension:', 'cookies\_count': 20,

The problem is the the extension being able to open a cross-origin sharedworker.

This is a variation of [bug 496239657](https://issues.chromium.org/issues/496239657), but instead of a DedicatedWorker, we are using a SharedWorker. I am assigning from previous owner.

### tr...@gmail.com (2026-04-20)

Bisect update for the VRP record:

Introducer commit: 6cb099a05fab9553bb6e705362032ee4bb79d82f

Author: Patrick Monette [pmonette@chromium.org](mailto:pmonette@chromium.org)

Date: 2019-09-18

Subject: "Enforce same-origin policy for shared workers in the browser process"

Bug ref: [crbug.com/1004324](https://crbug.com/1004324)

Gerrit: <https://chromium-review.googlesource.com/c/chromium/src/+/1804513>

Change-Id: I85a80a8d590c44f2f23659bbafb79c6c3b83e059

Position: refs/heads/master@{#697723}

That commit introduced both the same-origin enforcement and the
chrome-extension:// allowlist carve-out (DoesSchemeAllowCrossOriginSharedWorker,
chrome/browser/chrome\_content\_browser\_client.cc:2446-2457 in the original diff).
The carve-out has been in place unchanged since 2019.

Reproducible:
git log --all --oneline -S "DoesSchemeAllowCrossOriginSharedWorker"   

-- chrome/browser/chrome\_content\_browser\_client.cc
→ 6cb099a05fab9 (single result)

### ch...@google.com (2026-04-21)

Setting milestone because of s2 severity.

### dx...@google.com (2026-04-27)

Project: chromium/src  

Branch:  main  

Author:  Yoshisto Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7784632>

SharedWorker: Enforce same-origin check for IWA and Extensions

---


Expand for full commit details
```
     
    This is a security hardening to prevent asset exfiltration from 
    extension and Isolated Web App (IWA) contexts by compromised renderer 
    processes. 
     
    A compromised renderer hosting a chrome-extension:// or isolated-app:// 
    document could previously construct a SharedWorker whose main-script URL 
    was cross-origin to the creator. This was because the same-origin check 
    in SharedWorkerServiceImpl::ConnectToWorker allowed cross-origin 
    requests if the scheme was allowlisted (and chrome-extension was 
    whitelisted in 
    ChromeContentBrowserClient::DoesSchemeAllowCrossOriginSharedWorker). 
     
    This CL adds a strict same-origin check for these schemes in 
    SharedWorkerServiceImpl::ConnectToWorker, gated by a new feature flag 
    `kEnforceSharedWorkerSameOriginCheck`. If a violation is detected, the 
    browser process terminates the renderer with a bad message 
    (`SWSI_CROSS_ORIGIN_SCRIPT_URL`). 
     
    This is a sibling fix to the DedicatedWorker hardening landed in commit 
    8bde565f45a8baf9b84c129905eb53c9abe108d2. 
     
    This CL also updates 
    `RegisterNonNetworkWorkerMainResourceURLLoaderFactories` to take 
    `RequestDestination` to strictly separate the behavior for 
    DedicatedWorker and SharedWorker when creating 
    `IsolatedWebAppURLLoaderFactory`. 
     
    Bug: 504073872 
    Change-Id: I852098d5ffc7b31d176de87dc76bc81dc429636f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7784632 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1620886}

```

---

Files:

- M `chrome/browser/chrome_content_browser_client.cc`
- M `chrome/browser/chrome_content_browser_client.h`
- M `content/browser/bad_message.h`
- M `content/browser/worker_host/dedicated_worker_host.cc`
- M `content/browser/worker_host/shared_worker_service_impl.cc`
- M `content/browser/worker_host/shared_worker_service_impl_unittest.cc`
- M `content/browser/worker_host/worker_script_fetcher.cc`
- M `content/browser/worker_host/worker_script_fetcher.h`
- M `content/public/browser/content_browser_client.cc`
- M `content/public/browser/content_browser_client.h`
- M `content/public/common/content_features.cc`
- M `content/public/common/content_features.h`
- M `extensions/shell/browser/shell_content_browser_client.cc`
- M `extensions/shell/browser/shell_content_browser_client.h`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [0e9234d7c0a1074df286f33eae9c1008a5d05a6e](https://chromiumdash.appspot.com/commit/0e9234d7c0a1074df286f33eae9c1008a5d05a6e)  

Date: Mon Apr 27 03:48:25 2026


---

### tr...@gmail.com (2026-05-14)

Hello , just to know why is it steel on unconfirmed states when it has been fixed ? Best regards

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. Web platform privilege escalation with bisect.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504073872)*
