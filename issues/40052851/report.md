# Security: XS-Leak with Resource Timing API and CSP Embedded Enforcement

| Field | Value |
|-------|-------|
| **Issue ID** | [40052851](https://issues.chromium.org/issues/40052851) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>PerformanceAPIs, Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@shift-js.info |
| **Assignee** | yo...@chromium.org |
| **Created** | 2020-07-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

When we get an error by `csp` attribute of `iframe` tags (i.e. CSP Embedded Enforcement), `name` property of `PerformanceResourceTiming` for the iframe turns into `data:,`.  

This may allow attackers to check whether a Cross-Origin response has a more restrictive CSP than one specified in `csp` attribute, or not.  

In other words, this behavior of CSPEE and Resource Timing API can be utilized as XS-Leak.

Notably, express, a famous server-side library of Node.js, returns `default-src: 'none'` header with its default error page. For instance, the following HTTP server written in Node.js returns `default-src: 'none'` with 404 when we access `/foobar`, while `/` returns 200 without any CSP header.

```
const express = require('express')  
const app = express()  
  
app.get('/', (req, res) => res.send('Hello World!'))  
app.listen(25252, () => { })  

```

This fact means that, in the case of express, attackers can know whether a cross-origin application by express returns a default error page or not. Here's the PoC:

```
<script>  
    window.onload = () => {  
        performance.getEntriesByType("resource").map((r, i) => {  
            if (r.name === "data:,") {  
                alert(`record ${i} tells us we got default error page!`);  
            } else {  
                alert(`record ${i} tells us we got a normal page!`);  
            }  
        })  
    }  
</script>  
<iframe id="a" src="http://localhost:25252/" csp="default-src 'none'"></iframe>  
<iframe id="b" src="http://localhost:25252/404" csp="default-src 'none'"></iframe>  

```

Considering a lot of web apps are using express still now, I believe this XS-Leak vector has an impact to some extent.

**VERSION**  

Chrome Version: Version 83.0.4103.61 (Official Build) (64-bit) + stable  

Operating System: Ubuntu 20.04

**REPRODUCTION CASE**

1. Download attached files (`poc.html` and `index.js`) into a same directory.
2. In the directory in which downloaded files are placed, run `npm install && node index.js`.
3. Open `poc.html`.

**CREDIT INFORMATION**  

Reporter credit: Takashi Yoneuchi (@y0n3uchy)

## Attachments

- [index.js](attachments/index.js) (text/plain, 139 B)
- [index.html](attachments/index.html) (text/plain, 508 B)

## Timeline

### me...@chromium.org (2020-07-17)

I beleive I was able to reproduce the intended behavior of the POC.
mkwest@ could you please take a look?

[Monorail components: Blink>SecurityFeature]

### [Deleted User] (2020-07-17)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2020-07-20)

It seems to me that error pages shouldn't show up in performance timing APIs. Yoav, is this intentional?

[Monorail components: -Blink>SecurityFeature Blink>PerformanceAPIs Blink>SecurityFeature>ContentSecurityPolicy]

### mk...@chromium.org (2020-07-20)

I suspect this might be happening because the navigation to the error page is performed by Blink, rather than blocking the navigation with an error interstitial in the browser, which antoniosartori@ is working through.

### np...@chromium.org (2020-07-20)

We do intentionally expose some error pages in Resource Timing. Perhaps what we need is further restricting what information is exposed in those cases?

### mk...@chromium.org (2020-07-20)

I'd prefer that we not explicitly distinguish between a cross-origin page that loaded successfully, and one that caused a violation of some sort (XFO, CSP, whatever). Listing the URL that the embedding page already knows is fine, pointing out that it was an error page seems less fine.

### np...@chromium.org (2020-07-20)

Right, and per the spec (https://w3c.github.io/resource-timing/#sec-performanceresourcetiming), for name: "This attribute MUST return the resolved URL of the requested resource. This attribute MUST NOT change even if the fetch redirected to a different URL." so I think this means the name should not be set to 'data:,'. Somehow the original requested URL is being lost.

### yo...@chromium.org (2020-07-28)

It seems to me like the correct behavior we want here is:
* iframe URLs are reported using regular Performance Entries - Otherwise, that would also enable to distinguish between an error page and a non-error page
* Those URLs should not change if the iframe loading was terminated by CSP's embedded enforcement

Does that match y'all's understanding?

### np...@chromium.org (2020-07-28)

That makes sense to me. BTW I closed https://crbug.com/chromium/1105834 recently as it was fixed in 84, so perhaps double check that this is still an issue.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### yo...@chromium.org (2020-12-07)

I'm able to reproduce the issue to some extent (I see that cross-origin blocked entries are not reported at all, rather than reported as 'data:', but the effect is the same).

### yo...@chromium.org (2020-12-08)

https://chromium-review.googlesource.com/c/chromium/src/+/2567925 also solves this issue. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eb493883a20b1e05a759c3006ee35a93d10ffa72

commit eb493883a20b1e05a759c3006ee35a93d10ffa72
Author: Yoav Weiss <yoavweiss@chromium.org>
Date: Tue Dec 08 12:40:16 2020

[resource-timing] ResourceTimingInfo for failed navigations

Failed navigations currently don't get a ResourceTiming entry.
This CL changes that by properly reporting them.

Bug: 1131929, 1105875
Change-Id: I0808f35e1b0d596c2bafa7630ed873c947254c5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567925
Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#834675}

[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/public/web/web_security_policy.h
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/content/renderer/render_thread_impl.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/core/exported/web_security_policy.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/platform/weborigin/scheme_registry.h
[add] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit.html
[add] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/web_tests/external/wpt/resource-timing/resources/csp-default-none.html.headers
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/core/frame/remote_frame_owner.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/platform/weborigin/scheme_registry.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/public/web/web_navigation_params.h
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/core/loader/document_loader.h
[add] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/web_tests/external/wpt/resource-timing/resources/csp-default-none.html


### yo...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations, the VRP panel has decided to award $1000 for this bug.

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-03-16)

This issue was migrated from crbug.com/chromium/1105875?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>PerformanceAPIs, Blink>SecurityFeature>ContentSecurityPolicy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052851)*
