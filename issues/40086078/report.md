# Security: CSP in WebUI can trivially be bypassed by extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40086078](https://issues.chromium.org/issues/40086078) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Platform>Extensions, UI>Browser>WebUI |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-11-25 |
| **Bounty** | $1,000.00 |

## Description

chrome-extension: resources are not blocked by the content security policy [1]. This makes sense for regular web pages, over which extensions take priority. This is less desirable on WebUI pages, which are parts of Chrome that are more privileged than extensions.

I have found a XSS vulnerability that uses this bug to run a program outside of Chrome (to be reported separately).


This is the recipe for exploitation:
1. Create an extension with a script that you want to run (e.g. s.js), put this in web_accessible_resources.
2. Put the following in the injected HTML: <script src="chrome-extension://[extensionid]/s.js"></script>
   (If the HTML is assigned via innerHTML, put it in a <iframe srcdoc="<script>..."> to make sure that the script is parser-inserted)
3. Open the WebUI page with a XSS/HTML injection vulnerability (using the chrome.tabs.create extension API).

The above recipe even works if the CSP is default-src 'none'.

I suggest to not allow chrome-extension:-URLs to bypass CSP on WebUI pages, except possibly for URLs from component extensions (these are trusted parts of Chrome, so there is no need to block them; doing so may even break their functionality).


[1] https://www.w3.org/TR/2016/WD-CSP3-20160901/#extensions

## Timeline

### ro...@robwu.nl (2016-11-25)

https://crbug.com/chromium/668653 shows an exploit where an external program (mspaint) is launched through XSS in a WebUI page.

### ro...@robwu.nl (2016-11-28)

Cc-ing reviewers for my patches to https://crbug.com/chromium/668653.

### mk...@chromium.org (2016-11-28)

There's an experiment in that prevents `chrome-extension://` URLs from automatically bypassing CSP for parser-inserted scripts like `innerHTML` (see https://crbug.com/chromium/653521 and  https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.cpp?rcl=0&l=591). Exploits like this are a good argument in favor of shipping it.

WDYT, rdevlin.cronin@?

### ro...@robwu.nl (2016-11-28)

Mind ccing me on https://crbug.com/chromium/653521?

### oc...@chromium.org (2016-11-29)

Assuming this impacts Stable. I'm going to give this one a Low because of this requires an XSS on a webui page + extension to be installed.

### sh...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-12)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-12-12)

@3 - I think that this decision can be orthogonal https://crbug.com/chromium/653521.  We already (mostly) disallow script injection on chrome:// urls, so there's no reason CSP bypasses should be allowed.

### aw...@google.com (2016-12-16)

Note to VRP Panel: please consider in conjunction with 668653

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-26)

Hi folks - been a while with no movement on this bug. What are the next steps here?  Mike, are you still the best owner?

### sh...@chromium.org (2017-02-10)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2017-04-20)

+estark as another CSP owner. 

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### rs...@chromium.org (2017-05-02)

estark/mkwst: Any update on this issue?

### es...@chromium.org (2017-05-26)

I'm not that familiar with this area. Is ShouldBypassMainWorldCSP() what controls whether CSP is bypassed in this scenario? If so, is there any way in Blink to check whether a page is WebUI so that we can avoid bypassing?

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2017-07-12)

I've created a patch that implements my suggestion from the initial report:
https://chromium-review.googlesource.com/c/567499/

I wonder why the bot stopped nagging 5 months ago despite the lack of activity on this bug.

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-08-29)

Friendly security sheriff ping: it looks like the CL https://chromium-review.googlesource.com/c/567499/ has gotten stuck in review. Can we please move ahead with implementation / are there any blockers which are preventing moving ahead?

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/956801d1098d266fe794c9b1a137aadc259b84f1

commit 956801d1098d266fe794c9b1a137aadc259b84f1
Author: Rob Wu <rob@robwu.nl>
Date: Wed Jan 10 17:06:31 2018

Never bypass CSP in WebUI pages

BUG=668645
TEST=browser_test --gtest_filter=ExtensionCSPBypassTest.LoadWebAccessibleScript

Change-Id: I03a96a742b06ca6ec81fad95aae17cbdb11e1cce
Reviewed-on: https://chromium-review.googlesource.com/567499
Commit-Queue: Rob Wu <rob@robwu.nl>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528343}
[add] https://crrev.com/956801d1098d266fe794c9b1a137aadc259b84f1/chrome/browser/extensions/extension_csp_bypass_browsertest.cc
[modify] https://crrev.com/956801d1098d266fe794c9b1a137aadc259b84f1/chrome/test/BUILD.gn
[modify] https://crrev.com/956801d1098d266fe794c9b1a137aadc259b84f1/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.cpp
[modify] https://crrev.com/956801d1098d266fe794c9b1a137aadc259b84f1/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicyTest.cpp
[modify] https://crrev.com/956801d1098d266fe794c9b1a137aadc259b84f1/third_party/WebKit/Source/platform/weborigin/SchemeRegistry.cpp
[modify] https://crrev.com/956801d1098d266fe794c9b1a137aadc259b84f1/third_party/WebKit/Source/platform/weborigin/SchemeRegistry.h


### ro...@robwu.nl (2018-01-14)

Verified fixed in 65.0.3322.0. Visiting chrome://version and executing the following in the JS console results in the expected error below:
var s = document.createElement('script');
s.src = 'chrome-extension://foo';
document.head.append(s);

Refused to load the script 'chrome-extension://foo/' because it violates the following Content Security Policy directive: "script-src chrome://resources 'self' 'unsafe-eval'".

### sh...@chromium.org (2018-01-14)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2018-01-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-06)

Thanks Rob! The VRP panel awarded $500 for this report and $500 for the patch. Cheers!

### aw...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

govind@ - good for 65

### go...@chromium.org (2018-02-09)

Approving merge to M65 branch 3325 based on https://crbug.com/chromium/668645#c38. Please merge ASAP so we can pick it up for next week Beta release. Thank you.

### ro...@robwu.nl (2018-02-09)

No need to merge; 956801d1098d266fe794c9b1a137aadc259b84f1 is already on M65:
https://chromium.googlesource.com/chromium/src.git/+/956801d1098d266fe794c9b1a137aadc259b84f1/chrome/VERSION

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/668645?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Platform>Extensions, UI>Browser>WebUI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086078)*
