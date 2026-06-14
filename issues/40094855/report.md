# Security: Access-Control-Expose-Headers is not honored for redirects

| Field | Value |
|-------|-------|
| **Issue ID** | [40094855](https://issues.chromium.org/issues/40094855) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Network>XHR, Blink>SecurityFeature>CORS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2019-05-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

CORS defines a mechanism to hide custom response headers, unless explicitly allowed by listing in Access-Control-Expose-Headers. Chrome exposes all headers regardless, if response is a result of a redirect from first party to third-party.

I expect Chrome to follow other browsers behavior and only allow access to explicitly exposed headers.

All works as expected if there is no redirect and request goes directly to third-party.

**VERSION**  

Chrome Version: Version 73.0.3683.103 (Official Build) (64-bit)  

as well as Version 76.0.3784.1 (Official Build) canary (64-bit)  

Operating System: MacOS 10.13.6

**REPRODUCTION CASE**  

Attached is a simple golang program that reproduces the problem. It hardcodes the domain name, so you would need to map `origin` to the IP of the network interface that servers are listening on.  

Loading `http://origin:8001` prints both allowed and disallowed header values in the console.  

Expected result is to only print the allowed header value.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Sergey Shekyan (Shape Security)

## Attachments

- deleted (application/octet-stream, 0 B)
- [cors_redirect_testcase.go](attachments/cors_redirect_testcase.go) (text/plain, 1.4 KB)

## Timeline

### ad...@google.com (2019-05-03)

shekyan@gmail.com: Thanks for the report!

I think your test case may be incomplete. There's nothing listening on port 9999 to provide the x-a and x-b headers in the first place.

I'm happy to work on expanding the test case based on your description, but I thought I'd ask first if there's a bit more you intended to provide. Thanks!

### sh...@gmail.com (2019-05-03)

Oh. Sorry, wrong test case!

### sh...@gmail.com (2019-05-03)

Here is the part of the fetch spec that describes `Access-Control-Expose-Headers`, for convenience: https://fetch.spec.whatwg.org/#http-access-control-expose-headers

### ad...@google.com (2019-05-03)

Thanks very much!

OK, it behaves for me as described, though to work around some Google networking restrictions I had to change 'origin' to 'localhost' in the script.

I don't know enough about CORS to know if this is a bug, so sending to our CORS team for a look.

[Monorail components: Blink>SecurityFeature>CORS]

### sh...@chromium.org (2019-05-04)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-04)

[Empty comment from Monorail migration]

### yh...@chromium.org (2019-05-07)

Reproducible with and without OOR-CORS.
Unreproducible with Firefox.

### yh...@chromium.org (2019-05-07)

Unreproducible with Fetch API. This may be an XHR problem.

### yh...@chromium.org (2019-05-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>Network>XHR]

### yh...@chromium.org (2019-05-07)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/08cc019f3f8c86d24330b4e3770bc2674000937c

commit 08cc019f3f8c86d24330b4e3770bc2674000937c
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed May 08 07:21:52 2019

[XHR] Use response tainting to calculate CORS-exposed header-name list

XHR uses the same-originness of the request origin and the destination
URL to calculate the CORS-exposed header-name list, which leads to
wrong results with redirects. Use response tainting as specced.

Bug: 959390
Change-Id: Iec448dfe7d2b47d00f0f471391eb7918a1fe7bc4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1598949
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#657626}

[modify] https://crrev.com/08cc019f3f8c86d24330b4e3770bc2674000937c/third_party/blink/renderer/core/xmlhttprequest/xml_http_request.cc
[modify] https://crrev.com/08cc019f3f8c86d24330b4e3770bc2674000937c/third_party/blink/renderer/core/xmlhttprequest/xml_http_request.h
[add] https://crrev.com/08cc019f3f8c86d24330b4e3770bc2674000937c/third_party/blink/web_tests/external/wpt/xhr/access-control-expose-headers-on-redirect.html


### yh...@chromium.org (2019-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-10)

This bug requires manual review: M75 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-05-10)

yhirano@ pls share canary results for this change. 

adetaylor@ to review merge request 

### yh...@chromium.org (2019-05-10)

I haven't received any bad news from Canary.

### sh...@chromium.org (2019-05-10)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-05-10)

adetaylor@ pls confirm you are good with this merge request

### ad...@chromium.org (2019-05-10)

Makes sense to me to merge to M75.

### sr...@google.com (2019-05-10)

approving for M75, branch:3770

### sh...@chromium.org (2019-05-11)

[Empty comment from Monorail migration]

### cr...@appspot.gserviceaccount.com (2019-05-13)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/31502a47261d12dce71daf41b34511251d0ef019

Commit: 31502a47261d12dce71daf41b34511251d0ef019
Author: yhirano@chromium.org
Commiter: yhirano@chromium.org
Date: 2019-05-13 02:29:41 +0000 UTC

[XHR] Use response tainting to calculate CORS-exposed header-name list

XHR uses the same-originness of the request origin and the destination
URL to calculate the CORS-exposed header-name list, which leads to
wrong results with redirects. Use response tainting as specced.

TBR=yhirano@chromium.org

(cherry picked from commit 08cc019f3f8c86d24330b4e3770bc2674000937c)

Bug: 959390
Change-Id: Iec448dfe7d2b47d00f0f471391eb7918a1fe7bc4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1598949
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#657626}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1608860
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/branch-heads/3770@{#549}
Cr-Branched-From: a9eee1c7c727ef42a15d86e9fa7b77ff0e63840a-refs/heads/master@{#652427}


### na...@google.com (2019-05-13)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-06-20)

Congrats the Panel decided to reward $500 for this report. 

### na...@google.com (2019-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/959390?no_tracker_redirect=1

[Multiple monorail components: Blink>Network>XHR, Blink>SecurityFeature>CORS]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094855)*
