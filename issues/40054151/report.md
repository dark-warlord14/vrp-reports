# Security: Referrer Header Spoofing Vulnerability via <base> tags 

| Field | Value |
|-------|-------|
| **Issue ID** | [40054151](https://issues.chromium.org/issues/40054151) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>Referrer |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | te...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2020-12-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

While doing some analysis it was observed that when a <base> tag is set to a page and a css request is being made to a page, Chrome browser makes use of the url in base tag as a referrer header value , this is only valid in case a base header is set , in case the header is absent a plain requirest is made to the url for css call.

This was only observed with chrome and other browsers set the referrer to URI requesting the resource.

For example in below code, chrome doesnt set any referrer header automatically when making request to x.burpcollaborator.net .

<html><head>
<title>Test</title>
<style>
@import 'https://x.burpcollaborator.net/x';<!--change this to any address of your choice and verify the referrer header!-->
</style>
</head>
<body>
test
<body></html>

However in below code a referrer header is set to google.com in case base header is set , it can be set to any value

<html><head>
<title>Test/title>
<base href="https://www.gmail.com/">
<style>
@import 'https://x.burpcollaborator.net/x';<!--change this to any address of your choice and verify the referrer header!-->
</style>
</head>
<body>
test
<body></html>

**VERSION**  

Chrome Version: Latest (83.0.4103.61)  

Operating System: Windows, Mac , Android

**REPRODUCTION CASE**  

Please use below code and save it as html and open via chrome

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Ashish Gautam Kamble

## Timeline

### [Deleted User] (2020-12-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-15)

Thanks for your report. This might be a spec issue rather than a security issue. I'm unsure how an attacker could use this to endanger users, since they would already have to control the website in order to set the base tag.

Can you elaborate on how this might be leveraged into an attack? In the meantime, I will add some additional developers on this issue for their comment.

[Monorail components: Blink>SecurityFeature>Referrer]

### da...@chromium.org (2020-12-15)

[Empty comment from Monorail migration]

### da...@chromium.org (2020-12-15)

Hi, thanks: I was able to verify 

<base href="https://www.google.com">
<style>
    @import 'https://www.flickr.com/picture.jpg';
</style>

hosted on a non-google domain resulted in a google.com referrer.

Without the <base> tag, the request had no referrer (rather than a referrer of the initiating origin, which was what I expected).

This behavior seems to come from the following code:
- CSSParserContext's constructors look for a base URL (for instance from Document::BaseURL) and then set CSSParserContext::referrer_ from this value. [1]
- StyleRuleImport then uses this value when populating fetching arguments. [2]

[1]: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/css/parser/css_parser_context.cc;l=125;drc=ec0e29ae0cc41412b3c0594f1d94ceaa3d9e3870;bpv=1;bpt=1
[2]: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/css/style_rule_import.cc;l=152;drc=ec0e29ae0cc41412b3c0594f1d94ceaa3d9e3870;bpv=1;bpt=1?q=cssparsercontext::getreferrer&ss=chromium%2Fchromium%2Fsrc


I think this is a one-line fix and have written up crrev.com/c/2592447.

Mike is better equipped than me to assess whether there's a security impact.

### da...@chromium.org (2020-12-15)

(Lukasz, I initially added you because I was curious if this could lead to initiatior mismatches, but I think the answer is probably not: we just use this information to set the referrer, not the initiator.)

### wf...@chromium.org (2020-12-15)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-15)

assigning as per https://crbug.com/chromium/1158010#c4. I've given it Medium severity for now.

### da...@chromium.org (2020-12-15)

-> falken

Matt, I noticed you've submitted a change or two dealing with CSS fetching and particularly the base URL.

Could you please take a quick look at this report and help confirm whether the behavior described in the report is WAI, or whether it needs a fix (e.g. crrev.com/c/2592447)? 

Thanks!

### fa...@chromium.org (2020-12-15)

Looping in also yhirano@ who has more referrer experience, and domenic@ who has commented on the github issue.

I don't have a very quick answer. The two signals I'd look at are how other browsers behaves and what the spec says.

As for what the spec says, this is a bit hard to chase down. From what I see, it looks like the base URL should not affect Referrer.

1) I don't actually see where the CSS spec says to fetch @import URLs:
https://drafts.csswg.org/css-cascade-4/#at-ruledef-import

