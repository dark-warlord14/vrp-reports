# Referrer Spoof using <base href> and <style>

| Field | Value |
|-------|-------|
| **Issue ID** | [40056681](https://issues.chromium.org/issues/40056681) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>Referrer |
| **Platforms** | Linux |
| **Reporter** | pr...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2021-07-27 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36

Steps to reproduce the problem:
The bug was originally filed by Jun (https://crbug.com/1152999) and was fixed recently. However, it still works in latest versions of Chrome Canary and Dev;

Steps to reproduce:
1. Open DevTools and switch to Network Tab
2. Visit https://cm2.pw/?xss=%3Cbase+href=//g.co%3E%3Cstyle%3E@import+//t.co%3C/style%3E
3. Notice the referer header sent to t.co

What is the expected behavior?
The referer should have been set to requesting domain instead of baseURI.

What went wrong?
The referer got spoofed.

Did this work before? N/A 

Chrome version: 93.0.4577.8  Channel: dev
OS Version: 

Link to original report-https://bugs.chromium.org/p/chromium/issues/detail?id=1152999

Please credit Jun as he is the original reporter.

## Attachments

- [Screenshot_google-chrome-unstable_20210727110808.png](attachments/Screenshot_google-chrome-unstable_20210727110808.png) (image/png, 144.9 KB)
- [Screenshot_select-area_20210727112519.png](attachments/Screenshot_select-area_20210727112519.png) (image/png, 66.4 KB)
- [Screenshot_select-area_20210727112553.png](attachments/Screenshot_select-area_20210727112553.png) (image/png, 39.7 KB)

## Timeline

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-07-27)

I can repro. davidvc, could you PTAL?

[Monorail components: Blink>SecurityFeature>Referrer]

### da...@chromium.org (2021-07-27)

Hi Rune, are you a good owner for bugs in the CSS stylesheet fetching code? Thanks!

### [Deleted User] (2021-07-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### fu...@chromium.org (2021-08-02)

davidcv@: Isn't this what you fixed in https://crbug.com/chromium/1158010? Was anything missing in that change?


### da...@chromium.org (2021-08-04)

I'll take a look at the repro case tomorrow morning and see if it seems to be the same issue.

### da...@chromium.org (2021-08-04)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-08-04)

-RBS, since this isn't a regression

### [Deleted User] (2021-08-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-08-05)

+Ade

Hi Ade, this bug is actually covering the fact that our fix to an older, and longstanding, Sev-Medium did not cover one codepath where the behavior in that bug can trigger. (There is a "preload" and a "non-preload" path, and the fix in https://crbug.com/chromium/1158010 only covered the "non-preload" path.)

Is this collection of labels right?

Thanks!

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-08-05)

To summarize the issue in this bug:

We request inline stylesheets from multiple places, in particular from the HTML preloader as well as from the CSS parser. The fix in https://crbug.com/chromium/1158010 only covered the path in the CSS parser. While we wrote a WPT that failed without the patch applied and passed with the patch applied, this WPT did not cover the preload path. The necessary work to resolve this issue is to fix the code path from the HTML preloader, too, and then add test coverage for the HTML preloader code path. I'll also manually verify that the repro case does not work post-fix, which I (whoops: my first security bug!) did not do in the last case.

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-08-07)

+yoavweiss for context since I see Yoav has worked on the preload code 

### mk...@chromium.org (2021-08-16)

+dom for referrer policy.

### yo...@chromium.org (2021-08-16)

I suspect that it may be sufficient to modify the kBaseUrlIsReferrer in [1] to kDocumentIsReferrer.

It seems like we explicitly wanted [2] the referrer of these styles to be the base URL, rather than the document. Adding estark@ and jochen@ who may have more context on that.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/parser/css_preload_scanner.cc;l=262?q=CSSPreloadScanner&ss=chromium%2Fchromium%2Fsrc
[2] https://codereview.chromium.org/2808663003/

### da...@chromium.org (2021-08-16)

Drafted up a CL last week at crrev.com/c/3078937

Thanks Yoav for the confirmation that the approach seems reasonable!

Might be taking a sick day today---should just take a little polish tomorrow to get it out the door 

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-08-30)

Getting https://crbug.com/chromium/1233375#c22's change out the door fell victim to Perf but it's in my queue for this week.

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-09-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1eb5454949672457a4bc6fafa538da6486cdf3b8

