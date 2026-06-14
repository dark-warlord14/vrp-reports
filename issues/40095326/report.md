# Site Isolation: Multiple restriction bypasses in register​Protocol​Handler

| Field | Value |
|-------|-------|
| **Issue ID** | [40095326](https://issues.chromium.org/issues/40095326) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML>CustomHandlers, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2019-06-07 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

register​Protocol​Handler has 2 restrictions.

1. Protocol should be one of permitted schemes (<https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler#Permitted_schemes>)
2. URL parameter should be same-origin as caller

This 2 checks are mostly checked in renderer process, thus attacker with ability to compromise renderer can register protocol handler with almost arbitrary url.

List of blacklisted scheme in the browser process are:  

["file","devtools","chrome","about","data","blob","javascript","view-source","externalfile","chrome-distiller","ftp","chrome-extension","content","filesystem","http","https","ws","wss","chrome-search"]  

Those schemes are check in following places:  

<https://cs.chromium.org/chromium/src/chrome/browser/profiles/profile_io_data.cc?q=ProfileIOData::IsHandledProtocol&l=467>  

<https://cs.chromium.org/chromium/src/content/browser/web_contents/web_contents_impl.cc?l=4818&q=IsPseudoScheme>

This means "chrome-error", "chrome-guest", and any other schemes can be registered. And resulting navigation url to those protocols can be anything. Note that user still has to approve the permission prompt for this to succeed.

Now, a website can invoke register​Protocol​Handler from an iframe. And destination URL can be a Data URL. When Data URL is set as a destination URL, permission prompt will display "wants to open \* links" where \* will be protocol name or related word (e.g. "email" for mailto:). This loses a lot of information like requesting origin and destination URL. Therefore I don't feel enough protection is there in permission prompt.

When Data URL is registered as a destination of mailto: (for example), mailto: links in any website will now result in navigation to Data URL. When this happens inside an iframe, Data URL will continue to use existing process, effectively bypassing Site Isolation.

**VERSION**  

Chrome Version: 75 stable  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Go to <https://shhnjk.azurewebsites.net/pageWithAds.html>
2. Attach WinDbg to Subframe process (i.e. shhnjk.com's process)
3. Load attached protocol.js in WinDbg (i.e. .scriptrun C:\windbg\protocol.js)
4. Click on Go button inside iframe
5. Observe that no origin information being displayed in the prompt
6. Click allow, and click on the next step link inside iframe
7. Click on the mailto link inside iframe
8. Observe that Data URL's script is being executed in shhnjk.azurewebsites.net's process

## Attachments

- [mailto.PNG](attachments/mailto.PNG) (image/png, 5.7 KB)
- [protocol.js](attachments/protocol.js) (text/plain, 1.3 KB)

## Timeline

### Ju...@microsoft.com (2019-06-07)

Of course, this bug has security implications other than Site Isolation. For example, native applications often have their own protocol handlers (e.g. skype, word, line, etc). Those protocol handlers might try to receive secret information, which could be leaked by this bug, because URL parameters includes `%s` which will be replaced with argument of the protocol handler (see: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler#Parameters).

### cr...@chromium.org (2019-06-07)

Thanks for the report!  While looking for owners, it actually looks like dcheng@ recently spotted part of this as well in https://crbug.com/chromium/952974 in April.  raymes@, can you take a look at this expanded version of the report and how it can be exploited?  Adding CustomHandlers component as well.

It sounds like we may want a few fixes, perhaps to WebContentsImpl::OnRegisterProtocolHandler:
1) Limiting |protocol| to the allowlist from https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler#Permitted_schemes.
2) Ensuring |url| is same origin with source->GetLastCommittedOrigin(), or something similar.  (CanAccessDataForOrigin may also be useful, but I don't think it would complain if |url| were a data: URL and |source| were on a web page.)
3) Fixing the permission prompt to show the URL if the origin is opaque (?).

Are there any valid cases for |url| to be a data: URL, by the way?  I'm not sure if a data: URL can be considered same origin even with itself, or if registerProtocolHandler should ever be allowed on a data: URL.  Maybe we can prevent that as well.

I imagine this affects all versions.  In terms of severity, we definitely want to fix it, but there's some mitigating factors from requiring users to click "Allow" to a vague permission request.  I think that might move it from Medium to Low, which is also how https://crbug.com/chromium/952974 was rated.

[Monorail components: Blink>HTML>CustomHandlers UI>Security>UrlFormatting]

### Ju...@microsoft.com (2019-06-07)

More fix proposals:
4) Only allow register​Protocol​Handler from secure context
5) Only allow register​Protocol​Handler from top-level browsing context 

### sh...@chromium.org (2019-06-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### Ju...@microsoft.com (2019-06-10)

I disagree with the severity assessment :)
As far as I tested, there are many bugs in register​Protocol​Handler API.

