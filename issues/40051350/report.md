# Security: Extension fingerprinting by detecting fetched resources

| Field | Value |
|-------|-------|
| **Issue ID** | [40051350](https://issues.chromium.org/issues/40051350) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>PerformanceAPIs>ResourceTiming, Platform>Extensions, Privacy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2020-01-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Browser extensions can fetch resources (i.e., style sheets, scripts, images, etc.) from the Internet. Attackers can use Resource Timing API to collect the list of fetched resources and enumerate installed extensions. Using the performance.getEntriesByType("resource") method, we can query the list of all resources requested. In this way, we can obtain the list of all resources requested by the content scripts of extensions installed in the user’s browser (resources requested by extensions’ background pages are not included).  

Content scripts are not accessible from the DOM and they cannot be detected directly. However, with the mentioned approach attackers can get enough information to detect them. By limiting Resource Timing API to Dom and filtering out extension’s resources this vulnerability will be fixed.

**REPRODUCTION CASE**  

For instance, the HTTP requests that are issued by the "source now" extension (UUID: dimnlaemmkbhojonandnnbogfifjnpno ) are:  

<https://b.alicdn.com/@sc/list-buyer/assets/source-now/entry/index.js>  

<https://b.alicdn.com/@sc/list-buyer/lib/js/jquery.js>  

We can detect whether this extension is installed or not with the following script:  

performance.getEntriesByName('<https://b.alicdn.com/@sc/list-buyer/lib/js/jquery.js').length==1>

**VERSION**  

Chrome Version: All versions  

Operating System: Mac OS, Windows, Linux

**CREDIT INFORMATION**  

Reporter credit: Soroush Karami ([sor.karami@gmail.com](mailto:sor.karami@gmail.com))

## Timeline

### so...@gmail.com (2020-01-25)

The example in the report is not a good one, since actually the extension adds the resources to the DOM and DOM fetches the URLs.

Following extension is better example, because the resource is fetched by content script:
https://chrome.google.com/webstore/detail/mega-oferta/clmonajkjkippgbeplpaednnilkjeogi
can be detected by:
performance.getEntriesByName('https://jcash.com.br/x1/2.xml').length==1


### es...@chromium.org (2020-01-27)

Adding some Resource Timing and extensions folks -- can you please take a look and see if you can repro this and confirm that it's a bug?

[Monorail components: Blink>PerformanceAPIs>ResourceTiming Platform>Extensions Privacy]

### es...@chromium.org (2020-01-27)

(also cc'ed aaj@ since ISTR that he was involved in the security review for Resource Timing, but please ignore if I'm misremembering)

### sh...@chromium.org (2020-01-28)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2020-02-14)

Yoav, have you had an opportunity to look at this?

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### yo...@chromium.org (2020-06-19)

Apologies, but I completely missed this initially :/

Seems reasonable to eliminate those fetches from Resource Timing. Since many extensions also modify the DOM, I'm not sure this will solve the fingerprinting problem, but it may make it harder.

### rd...@chromium.org (2020-06-19)

Interesting!  Thanks for the report.

cc karandeepb@ as well, since he's been doing a few things related to the content script / main world boundary.

While I could see this as being nice to have, I don't think it's a requirement or a security bug.  Any time an extension injects a script into a web page, that web page has the _potential_ to detect that script.  This is a fundamental limitation of running in the same process, and on the same content, as the page.  The boundary between content script and main world is more for convenience (preventing collisions) and a "minimum bar", rather than a security boundary (which is the same reason content scripts don't have access to heavily privileged APIs), or a guarantee against detection.

This seems like something we should still fix from a functional standpoint, and it's an exceptionally easy fingerprinting technique for extensions that are susceptible to it, so I'm quite supportive of changing the behavior.  But I wouldn't consider it a security bug.

### ka...@chromium.org (2020-06-19)

Hmm I wonder if this will be solved by a separate ResourceFetcher for each world, but it has its own problems (https://docs.google.com/document/d/1hPEdml8q6nYkeSHAIFp4Qp5jxEm_GiQd8bY9VuJxswE/edit?usp=sharing for details). +yhirano@ and +hiroshige@ as FYI.

Also, +morlovich@ who was working on extension fingerprinting.

I'd agree that this isn't a security bug. There are multiple ways to fingerprint extensions today.

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### yo...@chromium.org (2020-12-08)

Thinking about this more and given comments #8 and #9, I'm considering WONTFIXing this.
It doesn't seem trivial to keep track of which fetches were triggered by extensions (through fetch/XHR or by creating DOM elements), and the benefits of that seem dubious.

Any objections?

### ka...@chromium.org (2020-12-08)

> It doesn't seem trivial to keep track of which fetches were triggered by extensions (through fetch/XHR or by creating DOM elements), and the benefits of that seem dubious.

While it's not full-proof, we do something similar for CSP checks for fetches initiated in isolated worlds. See ResourceLoaderOptions::world_for_csp. We may be able to rely on that and exclude fetches initiated from isolated worlds from the performance API. Note that there are some non-extension clients for isolated worlds as well. Also, using this method, we still won't be able to exclude fetches which run in the main world as a side effect of an operation in the isolated world.

If the work here isn't that involved, it's probably still a reasonable change to make. That said, still a P3 given that any mitigations we implement won't be full-proof and there are other fingerprinting vectors available to sites (we are fixing some of the more prevalent ones like web accessible resources).

### yo...@chromium.org (2020-12-09)

OK, so keeping track of fetches from isolated worlds will enable us to avoid exposing e.g. fetch() calls triggered by extensions, but not e.g. <script> resources they added to the DOM?

### ka...@chromium.org (2020-12-14)

Even the request for the script resource added to the DOM when in the isolated world would be attributable to the isolated world and hence we would be able to avoid exposing that request. 
However the added script resource is run in the main world, so any resource requests it initiates would still be exposed. It all depends on the isolated world, main-world boundary which is not that intuitive. See https://docs.google.com/document/d/1b2ALoATe8kLocPmruUtX5ugc2tqPnY3ghtaNsh0KT14/edit?usp=sharing (googlers only).

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### yo...@chromium.org (2022-09-22)

I completely dropped this off my lists...
Re-reading past discussions, it seems like it's feasible to remove extension-based resource timing entries from the performance timeline. The main question: do we want to do that?

Is it a security/privacy issue if we don't do that? Does it significantly increase the fingerprintability risk of extensions beyond DOM injections and/or blocking of other requests? 

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### aa...@google.com (2022-09-29)

IMHO this is something that we want to do, and not removing these entries from the performance timeline results in a low-risk information leak. While there are other ways to detect extensions (checking for web-accessible resources or the presence of DOM modifications identifying an extension), I'm guessing that we'll want to crack down on them somehow as part of our efforts to reduce fingerprintability. 

As a specific concern, `performance.getEntriesByType("resource")` is not what we'd generally classify as an entropy-rich API that's susceptible to fingerprinting, but exposing extension-requested resources makes it provide a potentially highly granular signal useful for tracking. It would be nice if this went away and forced fingerprinters to enumerate resources / DOM modifications they're probing for, because this makes fingerprinting easier to detect.

### yo...@chromium.org (2022-09-29)

OK, thanks for clarifying!

So, what we probably want to do:
* In ResourceFetcher::PopulateAndAddResourceTimingEntry [1] we have the Resource, we can get its options(), and check if the CSP world is the main world, and if not, bail.
* We probably also want to clarify that in the spec.

Can we WPT extensions? Or would this have to rely on browser tests?

[1]

### hi...@chromium.org (2022-10-04)

[Empty comment from Monorail migration]

### yo...@chromium.org (2022-11-25)

haoliuk@ signed up to take a look. Thanks Hao! :)

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### ha...@chromium.org (2022-12-20)

It seems we can't test it in wpt as it launches content_shell. 
We need to have a browser test that installs an extension which fetch a resource 
and verifies that there's no corresponding resource timing entry. 

### ha...@chromium.org (2022-12-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d4807ebd5752d1811366d8f2822b5d20d4d91449

commit d4807ebd5752d1811366d8f2822b5d20d4d91449
Author: Hao Liu <haoliuk@chromium.org>
Date: Tue Jan 03 16:28:33 2023

Fix extension fingerprinting via resource timing entry

This CL is to prevent resource timing entry being emitted for resources
that are initiated in the Non main world.

Test cases are added for resources initiated from both the main world
and non main world.

Bug: 1045681
Change-Id: I309b54dae63f56e8d1d71e5c33507623b0c80389
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4116604
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Hao Liu <haoliuk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1088254}

[add] https://crrev.com/d4807ebd5752d1811366d8f2822b5d20d4d91449/chrome/test/data/extensions/resource_timing/test-page.html
[modify] https://crrev.com/d4807ebd5752d1811366d8f2822b5d20d4d91449/third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc
[modify] https://crrev.com/d4807ebd5752d1811366d8f2822b5d20d4d91449/chrome/test/BUILD.gn
[add] https://crrev.com/d4807ebd5752d1811366d8f2822b5d20d4d91449/chrome/test/data/extensions/resource_timing/fetch_resource/manifest.json
[add] https://crrev.com/d4807ebd5752d1811366d8f2822b5d20d4d91449/chrome/browser/performance_timeline_browsertest.cc
[add] https://crrev.com/d4807ebd5752d1811366d8f2822b5d20d4d91449/chrome/test/data/extensions/resource_timing/24.png
[add] https://crrev.com/d4807ebd5752d1811366d8f2822b5d20d4d91449/chrome/test/data/extensions/resource_timing/fetch_resource/content_script.js


### ha...@chromium.org (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-02)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1045681?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>PerformanceAPIs>ResourceTiming, Platform>Extensions, Privacy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051350)*