commit 1eb5454949672457a4bc6fafa538da6486cdf3b8
Author: David Van Cleve <davidvc@chromium.org>
Date: Thu Sep 23 01:56:50 2021

css: Use document (not base) URL for inline style preloads' referrers

crrev.com/c/2592447 fixed one code path where setting a document's base
URL (via the HTML <base> tag) led to requests from inline CSS using the
base URL as their referrer, rather than the document URL. This goes
against the recommendation in the Referrer Policy spec that requests
from inline CSS use their documents' referrers. [1] In general, we try
to avoid letting pages override outgoing requests' referrers to
different-origin URLs, even though this is not a hard security boundary.

It turns out a separate code path can also trigger requests from inline
style sheets: in particular, '@import' statements in inline stylesheets
get prefetched by the HTML parser, which currently has separate logic
that explicitly sets those requests' referrers to the document's base
URL.

This change removes that logic. After this change, preload requests from
inline style in the HTML parser will use the document's URL, not its
base URL, when generating their referrers. This CL also adds two new WPTs:
* "stylesheet-with-differentorigin-base-url.html" verifies the referrer
for an inline stylesheet requesting another stylesheet via an @import
statement. There are other tests inspecting the referrers for SVG and
image fetches from inline stylesheets, but not for child stylesheet
fetches. This test passes even without this CL applied (because of
crrev.com/c/2592447).
* "stylesheet-with-differentorigin-base-url-from-preload.html" does the
same thing, except from a srcdoc iframe. Using a srcdoc iframe triggers
the preload code path since the inline stylesheet is hardcoded in a
<style> HTML tag. (In contrast, the test above uses JS to add the style
element to the DOM.) Because this second test exercises the preload
codepath, it fails without this patch's functional changes applied.

With this patch applied, the repro in the linked bug no longer succeeds.

[1] https://www.w3.org/TR/referrer-policy/#integration-with-css

Test: New WPT covers the preload path. Manually tested the bug's repro.
Change-Id: I6bd797978b207a4bc0bb1b35565eb93c7162729f
Fixed: 1233375
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3078937
Commit-Queue: David Van Cleve <davidvc@chromium.org>
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Reviewed-by: Emily Stark <estark@chromium.org>
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Cr-Commit-Position: refs/heads/main@{#924146}

[modify] https://crrev.com/1eb5454949672457a4bc6fafa538da6486cdf3b8/third_party/blink/renderer/core/html/parser/preload_request.cc
[modify] https://crrev.com/1eb5454949672457a4bc6fafa538da6486cdf3b8/third_party/blink/renderer/core/html/parser/preload_request.h
[modify] https://crrev.com/1eb5454949672457a4bc6fafa538da6486cdf3b8/third_party/blink/renderer/core/html/parser/css_preload_scanner.cc
[modify] https://crrev.com/1eb5454949672457a4bc6fafa538da6486cdf3b8/third_party/blink/renderer/core/html/parser/html_preload_scanner.cc
[add] https://crrev.com/1eb5454949672457a4bc6fafa538da6486cdf3b8/third_party/blink/web_tests/external/wpt/referrer-policy/css-integration/child-css/internal-import-stylesheet-with-differentorigin-base-url-from-preload.tentative.html
[modify] https://crrev.com/1eb5454949672457a4bc6fafa538da6486cdf3b8/third_party/blink/web_tests/external/wpt/common/security-features/subresource/stylesheet.py
[modify] https://crrev.com/1eb5454949672457a4bc6fafa538da6486cdf3b8/third_party/blink/renderer/core/html/parser/html_resource_preloader_test.cc
[add] https://crrev.com/1eb5454949672457a4bc6fafa538da6486cdf3b8/third_party/blink/web_tests/external/wpt/referrer-policy/css-integration/child-css/internal-import-stylesheet-with-differentorigin-base-url.tentative.html


### [Deleted User] (2021-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-09-23)

cc += homesen83@gmail.com, the reporter of the duplicate https://crbug.com/chromium/1251401

### da...@chromium.org (2021-09-29)

cc += the co-reporters of another duplicate, https://crbug.com/chromium/1244322

### da...@chromium.org (2021-09-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-30)

Hello, Prakash - the VRP Panel has decided to reward you $500 for this report as a thank you for your efforts. 

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

(Sheriffbot didn't ask for merges here. That Sheriffbot bug is tracked as https://crbug.com/chromium/1262390).

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1233375?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1244322, crbug.com/chromium/1251401]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056681)*