2) I assume it should do something similar to <link rel="stylesheet">. This seems to go here:
https://html.spec.whatwg.org/multipage/semantics.html#default-fetch-and-process-the-linked-resource

although there is a TODO and issue to use CSSOM's fetching steps instead:
https://github.com/whatwg/html/issues/968
https://drafts.csswg.org/cssom/#fetching-css-style-sheets

3) Looking at the Fetch spec, it appears to use the document URL rather than the document base URL for the referrer:
"If request’s referrer is not "no-referrer", set request’s referrer to the result of invoking determine request’s referrer. [REFERRER]" at https://fetch.spec.whatwg.org/#main-fetch
https://w3c.github.io/webappsec-referrer-policy/#determine-requests-referrer

I don't see anything that says to use base URL as the referrer anywhere.

So I think changing to use the document URL is indeed correct. It'd be good to see if other browsers do this too. It'd be especially interesting to see when the referrer code was written, if it came from WebKit days or was intentionally added later.

### fa...@chromium.org (2020-12-15)

+bashi@ who seems to have added the original change (but is likely ooo, +jochen as the reviewer):

https://codereview.chromium.org/314893003 for https://bugs.chromium.org/p/chromium/issues/detail?id=380457

This says "For css resources specified in stylesheets, their referrer should be set to the stylesheet's URL, not the document's URL." so this was intentional, but maybe base URL and stylesheet URL are different?



### mk...@chromium.org (2020-12-15)

1.  Unless something has changed in the last year or so, fetching for CSS is not yet well-defined. https://w3c.github.io/webappsec-referrer-policy/#integration-with-css hand-waves at the problem in ways that we considered good-enough while writing it, but it would be excellent for someone (not it!) to actually hammer out the integration. dom@ might be interested.

2.  Regardless of spec text, `<base>` should not influence the referrer. The text above points to what that change was supposed to achieve: the stylesheet's URL should be used as the referrer, not the document's URL. In this case, though, the stylesheet is inline in the document, so we do want to use the document's URL.

This does have security implications, insofar as some sites use `referer` as an access-control measure: it shouldn't be possible for a site to forge cross-origin `referer` headers. I'm not sure whether it's possible to send CORS-enabled requests from stylesheets (perhaps fonts?), but it would be interesting to verify that the `Origin` header and the `Sec-Fetch-Site` headers are behaving correctly as well, as I have vague recollections of those being wrapped up in the same data source as the referrer. TL;DR: Medium severity feels right.

### jo...@chromium.org (2020-12-15)

