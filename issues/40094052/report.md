# Security: CSP violation reports leak the destination origin of a blocked redirect in the blocked-uri / blockedURI field

| Field | Value |
|-------|-------|
| **Issue ID** | [40094052](https://issues.chromium.org/issues/40094052) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | an...@chromium.org |
| **Created** | 2019-02-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A malicious page can abuse CSP violation reports to determine not only whether a request results in a cross-origin redirect, but also the origin of the redirection target, because the origin of the blocked resource is sent in the blocked-uri field of CSP reports and the blockedURI member of the securitypolicyviolation event.  

This is incorrect; the requested URL should be reported instead of the (blocked) destination URL.

From <https://w3c.github.io/webappsec-csp/#create-violation-for-request> :

> Note: We use request’s url, and not its current url, as the latter might contain information about redirect targets to which the page MUST NOT be given access.

**VERSION**  

Chrome Version: 72.0.3626.109 (stable), 74.0.3709.0 (canary)

**REPRODUCTION CASE**  

Open the attached HTML file in Chrome.  

The page registers a "securitypolicyviolation" event listener, and loads of an attachment (from origin bugs.chromium.org via an <img>) of a (currently) non-public bug (<https://crbug.com/chromium/805557> at the time of writing).

- If you are not logged in, a redirect to accounts.google.com occurs.
- If you are logged in and have access to the bug, a redirect to some long googleusercontent.com subdomain occurs.
- If you are logged in and have no access to the bug (e.g. log in via a Google account without security access), no redirect occurs.

Because of this bug, the test page detects the redirection target via blockedURI and able to tell which of these events occurred.

What should have happened is that the blockedURI contains the originally requested URL (at bugs.chromium.org).  

This is what Firefox does, in compliance with the CSP spec.

The kind of bug was previously reported at <https://crbug.com/chromium/633306>, but only partially fixed.

## Attachments

- [securitypolicyviolation-blocked-uri.html](attachments/securitypolicyviolation-blocked-uri.html) (text/plain, 2.3 KB)

## Timeline

### mk...@chromium.org (2019-02-18)

Perhaps andypaicu@ has some spare cycles to take a look at this? We should update our implementation to CSP3's mandate rather than CSP2's.

### sh...@chromium.org (2019-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-02)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-17)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2019-04-01)

Friendly security sheriff ping. Any updates on this?

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-26)

Andy, what's the status here?

### dr...@chromium.org (2019-05-30)

Friendly security sheriff ping - any update on this?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

andypaicu@, friendly ping from the security marshal.

### an...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

mkwst@: can you help us move this forward a bit? Thanks!

- a friendly security marshal

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### mk...@chromium.org (2019-11-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### ar...@chromium.org (2019-12-19)

I will own this.

### ar...@chromium.org (2019-12-19)

Okay, so this is not a regression, but an new thing to implement instead.
The new spec requires the reported URL to be the initial URL, not the blocked one.
This shouldn't be very hard to implement, but it requires many patches for, because of all the directives.

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-04-30)

[Empty comment from Monorail migration]

### ar...@google.com (2020-05-04)

+antoniosartori, who just started looking into this.

### an...@chromium.org (2020-05-06)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778

commit 74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Tue May 19 15:59:40 2020

Use original URL before redirects as blocked URL in CSP reporting

