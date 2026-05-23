# DevTools Sources panel with Service Worker causes POST to be resent bypassing SameSite=Strict

| Field | Value |
|-------|-------|
| **Issue ID** | [470574526](https://issues.chromium.org/issues/470574526) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>Cookies, Platform>DevTools>Sources |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 143.0.0.0 |
| **Reporter** | j....@gmail.com |
| **Assignee** | al...@google.com |
| **Created** | 2025-12-21 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Visit https:// jtw.sh/ samesite-post-bypass-ce7139c3/target-sw.php so that cookies are set and a service worker is registered on the target website (`jtw.sh`)
2. Visit the attacker's site: https:// vps.jorianwoltjer.com/ samesite-post-bypass-ce7139c3/csrf-sw.html
3. Right click and choose *Inspect* to open the DevTools, or press `Ctrl+Shift+I` or `F12` on the keyboard
4. In the background, a malicious POST request with all cookies has now been sent to the target. See it in the *Sources* tab viewing the `target-sw.php` file (see recording samesite-post-bypass-sw.mp4)

Source code for reproducing this locally is also provided in the attached samesite-post-bypass-sw.zip. Run with `php -S 0.0.0.0:8000`

# Problem Description

In DevTools, the *Sources* panel shows source code of the current page and its associated files. It gets these resources from the cache, or re-fetches them if needed. This new request is initiated from the current site, which is a contradiction if the original navigation came from cross-site. It means that the request for the Sources tab will contain SameSite=Strict cookies even for POST requests.

Weirdly, this re-fetching process seems to only happen if there is a Service Worker registered for the target. Otherwise the error "Content unavailable. Resource was not cached" is shown in place of the content. The service worker doesn't have to do anything, it just needs to be registered on the target. So any site that uses a service worker and relies on SameSite for Cross-Site Request Forgery (CSRF) protection is vulnerable.

From the attacker a simple top-level form submission is enough. While it shouldn't work initially, after the DevTools are opened on the resulting page, the request is resent and SameSite=Strict cookies are now sent with the body payload from the attacker.

```
<form action="..." method="post">
  <input type="text" name="name" value="value">
</form>
<script>
  document.forms[0].submit();
</script>

```

This requires some unusual user interaction (`F12`), but to me still felt unexpected. It should not be possible for an attacker to prepare a request so that it contains their malicious POST body with the user's SameSite=Strict cookies without it being clearly visible.  

The request that the DevTools sources tab sends should inherit the SameSite-ness (initiator?) of the original request so that it is as identical as possible, and doesn't increase the risk of CSRF.

# Summary

DevTools Sources panel with Service Worker causes POST to be resent bypassing SameSite=Strict

# Custom Questions

#### Reporter credit:

Jorian Woltjer, Mian, bug\_blitzer

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: No \

## Attachments

- [samesite-post-bypass-sw.mp4](attachments/samesite-post-bypass-sw.mp4) (video/mp4, 2.3 MB)
- [samesite-post-bypass-sw.zip](attachments/samesite-post-bypass-sw.zip) (application/zip, 875 B)
- [csrf.html](attachments/csrf.html) (text/html, 208 B)
- [target.php](attachments/target.php) (application/x-httpd-php, 430 B)
- [sw.js](attachments/sw.js) (text/javascript, 0 B)
- [Tue Dec 23 2025 13:27:23 GMT-0800 (Pacific Standard Time).png](attachments/Tue Dec 23 2025 13_27_23 GMT-0800 (Pacific Standard Time).png) (image/png, 94.7 KB)

## Timeline

### aj...@google.com (2025-12-23)

Hello - please upload the sources as individual files, this makes it faster for us to triage the issue. Thanks!

### j....@gmail.com (2025-12-23)

Hi, of course, here are the files inside the ZIP. They should all be placed inside the same folder.

### aj...@google.com (2025-12-23)

I've tried to repro this but I see the following.

Could you outline the steps I need to take using the local repro on 127.0.0.1:8000 and 8001 (rather than the example sites above)?

### j....@gmail.com (2025-12-24)

Here are the steps to reproduce it locally:
1. Host victim & attacker site with `php -S 0.0.0.0:8000`. Now 127.0.0.1:8000 is the attacker's site, and localhost:8000 is the victim
2. Visit http://localhost:8000/target.php to get all cookies set and a service worker installed
3. Visit http://127.0.0.1:8000/csrf.html
4. When it has auto-submitted, press F12, go to the Sources tab and view `target.php`

In there you should see the response to the request with SameSite=Strict cookies and the attacker's POST data

### pe...@google.com (2025-12-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### es...@chromium.org (2026-01-02)

I was able to reproduce with the instructions in #5.

I'll assign this Low severity because of the user interaction to open DevTools (in contrast to <https://issues.chromium.org/issues/470629629> which requires two unusual user interactions).

Thanks for the report!

### ch...@google.com (2026-01-03)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@chromium.org (2026-01-05)

Looks like the initiator origin used [here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/protocol/devtools_network_resource_loader.cc;l=52;drc=fc7ddc185b7f027dd7f4981ba8b2334c69a2e79c) is "the last committed origin of a RenderFrameHost identified by a DevTools frame token". For the purpose of SameSite=Strict cookies, the "right" initiator origin to use is probably the initiator origin from the request that loaded the main frame.

### al...@google.com (2026-01-07)

I think this does not go via the code path linked in c#9. Instead, I think Page.getResourceContent is used resulting in a fetch happening here <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_resource_content_loader.cc;l=117;drc=64b417264ff2f93e61931ef67b439687923c44df>. I think this also explains why it only happens if there is a service worker.

```
[251731:1:0107/113220.731538:ERROR:third_party/blink/renderer/core/inspector/inspector_resource_content_loader.cc:125] XXX fetching url: "http://localhost:8000/target.php"
[251731:1:0107/113220.732163:ERROR:third_party/blink/renderer/core/inspector/inspector_resource_content_loader.cc:126] XXX document url: "http://localhost:8000/target.php"
[251731:1:0107/113220.732418:ERROR:third_party/blink/renderer/core/inspector/inspector_resource_content_loader.cc:127] XXX cache mode: kDefault

```

### al...@google.com (2026-01-07)

Verified that reverting <https://chromium-review.googlesource.com/c/chromium/src/+/2910485> fixes the issue. Given that @ja...@google.com could you please take a look? Do you know if checking ControllerServiceWorkerID is necessary? I also wonder if using the default cache mode should event be possible in the inspector\_resource\_content\_loader (cc @ds...@google.com for thoughts).

### ja...@chromium.org (2026-01-07)

> Weirdly, this re-fetching process seems to only happen if there is a Service Worker registered for the target

So the sources panel never actually sends a network request over the wire except in the case that my fix hits? If that's true, then yeah we should probably revert my change and find another way to fix the console errors that my patch fixed.

### ja...@chromium.org (2026-01-07)

> I also wonder if using the default cache mode should event be possible in the inspector\_resource\_content\_loader

Yeah, maybe you could make this vulnerability still happen after reverting my patch since it still used to have a default cache mode.

It would be nicer if we could just store all responses in the devtools frontend while recording network requests, and in the case where the user opens devtools after the page has loaded, just have an error message there saying to reload the page with devtools enabled from the start. That would probably also be a good way to solve <https://issues.chromium.org/issues/40254754>

In the meantime, I'm still supportive of reverting my fix if you want.

### al...@google.com (2026-01-08)

Thanks for checking! Indeed, I think <https://issues.chromium.org/issues/40254754> already has a solution but this code path in getResourceContent only looks into the HTTP cache. cc @al...@google.com

### al...@google.com (2026-01-08)

So here is a proposed solution (<https://chromium-review.googlesource.com/c/chromium/src/+/7409996>): set the request mode to kSameOrigin and the cache mode to kOnlyIfCached for all document requests in InspectorResourceContentLoader.

1. kOnlyIfCached is only expected to work with kSameOrigin. If the request ends up in the service worker, it should retrieve the cached response if any without sending any requests.
2. this satisfies the DevTools requirements for populating the data from cache: makes the behavior consistent with and without service workers present. In small number of instances, the data would not be populated because an actual network request would no longer be sent but it sounds acceptable since the code path only affected sites with a service worker with not cached responses.

WDYT? Would it have any negative security consequences? @ds...@google.com @aj...@google.com @ch...@chromium.org

### da...@google.com (2026-01-12)

SGTM

### dx...@google.com (2026-01-13)

Project: chromium/src  

Branch:  main  

Author:  Alex Rudenko [alexrudenko@chromium.org](mailto:alexrudenko@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7409996>

Set resource request mode to kSameOrigin and only use the kOnlyIfCached mode

---


Expand for full commit details
```
     
    kOnlyIfCached only works if kSameOrigin is set [1]. The default request 
    mode is kNoCors[2]. While kNoCors + kOnlyIfCached seems to work for 
    getting cached resources, this combination does not work when getting 
    cached requests from the service worker. This CL changes the mode to 
    kSameOrigin which should allow the request to hit the service worker 
    cache. 
     
    The intention of this part of the resource content loader seems to be to 
    avoid hitting the network so the combination of kOnlyIfCached + 
    kSameOrigin would achieve that. 
     
    [1]: 
    [2]: 
     
    https: //source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/request.cc;l=649;drc=f3534bf8a057a7dcb2f239e855fc71b2faf6dddf 
    https: //source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/fetch_request_data.h;l=240;drc=4641a043d7914ce31515751c357158d46f4c937a 
    Fixed: 470574526 
    Change-Id: Ib92a9df516ee94a8bfbea57f5da17b5e21f9261a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7409996 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Auto-Submit: Alex Rudenko <alexrudenko@chromium.org> 
    Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1568281}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/inspector_resource_content_loader.cc`

---

Hash: [a6d7acc60f1c45f3fd24671a5283a1b4cb585948](https://chromiumdash.appspot.com/commit/a6d7acc60f1c45f3fd24671a5283a1b4cb585948)  

Date: Tue Jan 13 08:39:51 2026


---

### sp...@google.com (2026-01-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Web Exploitation mitigation bypass mitigated by devtools requirement


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Web Exploitation mitigation bypass mitigated by devtools requirement

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/470574526)*