1. Destination URL can be arbitrary
With only this bug,Site Isolation can be bypassed. Because URL can be Data URL. And exploiting this bug doesn’t require a scheme restriction bypass.

2. Scheme restriction can be bypassed
This one is not a Site Isolation bypass, as attacker would want to use attacker’s origin to exfiltrate parameters (or arguments) passed with specific scheme.

3. Permission prompt uses URL parameter's origin
This is why permission prompt shows no origin information when URL parameter is a Data URL. This also bypasses Permission Delegation (https://www.chromestatus.com/feature/5670617353289728), which is to make sure prompt origin will always be a top-level browsing context's origin

Additionally, allowing register​Protocol​Handler in non-secure-context and from iframe without feature policy seems like a bad design (and probably a bug).

And I don’t think vague prompt is a mitigation. Yes,it will decrease the probability of successful exploit, but that’s because of a requirement to click Allow. User really has no clue who’s requesting, and I don’t think something like this should be considered as a mitigation.

With all above information, I think this warrants Medium severity.

### ra...@chromium.org (2019-06-14)

FYI I have a fix up at https://chromium-review.googlesource.com/c/chromium/src/+/1652756.

It does not currently address Secure Origin or Main Frame restrictions which we may want but that would require Web Platform approval.

### ra...@chromium.org (2019-06-14)

[Empty comment from Monorail migration]

### Ju...@microsoft.com (2019-06-20)

sources:
 
https://shhnjk.azurewebsites.net/pageWithAds.html
------------------------------------
This page has some ads.<br>
<iframe src="https://test.shhnjk.com/regproto.html"></iframe>
------------------------------------

https://test.shhnjk.com/regproto.html
------------------------------------
<div></div><br>
<script>
    function go(){
        try{
        navigator.registerProtocolHandler("mailto", "data:text/html,//www.google.com/?<script>alert(1)<\/script>&leak=%s", "test");
        }catch(e){};
        document.querySelector("div").innerHTML = "Click allow and Go to <a href='/next_step.html' target='_top'>next step</a>";
    }
</script>
<button onclick="go()">Go</button>
------------------------------------

https://test.shhnjk.com/next_step.html
------------------------------------
Click below!<br>
<iframe src="https://shhnjk.azurewebsites.net/mailto.html"></iframe>
------------------------------------

https://shhnjk.azurewebsites.net/mailto.html
------------------------------------
<a href="mailto:secure@microsoft.com">mailto:secure@microsoft.com</a>
------------------------------------

### mm...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/181fa02d2006c3d0f82c54fe118f25a959829466

commit 181fa02d2006c3d0f82c54fe118f25a959829466
Author: Raymes Khoury <raymes@chromium.org>
Date: Tue Jul 09 02:45:24 2019

Add renderer-side checks for http/https URLs for registerProtocolHandler

Currently we allow any URLs to be handlers for calls to
registerProtocolHandler as long as they are same origin accessible.
However:
1) This has led to bugs (see below)
2) It doesn't make much sense for handlers to be data:, blob: URLs etc
3) The spec gives freedom to implementers to add additional checks like
this https://html.spec.whatwg.org/multipage/system-state.html#custom-handlers
4) The guidance on https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler
states that "The handler's URL must use one of "http" or "https" as its
scheme." (even though this isn't mandated in the spec)
5) Firefox restricts handlers to https.

This CL requires http/https URL handlers.

Chrome status entry: https://chromestatus.com/feature/5066079862784000

Bug: 971917,952974
Change-Id: Id76bf6f7ac28f18c4158893f47806c9ef6aea9c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1683577
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Gyuyoung Kim <gyuyoung@igalia.com>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Raymes Khoury <raymes@chromium.org>
Cr-Commit-Position: refs/heads/master@{#675498}

[modify] https://crrev.com/181fa02d2006c3d0f82c54fe118f25a959829466/third_party/blink/renderer/modules/navigatorcontentutils/navigator_content_utils.cc
[add] https://crrev.com/181fa02d2006c3d0f82c54fe118f25a959829466/third_party/blink/web_tests/register-protocol-handler/blob-urls.html
[add] https://crrev.com/181fa02d2006c3d0f82c54fe118f25a959829466/third_party/blink/web_tests/register-protocol-handler/data-urls.html


### ra...@chromium.org (2019-07-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971

commit 5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971
Author: Raymes Khoury <raymes@chromium.org>
Date: Wed Jul 10 02:09:23 2019

Add browser-side checks for registerProtocolHandler

This adds browser-side checks for the registerProtocolHandler API. In
particular:
1) Checks that the origin of the URL handler matches the origin of the RFH
where the call originates.
2) Checks that the protocol being handled is one of the safelisted
schemes.
3) Checks that the scheme of the URL handler is either http or https.