yeah, the intention is that if it's an inline stylesheet, the document's referrer should be used, but if it's an standalone stylesheet, that stylesheet's base URL (well, whatever it's called, it's not defined in CSS, but it should be a thing that can't be overwritten) should be used

### lu...@chromium.org (2020-12-15)

RE: https://crbug.com/chromium/1158010#c11: mkwst@: interesting to verify that the `Origin` header and the `Sec-Fetch-Site` headers are behaving correctly

Both `Origin` and `Sec-Fetch-Site` are based on network::ResourceRequest::request_initiator (soon-to-be-verified everywhere against `request_initiator_site_lock` and so unspoofable/protected against compromised renderers).

OTOH, (based on https://crbug.com/chromium/1158010#c12) it seems the `Referer` header can mismatch `request_initiator_site_lock` in the following scenario:

    a.com/main.html: <link rel="stylesheet" href="https://b.com/style.css">
    b.com/style.css: @import url("https://c.com/nested.css");

Here, the fetch for c.com/nested.css will use `Sec-Fetch-Site` based on request_initiator=a.com (all requests within the frame use the same URLLoaderFactory), but (based on https://crbug.com/chromium/1158010#c12) `Referer` should be based on b.com/style.css (IIUC) - the latter is incompatible with `request_initiator_origin_lock`.

So, if I understood the above correctly, then we get the following conclusion: `Referer` should not be used as an access-control measure / security mechanism (because it is not secure against compromised renderers).

### mk...@chromium.org (2020-12-15)

> Both `Origin` and `Sec-Fetch-Site` are ... unspoofable

Excellent, thanks Lukasz!

> it seems the `Referer` header can mismatch `request_initiator_site_lock` in the following scenario: ... `Referer` should not be used as an access-control measure

Correct. It shouldn't be used; other mechanisms are more robust. "Should", however, has little impact on "does". :) It would be ideal for us to limit the scenarios in which this mechanism has unexpected values to those that require actively corrupting the renderer. (So, I could live with "Low" severity instead of "Medium", but it's still a bug we ought to fix.)

### [Deleted User] (2020-12-15)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-15)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@chromium.org (2020-12-16)

[Empty comment from Monorail migration]

### mk...@google.com (2020-12-16)

[Empty comment from Monorail migration]

### es...@chromium.org (2020-12-16)

(I left a comment on https://crbug.com/chromium/1152999 about why I initially removed security labels, since that seems to have caused some confusion.)

### fa...@chromium.org (2020-12-16)

davidvc: would you like to own this again?

### da...@chromium.org (2020-12-16)

I'll take a look at the failing tests and try to get this in today.

### te...@gmail.com (2020-12-16)

will a CVE be assigned for this ?

### da...@chromium.org (2020-12-17)

CL in review (crrev.com/c/2592447)

### fa...@chromium.org (2020-12-17)

adding futhark@ for review context 

### te...@gmail.com (2020-12-21)

will a CVE be assigned for this ?


### te...@gmail.com (2020-12-21)

or i will have to apply for a cve


### ad...@google.com (2020-12-23)

A CVE will be assigned when we release the fix.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0b1539fcb923056624d4adc84b88140d367d92da

commit 0b1539fcb923056624d4adc84b88140d367d92da
Author: David Van Cleve <davidvc@chromium.org>
Date: Fri Jan 08 16:06:24 2021

css: Make fetches from inline CSS use the document's URL as referrer

Right now, fetches from inline CSS use the inline CSS's base URL
instead of the URL from the context that embeds the inline CSS: for
instance, loading a source-site.com page with the following code
  <base href="https://other-site.com">
  <style type=text/css> @import('best-sheet.com') </style>
should lead to the best-sheet.com sheet getting fetched with a
source-site.com referrer, but it will currently provide an
other-site.com referrer. However, if the imported sheet from
best-sheet.com makes more nested fetches, those nested requests should
use best-sheet.com as the basis for their referrers (as they do
currently).

This CL updates CSSParserContext's referrer setting logic to roughly do
the following:
- inline CSS: use the embedding document's URL as the referrer, or, for
srcdoc iframes, walk up the frame tree until hitting a non-srcdoc frame
- requests from fetched stylesheets: just as currently, use the fetched
sheet's URL as the basis for constructing the referrer

This seemed like it required refactoring CSSParserContext slightly
because there are constructors that take both a Document and a base URL,
and it's not obvious from the constructor signature whether the
Document or the base URL should be the one that provides the referrer.
To resolve this ambiguity, the refactor updates these CSSParserContext
constructors to take caller-provided Referrer objects.

Change-Id: If5a99d8057dff5e771e821d0e1f605566e28ff1d
Fixed: 1158645, 1158010
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2592447
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Commit-Queue: David Van Cleve <davidvc@chromium.org>
Cr-Commit-Position: refs/heads/master@{#841509}

[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/css/parser/css_parser_context.h
[add] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/web_tests/external/wpt/referrer-policy/css-integration/image/inline-style-with-differentorigin-base-tag.tentative.html
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/css/css_style_sheet.cc
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/html/track/vtt/vtt_parser.cc
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/css/selector_query.cc
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/html/link_style.cc
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/dom/processing_instruction.cc
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/css/style_rule_import.cc
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/web_tests/http/tests/css/resources/referrer-check.php
[add] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/web_tests/external/wpt/referrer-policy/css-integration/svg/inline-style-with-differentorigin-base-tag.tentative.html
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/css/selector_query_test.cc
[modify] https://crrev.com/0b1539fcb923056624d4adc84b88140d367d92da/third_party/blink/renderer/core/css/parser/css_parser_context.cc


### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-08)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-01-08)

+adetaylor: Hi Adrian! Is a medium-severity bug worth merging? The fix is relatively simple, but not totally trivial, and it's in some finicky, old code I'm not too familiar with. 

### ad...@chromium.org (2021-01-08)

Per policy yes, for externally reported medium severity bugs we do merge them back to both beta and stable. But if there's any doubt at all about stability risks, we don't, so I'll adjust labels thusly.

### te...@gmail.com (2021-01-12)

Hi @adetaylor@chromium.org . Will this be patched in upcoming chrome release 

### ad...@chromium.org (2021-01-12)

This will be released in Chrome 89 - due for release in March - https://chromiumdash.appspot.com/schedule

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-21)

Congratulation, Ashish - the VRP Panel has decided to award you $500 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your work and nice job! 

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-01-25)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-03-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e1505713dc313c6666b65b073bc7da9cfa1bf765

commit e1505713dc313c6666b65b073bc7da9cfa1bf765
Author: David Van Cleve <davidvc@chromium.org>
Date: Thu Mar 04 16:50:46 2021

css: Make fetches from inline CSS use the document's URL as referrer

Right now, fetches from inline CSS use the inline CSS's base URL
instead of the URL from the context that embeds the inline CSS: for
instance, loading a source-site.com page with the following code
  <base href="https://other-site.com">
  <style type=text/css> @import('best-sheet.com') </style>
should lead to the best-sheet.com sheet getting fetched with a
source-site.com referrer, but it will currently provide an
other-site.com referrer. However, if the imported sheet from
best-sheet.com makes more nested fetches, those nested requests should
use best-sheet.com as the basis for their referrers (as they do
currently).

This CL updates CSSParserContext's referrer setting logic to roughly do
the following:
- inline CSS: use the embedding document's URL as the referrer, or, for
srcdoc iframes, walk up the frame tree until hitting a non-srcdoc frame
- requests from fetched stylesheets: just as currently, use the fetched
sheet's URL as the basis for constructing the referrer

This seemed like it required refactoring CSSParserContext slightly
because there are constructors that take both a Document and a base URL,
and it's not obvious from the constructor signature whether the
Document or the base URL should be the one that provides the referrer.
To resolve this ambiguity, the refactor updates these CSSParserContext
constructors to take caller-provided Referrer objects.

(cherry picked from commit 0b1539fcb923056624d4adc84b88140d367d92da)

Change-Id: If5a99d8057dff5e771e821d0e1f605566e28ff1d
Fixed: 1158645, 1158010
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2592447
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Commit-Queue: David Van Cleve <davidvc@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#841509}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2731576
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1558}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/css/css_style_sheet.cc
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/css/parser/css_parser_context.cc
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/css/parser/css_parser_context.h
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/css/selector_query.cc
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/css/selector_query_test.cc
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/css/style_rule_import.cc
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/dom/processing_instruction.cc
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/html/link_style.cc
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/renderer/core/html/track/vtt/vtt_parser.cc
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/web_tests/external/wpt/referrer-policy/css-integration/image/inline-style-with-differentorigin-base-tag.tentative.html
[add] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/web_tests/external/wpt/referrer-policy/css-integration/svg/inline-style-with-differentorigin-base-tag.tentative.html
[modify] https://crrev.com/e1505713dc313c6666b65b073bc7da9cfa1bf765/third_party/blink/web_tests/http/tests/css/resources/referrer-check.php


### vs...@google.com (2021-03-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1158010?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1158645]
[Monorail mergedwith: crbug.com/chromium/1152999, crbug.com/chromium/1170235]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054151)*
