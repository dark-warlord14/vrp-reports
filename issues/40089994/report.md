# Security: XSS in "Site blocked" (supervised user) interstitial and chrome://interstitials/supervised_user

| Field | Value |
|-------|-------|
| **Issue ID** | [40089994](https://issues.chromium.org/issues/40089994) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | UI>Browser>WebUI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2017-12-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The "Site blocked" interstitial for supervised users has multiple XSS vulnerabilities at [1].  

The generated HTML is used in two places, and can be used as follows:

- Modify the custodian name and/or e-mail to contain a XSS payload. When the user triggers the supervised user interstitial, XSS will occur.
- Open the chrome://interstitials/supervised\_user debug page with additional query string parameters. This can be done manually or with a Chrome extension.

The Content-Security-Policy of interstitial pages is as follows [2]:  

script-src chrome://resources 'self' 'unsafe-eval' 'unsafe-inline';  

... and because of this very liberal policy, it does not offer protection against XSS (notably 'unsafe-inline' is allowed).

The impact of this vulnerability is access to any privileged webui API that is exposed to the page, as well as the ability to navigate to any other restricted URL ( such as chrome://quit ).

**VERSION**  

Chrome Version: 63.0.3239.108 (stable), 65.0.3303.0 (canary)

**REPRODUCTION CASE**  

Open the following URL and observe a navigation to chrome://quit:  

chrome://interstitials/supervised\_user?custodian=<img+src+onerror=location='chrome://quit'>

Or achieve the same effect by loading the attached Chrome extension via "Load unpacked extension" at chrome://extensions (extensions are normally not allowed to navigate to chrome://quit ).

The most realistic scenario to abuse this is through an extension: either by a malicious extension that directly calls chrome.tabs.create with the given URL (as in the attached example), or by an extension that blindly passes external URLs to a chrome.tabs.create/update function (which is not uncommon, sadly).

[1] <https://chromium.googlesource.com/chromium/src/+/74bfeb17d29b550a8332934cf36775ae4a902165/components/supervised_user_error_page/resources/supervised_user_block_interstitial.js#69>  

[2] <https://chromium.googlesource.com/chromium/src/+/74bfeb17d29b550a8332934cf36775ae4a902165/chrome/browser/ui/webui/interstitials/interstitial_ui.cc#420>

## Attachments

- [interstitial-supervised-xss.zip](attachments/interstitial-supervised-xss.zip) (application/octet-stream, 563 B)

## Timeline

### ro...@robwu.nl (2017-12-24)

Patch: https://chromium-review.googlesource.com/c/chromium/src/+/844075

+cc bauerb for review.

### el...@chromium.org (2017-12-24)

Nice find, thanks! 

Is there any reason why the CSP cannot be tightened for all interstitials?

### bu...@chromium.org (2017-12-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a296eff269063ef8daa7cdacf4483d3993214a1b

commit a296eff269063ef8daa7cdacf4483d3993214a1b
Author: Rob Wu <rob@robwu.nl>
Date: Sun Dec 24 15:37:52 2017

Fix XSS in supervised user interstitial

BUG=797525

Change-Id: Ib5cfa732b0f4de8645031c0166e4d67633a65c93
Reviewed-on: https://chromium-review.googlesource.com/844075
Reviewed-by: Bernhard Bauer <bauerb@chromium.org>
Commit-Queue: Rob Wu <rob@robwu.nl>
Cr-Commit-Position: refs/heads/master@{#526158}
[modify] https://crrev.com/a296eff269063ef8daa7cdacf4483d3993214a1b/components/supervised_user_error_page/resources/supervised_user_block_interstitial.js


### rs...@chromium.org (2017-12-28)

Labeling as medium-severity because this would require the user to install an extension to exploit.

### ro...@robwu.nl (2018-01-14)

Verified fixed in 65.0.3322.0 using the STR from the report.

Requesting merge of a296eff269063ef8daa7cdacf4483d3993214a1b to M-64.

### sh...@chromium.org (2018-01-14)

This bug requires manual review: We are only 8 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-14)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### cm...@google.com (2018-01-16)

awhalley@ I don't think we have to take this into M64 at this point but letting you make that call :)

### cm...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### cm...@chromium.org (2018-01-17)

awhalley@ also agrees that we can wait to ship this fix in M65. 

### me...@chromium.org (2018-01-17)

> The impact of this vulnerability is access to any privileged webui API that is exposed to the page, as well as the ability to navigate to any other restricted URL ( such as chrome://quit ).

As far as I can tell chrome://interstitials pages don't have access to privileged APIs. Can you please give an example?

### ro...@robwu.nl (2018-01-17)

> The impact of this vulnerability is access to any privileged webui API that is exposed to the page,
> as well as the ability to navigate to any other restricted URL ( such as chrome://quit ).

As far as I can tell chrome://interstitials pages don't have access to privileged APIs. Can you please give an example?

This XSS impacts two pages, chrome://interstitials (easy to exploit, see PoC) and the actual supervised user error interstitial (I haven't checked the list of available APIs here because the demonstrated issue in chrome://interstitials itself seems enough).
All WebUI pages (including chrome://intersititals) have access to the default webUI APIs from GenericHandler: https://chromium.googlesource.com/chromium/src/+/c9c27c4338cb1b8ad21a168d905cc4c964e857fb/content/browser/webui/generic_handler.cc#23

You can easily test this with the following snippet (crashes the tab, chrome://kill can normally not be opened by regular pages or extensions - see content::IsRendererDebugURL ):
chrome.send('navigateToUrl', ['chrome://kill', '', 0, false, false, false, false]);

Though webUI pages can seemingly already navigate to such URLs with standard JS APIs such as `location = ...` (as shown by my exploit).

### me...@google.com (2018-01-17)

Thanks, so navigateToUrl is the only additional API that an XSS will have access to.

I'm not entirely sure that's a security sensitive API though. Best it can do is DoS the browser by navigating to special URLs. Note that an extension can already emulate the behavior of chrome://kill by closing all tabs (https://crbug.com/chromium/180066). Beyond that, an extension doesn't seem to gain much by XSSing these interstitials.

### ro...@robwu.nl (2018-01-18)

@#14

chrome://quit's code path is very different from closing Chrome by closing all tabs using extension APIs.
chrome://restart allows extensions to restart Chrome (something that extensions cannot do (see ExtensionTabUtil::IsKillURL ).

I mainly view this vulnerability as a gadget to build automatic exploits for vulnerabilities surrounding the startup/shutdown logic of Chrome.
E.g. in the past I reported a UAF upon shutdown (https://crbug.com/chromium/518749), and in search for a gadget for a fast shutdown, I found and reported https://crbug.com/chromium/518827.

Now I don't have a new shutdown/startup vulnerability in mind this time, but I think that it's in the best interest of everyone to already report this vulnerability without waiting for more vulnerabilities to build a full exploit chain.

### ro...@robwu.nl (2018-01-19)

Merge rejected, so I'm changing the milestone label to 65.

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

The VRP Panel decided to award $1,000 for this report ($500 for the issue and $500 for the patch), as it wasn't clear what privileged webui APIs are actually accessible. They were willing to re-evaluate if you can show what additional privileges an attacker can achieve in this case.

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-23)

Supervised interstitials are not available from the web, there is an extension installation requirement, and the XSS gives limited privileges to the extension (navigating to chrome:// URLs). Given these, downgrading severity to low per severity guidelines, as this bug doesn't seem to meet medium severity criteria [1]. As awhalley@ said, happy to reevaluate in light of new information (which I think is quite probable).

[1] https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md



### me...@chromium.org (2018-01-23)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-23)

(And to be clear, I don't think this should decrease the reward amount)

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/797525?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>SupervisedUser, UI>Browser>WebUI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089994)*