Check (1) is implemented in the content/ layer so that non-Chrome
embedders can benefit from this check.

Checks (2) and (3) are implemented further down in Chrome because we
need to ensure that if existing handlers are registered that we don't
load them from prefs.

Tests are added.

We may want to consider restricting this API to secure contexts in a
follow-up but this will need to be vetted by blink-dev@.

Bug: 971917,952974
Change-Id: I08b1c46b8e8493679adf7f252d09a224d67e64e7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1652756
Commit-Queue: Raymes Khoury <raymes@chromium.org>
Reviewed-by: Christian Dullweber <dullweber@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Trent Apted <tapted@chromium.org>
Reviewed-by: Ben Wells <benwells@chromium.org>
Cr-Commit-Position: refs/heads/master@{#675929}

[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/browser/browsing_data/chrome_browsing_data_remover_delegate_unittest.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/browser/browsing_data/counters/site_settings_counter_unittest.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/browser/chrome_content_browser_client_browsertest.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/browser/custom_handlers/protocol_handler_registry.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/browser/custom_handlers/protocol_handler_registry.h
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/browser/custom_handlers/protocol_handler_registry_browsertest.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/browser/custom_handlers/protocol_handler_registry_unittest.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/browser/ui/browser.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/common/custom_handlers/protocol_handler.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/common/custom_handlers/protocol_handler.h
[rename] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/chrome/test/data/custom_handler.html
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/content/browser/bad_message.h
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/content/browser/web_contents/web_contents_impl_unittest.cc
[modify] https://crrev.com/5ee1de5da38b1f1cf5ed6defec5c578b9cb4c971/tools/metrics/histograms/enums.xml


### sh...@chromium.org (2019-07-10)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-07-13)

this broke the Secure Shell app.  it explicit registers as a handler for ssh:// and i see no reason why that should be disallowed.  it handles ssh:// URIs perfectly fine.

### va...@chromium.org (2019-07-13)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-07-17)

Fixit is over, cleaning up the label.

### yi...@google.com (2019-07-30)

Add dchan & dougman to look into the potential test coverage for this.

### Ju...@microsoft.com (2019-09-06)

Blocking bug is fixed. Marking this bug as fixed too.

### na...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-30)

Congrats! The Panel decided to reward $1,000 for this report :) 

### na...@google.com (2019-10-04)

The Panel reassessed your report and is going to reward you a total of $3,000! 

### al...@qt.io (2019-10-17)

With both patches reverted, is this bug really fixed?

### lu...@chromium.org (2019-10-17)

Hmmm... indeed - the two fixes have been reverted in:
- https://chromium-review.googlesource.com/c/chromium/src/+/1699705
- https://chromium-review.googlesource.com/c/chromium/src/+/1701466

Not sure why these were not posted to this bug by bugdroid... :-(

### ra...@chromium.org (2019-10-17)

The changes were relanded:
https://chromium-review.googlesource.com/c/chromium/src/+/1730689
https://chromium-review.googlesource.com/c/chromium/src/+/1728369

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f14acf3c2de32cb4ed194920213d2d2b2d1076c4

commit f14acf3c2de32cb4ed194920213d2d2b2d1076c4
Author: Frédéric Wang <fwang@igalia.com>
Date: Thu Jul 16 09:07:41 2020

Fix test for RegisterProtocolHandlerDifferentOrigin

The test verifies that when registering a protocol handler with same
or different origin, RegisterProtocolHandler is called only once on
the delegate. However, the callback would be executed with two
different URLs, so we really need to check that the callback is
called once for same-origin URL and never for different origin URL.

Bug: 971917, 952974
Change-Id: Iabb9d33a38975efee3a178b6dad067a8a9cad642
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2299229
Reviewed-by: Raymes Khoury <raymes@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Frédéric Wang <fwang@igalia.com>
Cr-Commit-Position: refs/heads/master@{#788975}

[modify] https://crrev.com/f14acf3c2de32cb4ed194920213d2d2b2d1076c4/content/browser/web_contents/web_contents_impl_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dde6d04f8e4887cf11280cc035aa1a2842fae715

commit dde6d04f8e4887cf11280cc035aa1a2842fae715
Author: Frédéric Wang <fwang@igalia.com>
Date: Mon Aug 24 10:27:03 2020

Introduce common browser/web API for validation of custom handlers

Logic to validate custom handlers is required on both the web and
browser processes. This CL introduces a new API in
third_party/blink/public/common in order to reduce duplication. As a
starting point, a new helper function allows to verify whether the
following condition is satisfied [1]:

> If scheme is neither a safelisted scheme nor a string starting with
> "web+" followed by one or more ASCII lower alphas'

In order to keep this CL small, more advanced aspects like same-origin
condition (currently performed in WebContentsImpl), validation of the
schemes of the registered URLs [2] [3] or other tests that are currently
only performed on the web process are not considered. This can be refine
later if needed.

This CL makes the check on the browser process slighty stronger.
Previously the only requirement for URLs starting with "web+" was to be
sure they are not just equal to "web+".

This CL might also make verification on the web process slightly less
efficient, if the conversion from WTF::String to base::StringPiece
requires a buffer allocation. However, it seems unlikely to be a
performance bottleneck for the current use cases.

[1] https://html.spec.whatwg.org/multipage/system-state.html#normalize-protocol-handler-parameters
[2] https://crbug.com/1112268
[3] https://crbug.com/64100

Bug: 971917, 952974
Change-Id: Iaada22200d7b7d834ad878bbc51cc40ea67d6332
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2362802
Commit-Queue: Frédéric Wang <fwang@igalia.com>
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Cr-Commit-Position: refs/heads/master@{#800948}

[modify] https://crrev.com/dde6d04f8e4887cf11280cc035aa1a2842fae715/chrome/browser/custom_handlers/protocol_handler_registry_unittest.cc
[modify] https://crrev.com/dde6d04f8e4887cf11280cc035aa1a2842fae715/chrome/common/custom_handlers/protocol_handler.cc
[modify] https://crrev.com/dde6d04f8e4887cf11280cc035aa1a2842fae715/third_party/blink/common/BUILD.gn
[add] https://crrev.com/dde6d04f8e4887cf11280cc035aa1a2842fae715/third_party/blink/common/custom_handlers/protocol_handler_utils.cc
[modify] https://crrev.com/dde6d04f8e4887cf11280cc035aa1a2842fae715/third_party/blink/public/common/BUILD.gn
[add] https://crrev.com/dde6d04f8e4887cf11280cc035aa1a2842fae715/third_party/blink/public/common/custom_handlers/protocol_handler_utils.h
[modify] https://crrev.com/dde6d04f8e4887cf11280cc035aa1a2842fae715/third_party/blink/renderer/modules/navigatorcontentutils/navigator_content_utils.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fd80e3d0848986fc99f0e7f2ee78585b02a2d27e

commit fd80e3d0848986fc99f0e7f2ee78585b02a2d27e
Author: Frédéric Wang <fwang@igalia.com>
Date: Mon Aug 24 15:44:30 2020

Add WPT tests for registerProtocolHandler and 'web+' schemes

This is a follow-up of [1] where the validation on the web and browser
processes have been unified. Tests for 'web+' have been added to
ProtocolHandlerRegistryTest (browser process). This CL adds similar and
more complete checks to the existing WPT test (web process).

The relevant section from the specification says [2]:

* Set scheme to scheme, converted to ASCII lowercase.
* If scheme is neither a safelisted scheme nor a string starting with
  "web+" followed by one or more ASCII lower alphas, then throw a
  "SecurityError" DOMException.

Bug: 971917, 952974, 627682

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2362802
[2] https://html.spec.whatwg.org/multipage/system-state.html#normalize-protocol-handler-parameters

Change-Id: I769048bd4db6883a75d4237f20f23aa61452d732
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2371632
Reviewed-by: Gyuyoung Kim <gyuyoung@igalia.com>
Commit-Queue: Frédéric Wang <fwang@igalia.com>
Cr-Commit-Position: refs/heads/master@{#801004}

[modify] https://crrev.com/fd80e3d0848986fc99f0e7f2ee78585b02a2d27e/third_party/blink/web_tests/external/wpt/html/webappapis/system-state-and-capabilities/the-navigator-object/protocol.https.html


### gi...@appspot.gserviceaccount.com (2021-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/083e63afeeed586b570beb61ed8f7ea5c340adb1

commit 083e63afeeed586b570beb61ed8f7ea5c340adb1
Author: Frédéric Wang <fwang@igalia.com>
Date: Thu May 13 16:20:50 2021

Document protocol_handler_utils.h' IsValidCustomHandlerScheme

Follow-up of https://chromium-review.googlesource.com/c/chromium/src/+/2362802

Bug: 971917, 952974
Change-Id: Ifc666ef23737201f1f29dda3da5cec1f116235c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2894264
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Frédéric Wang <fwang@igalia.com>
Cr-Commit-Position: refs/heads/master@{#882546}

[modify] https://crrev.com/083e63afeeed586b570beb61ed8f7ea5c340adb1/third_party/blink/public/common/custom_handlers/protocol_handler_utils.h


### is...@google.com (2021-05-13)

This issue was migrated from crbug.com/chromium/971917?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>CustomHandlers, Internals>Sandbox>SiteIsolation, UI>Security>UrlFormatting]
[Monorail blocking: crbug.com/chromium/983843]
[Monorail mergedwith: crbug.com/chromium/952974]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095326)*
