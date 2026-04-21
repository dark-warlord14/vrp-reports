# Security: iframe.contentWindow.location.href can bypass CSP for javascript URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40093235](https://issues.chromium.org/issues/40093235) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Loader, Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ac...@meta.com |
| **Assignee** | ac...@meta.com |
| **Created** | 2018-11-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

A parent document with a CSP that does not allow unsafe inline scripts can still execute JavaScript URLs in inline iframes if using the iframe content window's location.href to navigate.

This occurs because asynchronous `javascript:` URL navigations (such as those from location.href) do not check the parent document's CSP in the posted task- only the document of the embedded frame's CSP is checked (see ScriptController::ExecuteScriptIfJavascriptURL). Setting an iframe's document with the `src` attribute blocks this as expected due to the extra synchronous checks in HTMLFrameElementBase::OpenURL.

I discovered this when working on <https://crbug.com/chromium/638435>, as it caused the Web Platform Test `content-security-policy/navigation/to-javascript-url-script-src.html` to fail when I was migrating iframe.src navigations to be async (case "<iframe src='...'> with 'unsafe-inline' navigated to 'javascript:' blocked in this document").

More details on expected behaviour can be found here: <https://github.com/w3c/webappsec-csp/issues/127>

Please let me know if you need any more info!

**VERSION**

Chrome Versions:

- Trunk (r612476)
- 70.0.3538.110 + stable  
  
  Operating System: Ubuntu 18.04.1 LTS

**REPRODUCTION CASE**

Load the attached file test.html in Chrome, with both test.html and test\_frame.html hosted on an HTTP server. Observe that the iframe whose source is set with location.href erroneously executes the JavaScript URL, and prints "FAIL (JS URL executed)". The iframe whose source is set with the `src` attribute blocks this as expected.

This test passes for both cases in Firefox.

## Attachments

- [test.html](attachments/test.html) (text/plain, 812 B)
- [test_frame.html](attachments/test_frame.html) (text/plain, 21 B)

## Timeline

### ac...@meta.com (2018-11-28)

[Empty comment from Monorail migration]

### to...@chromium.org (2018-11-29)

Set Loader and SecurityFeature components labels.
Also, explicitly add mkwst to the CC list for CSP.

I guess you find this while making a patch in https://chromium-review.googlesource.com/c/chromium/src/+/1334589.

I haven't checked the last patch yet, due to high-priority works for the coming branch-cut. But, could you fix this issue by your patch, or still you need some extra works?

[Monorail components: Blink>Loader Blink>SecurityFeature]

### ac...@meta.com (2018-11-30)

> I guess you find this while making a patch in https://chromium-review.googlesource.com/c/chromium/src/+/1334589.

Yup, that's right :)

> I haven't checked the last patch yet, due to high-priority works for the coming branch-cut. But, could you fix this issue by your patch, or still you need some extra works?

The latest version of my patch makes async iframe.src navigations check the source browsing context's CSP, so it's not vulnerable to this (nor was it with synchronous navigations before the patch). I can write a quick separate patch to make location.href check the source browsing context's CSP as well, if you'd like.

### ac...@meta.com (2018-11-30)

[Description Changed]

### ct...@chromium.org (2018-12-01)

We'd gladly take a patch to fix this if you want to upload one :-).

A separate patch would make this easier if we decide we should merge back to release branches (although we've treated similar partial CSP bypasses as Severity-Low in the past, e.g. https://crbug.com/chromium/534570, so we might end up not merging unless the fix is very simple).

Also adding andypaicu@ for more CSP expertise.

### ct...@chromium.org (2018-12-01)

[Empty comment from Monorail migration]

### ac...@meta.com (2018-12-04)

Sure thing. I've got a patch ready -- what's the recommended way to publish security-sensitive CLs via Gerrit? It looks like `--private` uploads are disabled.

### ac...@meta.com (2018-12-04)

Ended up just making a --no-autocc CL (https://chromium-review.googlesource.com/c/chromium/src/+/1359823/) similar to other Severity-Low related CLs I've seen. Hope that's alright!

### ct...@chromium.org (2018-12-04)

It's okay to make public CLs for security bugs. Our general approach is to avoid highly security related language in the CL title/description but in general we don't worry about it much (e.g., no "Fix security bug in X", but "Check for null before accessing X" is fine).

### to...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0e3b0c22a5c596bdc24a391b3f02952c1c3e4f1b

commit 0e3b0c22a5c596bdc24a391b3f02952c1c3e4f1b
Author: Andrew Comminos <acomminos@fb.com>
Date: Thu Dec 06 19:37:49 2018

Check the source browsing context's CSP in Location::SetLocation prior to dispatching a navigation to a `javascript:` URL.

Makes `javascript:` navigations via window.location.href compliant with
https://html.spec.whatwg.org/#navigate, which states that the source
browsing context must be checked (rather than the current browsing
context).

Bug: 909865
Change-Id: Id6aef6eef56865e164816c67eb9fe07ea1cb1b4e
Reviewed-on: https://chromium-review.googlesource.com/c/1359823
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Andrew Comminos <acomminos@fb.com>
Cr-Commit-Position: refs/heads/master@{#614451}
[modify] https://crrev.com/0e3b0c22a5c596bdc24a391b3f02952c1c3e4f1b/third_party/blink/renderer/core/frame/location.cc
[add] https://crrev.com/0e3b0c22a5c596bdc24a391b3f02952c1c3e4f1b/third_party/blink/web_tests/external/wpt/content-security-policy/navigation/to-javascript-parent-initiated-parent-csp-disallow.html


### ac...@meta.com (2018-12-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-07)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-10)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-13)

Thank you for your report. The VRP Panel has decided to reward you $500 + $500 bonus for providing a patch. Since you are a new reporter a member of our finance will be in touch. 

Additionally, how would you like to be credited in release notes?

### ac...@meta.com (2018-12-13)

You can credit me as Andrew Comminos of Facebook. Thanks!

### aw...@google.com (2018-12-14)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-27)

please claim your reward by 1/31/2020. Otherwise it will be donated to charity. 

### na...@google.com (2020-01-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-03)

Extending the time period to claim this award to 3/31/2020.

### na...@google.com (2020-03-18)

Friendly reminder to claim this award by March 31, 2020. 

### na...@google.com (2020-04-02)

Extending this until to July 31, 2020

### am...@chromium.org (2021-03-22)

reward unclaimed; being donated to charitable organization

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/909865?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, Blink>SecurityFeature]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093235)*