When a resource was being blocked because of a Content Security Policy
violation after a redirect happened, we were using the final
URL (after the redirect) in the CSP reporting. This is a security
issue, since it could expose confidential information such as a token
contained in the redirect URL. As stated in
https://w3c.github.io/webappsec-csp/#create-violation-for-request
("We use request's url, and not its current url, as the latter might
contain information about redirect targets to which the page MUST NOT
be given access."), whe should instead report the request's original URL.

Bug: 932892
Change-Id: I1864e6e9e4cc266615e49276012ba7f9d96672f7
Fixed: 932892
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2181363
Reviewed-by: Camille Lamy <clamy@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Cr-Commit-Position: refs/heads/master@{#770126}

[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/content/browser/frame_host/mixed_content_navigation_throttle.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/content/common/frame_messages.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/public/web/web_local_frame.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/fetch/fetch_manager.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/csp/content_security_policy.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/csp/content_security_policy.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/csp/content_security_policy_test.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/csp/csp_directive_list.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/csp/csp_directive_list.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/csp/csp_directive_list_test.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/dom_window.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/local_dom_window.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/web_local_frame_impl.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/frame/web_local_frame_impl.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/html/html_plugin_element.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/html/link_style.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/html/media/html_media_element.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/base_fetch_context.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/base_fetch_context.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/base_fetch_context_test.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/frame_fetch_context.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/frame_fetch_context.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/frame_fetch_context_test.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/mixed_content_checker.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/mixed_content_checker.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/mixed_content_checker_test.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/ping_loader.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/threadable_loader.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/worker_fetch_context.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/loader/worker_fetch_context.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/workers/main_thread_worklet_test.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/workers/threaded_worklet_test.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/core/workers/worker_global_scope.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/modules/background_fetch/background_fetch_manager.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/modules/websockets/websocket_common.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/modules/webtransport/quic_transport.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/platform/loader/fetch/fetch_context.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/platform/loader/fetch/resource_loader.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/platform/loader/fetch/resource_request.cc
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/platform/loader/fetch/resource_request.h
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/renderer/platform/loader/testing/mock_fetch_context.h
[add] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/report-original-url-on-mixed-content-frame.https.sub.html
[add] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/report-original-url-on-mixed-content-frame.https.sub.html.sub.headers
[modify] https://crrev.com/74ac20cceb7d7fbceac0e1c2f9300c86e7c8c778/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/report-original-url.sub.html


### [Deleted User] (2020-05-19)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-26)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-29)

Congrats! The Panel decided to award $1,000 for this report. 

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/94ec3d7ec0bb6707b21f82e7efb93574c5151a40

commit 94ec3d7ec0bb6707b21f82e7efb93574c5151a40
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Tue Mar 09 14:27:14 2021

CSP: Add WPT for uri-before-redirects in spv

This adds a simple Web Platform Test for Content Security Policies
checking that if a violation occurs after a redirect, the blockedURI
contained in the securitypolicyviolation event is the original request
URI (before redirects).

Bug: 932892
Change-Id: I291caa3ea6e3a0fe003e5852518365eb5db29bbb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2744042
Auto-Submit: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#861141}

[add] https://crrev.com/94ec3d7ec0bb6707b21f82e7efb93574c5151a40/third_party/blink/web_tests/external/wpt/content-security-policy/securitypolicyviolation/img-src-redirect.sub.html


### an...@chromium.org (2021-03-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/58591c894e170acba5f0ce19850fe0ef0f59549c

commit 58591c894e170acba5f0ce19850fe0ef0f59549c
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Wed Apr 21 06:54:33 2021

CSP: Use request URL as blocked URL in browser

In Content Security Policy violation reports, the field `blockedURI`
must be filled with the blocked request's URL, and not the response
URL, since the latter could leak cross-origin information to the
context that initiated the request.

For checks performed by Blink, this was already addressed by
https://crrev.com/c/2181363. This CL fixes the behaviour also for
checks performed by the browser. At the moment, the only thing
actually affected by this is 'form-action' after redirects (although
reporting is partially broken for form-action, see failing WPT
content-security-policy/form-action/form-action-src-redirect-blocked.sub.html).
The directives 'navigate-to' and 'prefetch-src' will be affected once
they ship.

We explicitly exclude 'frame-src' from this logic because it is not
clear what to do. Reporting anything at all for 'frame-src' violations
is problematic
(https://github.com/web-platform-tests/wpt/issues/27384), and we
should probably consider dropping reporting completely for frame-src.
Since we are missing better alternatives, for 'frame-src' we keep
using response's URL stripped to the origin.

Change-Id: I47fee7b7c8ae6e152528c83abc238acb3239e10e
Bug: 932892,1172898
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2799711
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#874593}

[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/content/browser/renderer_host/ancestor_throttle.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/content/browser/renderer_host/form_submission_throttle.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/content/browser/renderer_host/navigation_controller_impl.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/content/browser/renderer_host/render_frame_host_csp_context.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/services/network/public/cpp/content_security_policy/content_security_policy.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/services/network/public/cpp/content_security_policy/content_security_policy.h
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/services/network/public/cpp/content_security_policy/content_security_policy_unittest.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/services/network/public/cpp/content_security_policy/csp_context.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/services/network/public/cpp/content_security_policy/csp_context.h
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/services/network/public/cpp/content_security_policy/csp_context_unittest.cc
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/third_party/blink/web_tests/http/tests/security/contentSecurityPolicy/1.1/form-action-src-get-blocked-with-redirect-expected.txt
[modify] https://crrev.com/58591c894e170acba5f0ce19850fe0ef0f59549c/third_party/blink/web_tests/http/tests/security/contentSecurityPolicy/1.1/form-action-src-redirect-blocked-expected.txt


### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/932892?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Blink>SecurityFeature>ContentSecurityPolicy]
[Monorail mergedwith: crbug.com/chromium/1055049, crbug.com/chromium/613960]
[Monorail components added to Component Tags custom field.]

### mi...@gmail.com (2025-10-21)

Seen this on server logs with UA string

Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_15\_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36

Our server responded with HTTP 303 to <https://accounts.google.com/o/oauth2/auth> which (after additional redirects) send CSP header with `report-uri /v3/signin/_/AccountsSignInUi/cspreport` and the browser proceeded to submit CSP report about Google's web page to `https://ourdomain.example.com/v3/signin/_/AccountsSignInUi/cspreport` instead of `https://accounts.google.com/v3/signin/_/AccountsSignInUi/cspreport` as expected.

I would parse that UA string as Chrome version 125 so this might be a regression. Even though Chrome version 125 is already old, it was released in May 2024 which should be later than the fixes mentioned in this bug.

I haven't seen this issue often so I would guess the regression is limited to some edge case (e.g. poor internet connection or some kind of race).

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094052)*
