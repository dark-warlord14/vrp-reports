# Security: Content-Security-Policy bypass via Console API CSS-formatted messages

| Field | Value |
|-------|-------|
| **Issue ID** | [40056332](https://issues.chromium.org/issues/40056332) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Platform>DevTools |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **CVE IDs** | CVE-2016-5157, CVE-2019-1986, CVE-2019-1987, CVE-2019-1988 |
| **Reporter** | gs...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-06-24 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Developer Tools use a separate context and do not use the corresponding web page's Content-Security-Policy.

If a web page uses the Console API to log user-controlled content, CSS styles can inject remote resources.

console.log() supports CSS formatting if the first argument is a string containing `%c`. A subsequent argument is then interpreted as CSS inline styles. `%c` can occur multiple times to abuse a subsequent argument as CSS inline styles.

A malicious user persists data that is rendered on a web page using console.log(), .trace() etc., e.g. a social network, such that the data is rendered with CSS containing a remote resource.  

They get a victim to open that web page and to open the Developer Tools console ("press F12").  

The remote resource's server gets the victim's browser request data including IP address, user agent etc.

Expected: Developer Tools must either respect Content-Security-Policy or not load remote resources at all.

**VERSION**  

Chrome Version: [91.0.4472.114] + [stable]  

Operating System: macOS 11.4 (20F71)

**REPRODUCTION CASE**

1. deploy attached PHP script on a PHP web server – PoC uses PHP only to send CSP header
2. open the web page served by that PHP file
3. open Developer Tools console – it shows a remotely loaded GIF in the console, regardless of the Content-Security-Policy of the web page

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

- no crash -

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Hoang Nguyen

## Attachments

- [csp-console-api-bypass.php](attachments/csp-console-api-bypass.php) (text/plain, 2.0 KB)

## Timeline

### [Deleted User] (2021-06-24)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-06-25)

Can you be much more specific about how the attack is mounted and what security boundary this violates?

This seems innocuous and intended to me, a Content security policy is meant to prevent XSS exploitation. Is your concern that a console.log() will use attacker-controlled strings (e.g. from the URL parameters) and then this results in arbitrary CSS running in the DevTools context?

[Monorail components: Platform>DevTools]

### gs...@gmail.com (2021-06-26)

When I set a Content-Security-Policy that disallows access to external domains, I expect my users to be protected from tracking and potential exploits of e.g. in image rendering not coming from my website but which managed to be mounted through my website.

console.log() etc. allow attackers to circumvent this policy and use my website to track or obtain the users' browser and connection information.

To a website operator, a console.log() is also not expected to introduce a security or privacy vulnerability just by logging user-provided input.

The attacker just needs to be able to inject a `%c` to enable CSS formatting with a subsequent string parameter that contains CSS with an external resource and is not constrained by Content-Security-Policy.

Given that the attacker can already inject this, it is likely that the displayed content on the web page is also controlled by the attacker, so they could just social-engineer the user to press F12 to open the Developer Tools to complete the attack.

Tracking can be used to detect when someone opens a web page and to determine their browser.
This could then be used to directly attack the victim. There have been exploits based on image rendering, e.g. CVE-2016-5157, CVE-2019-1986, CVE-2019-1987, CVE-2019-1988.

CSP is not restricted to XSS mitigation but also should prevent access to external resources in general, including images used for tracking via default-src and img-src.

### [Deleted User] (2021-06-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@chromium.org (2021-06-28)

CSP is only a mitigation for data exfiltration, but it is on the implicit roadmap to tighten it as a mitigation. We've previously WontFixed things like things but they are now somewhat in scope.

I guess the question is what would we do about this. We'd either have to remove the %c (unlikely). Or mark console.log() as some sort of Trusted Types sink, which is only DOM focus and data exfiltration is an explicit non-goal.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### mp...@chromium.org (2021-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

[Empty comment from Monorail migration]

### gs...@gmail.com (2021-06-29)

Firefox seems to block all external resources requested by the Console API CSS, so that would also be a way to mitigate, as an alternative to applying CSP to such requests as well.

Both would be breaking changes to current behavior but with probably minor impact as the Console API is primarily used for debugging and development.

A non-breaking change could be to use a Permissions-Policy header to control behavior but not worth it in my opinion because most people using console.log() etc. wouldn't be aware of this issue anyway, so would rarely use Permissions-Policy to mitigate, and those knowing about the privacy / security issue would refrain from using console.log() etc. or avoid injecting user-controlled strings in the first parameter.

### mk...@google.com (2021-06-29)

For my own clarity, I think this is the risk that's being described: an attacker with the capability of injecting text into a call to `console.log()` _and_ into subsequent arguments to `console.log()`, and the capability to control users' environment enough to cause them to open devtools can cause requests to be made, even given a restrictive CSP that would otherwise prevent such requests (something like `console.log("<?php echo $_GET['param']; ?>")` with a filtering function that somehow prevented more interesting injections than `%c", "background:url([secret data goes here])`?). This feels very low risk, given those constraints.

Still, it doesn't sound unreasonable to me to harden the console to prevent external requests entirely, but I'm not terribly familiar with `%c`'s usage in the wild (nor the set of CSS rules that might end up causing requests that developers might care about). That said, if we want to make devtools adhere to the same boundaries as the page sending it data, then there are likely a few other places we'd need to look. Source maps come to mind, both for script and style resources, and there are likely other fetching mechanisms we'd need to enumerate. +sigurds@ for insight from devtools.

That said, I don't think we've traditionally considered devtools to be an attack surface CSP can defend from. I'm not sure this is a good place to start. Again, I'd ask Sigurd to weigh in from that team's perspective.

### si...@chromium.org (2021-06-29)

We generally try to limit the requests that DevTools does to what the page itself could do, but we probably haven't considered CSP to the appropriate extent. For example, for source maps fetches we don't apply the page's CSP (and currently, we don't plan to, either). See https://csp-sourcemap.glitch.me/ for an example where a source map is fetched cross-origin.

That said, the ability to exfiltrate data this way seems somewhat serious to me and should probably be reigned in; in some sense it is a CSP-bypass that additionally needs the user to open DevTools.

For source maps, a similar possibility to exfiltrate data exists by if the attacker has the ability to injecting a script with a prepared source map URL that contains the data to exfiltrate. This, however, seems more difficult than merely issuing a console.log. DevTools will then send a request to that URL to fetch the source map when DevTools is opened.

The problem I see with just restricting %c and the like is that there might be legitimate use-cases out there, which we'd break. In the discussions around source maps, we encountered similar problems, where just restricting the loading mechanism would break existing use-cases. Maybe we should by-default only load resources from the current origin, but allow the DevTools user to override this restriction?

### [Deleted User] (2021-06-29)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gs...@gmail.com (2021-06-30)

I think an override in DevTools would be ok, as long as it is clear to an average user which security or privacy implications overriding the default has.

The exfiltration scenario and exploiting vulnerabilities in the rendering of external resources can be serious but are not trivial. Exfiltrating data (other than e.g. request data such as IP address, User-Agent, Referer) would require the ability to run code or have relevant data in the parameters where the CSS would be defined.

The primary attack is probably tracking someone.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### si...@chromium.org (2021-09-07)

Mathias, PTAL

### ja...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/73229f75565e9d9630f2e9f23b8e09290098ca87

commit 73229f75565e9d9630f2e9f23b8e09290098ca87
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Sun Mar 13 18:45:55 2022

E2E tests for console log formatters

Bug: chromium:1223475
Change-Id: I413b7d0f85dd69b2e94d72564506dac3727c9f21
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3516094
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>

[modify] https://crrev.com/73229f75565e9d9630f2e9f23b8e09290098ca87/test/e2e/console/console-log_test.ts


### gi...@appspot.gserviceaccount.com (2022-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3451e19bb3b05f269df717fd8ddb7bd2cb6d7a65

commit 3451e19bb3b05f269df717fd8ddb7bd2cb6d7a65
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Mar 14 10:36:26 2022

Roll DevTools Frontend from 3d369648ae95 to babb2204cf9c (2 revisions)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/3d369648ae95..babb2204cf9c

2022-03-14 wolfi@chromium.org Add round icon button
2022-03-14 jarin@chromium.org E2E tests for console log formatters

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1223475,chromium:1297532
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I7d7e8491e9367a69b88f7925e9773e77a31cadbe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3521126
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#980489}

[modify] https://crrev.com/3451e19bb3b05f269df717fd8ddb7bd2cb6d7a65/DEPS


### gi...@appspot.gserviceaccount.com (2022-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/48195593291718160b196157c24a0147cb006773

commit 48195593291718160b196157c24a0147cb006773
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Mon Mar 14 14:58:06 2022

Block urls in console.log %c formatter styles

We block some URL schemes (such as http or file) from style values in
the %c formatter for console.log. This is to prevent the requests from
bypassing security policies and leaking data.

Bug: chromium:1223475
Change-Id: I779cb95f523fcfbc84ce5edf1320d1ffde4d94fb
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3522264
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>

[modify] https://crrev.com/48195593291718160b196157c24a0147cb006773/test/unittests/front_end/panels/console/ConsoleFormat_test.ts
[modify] https://crrev.com/48195593291718160b196157c24a0147cb006773/front_end/panels/console/ConsoleViewMessage.ts
[modify] https://crrev.com/48195593291718160b196157c24a0147cb006773/front_end/panels/console/ConsoleFormat.ts
[modify] https://crrev.com/48195593291718160b196157c24a0147cb006773/test/e2e/console/console-log_test.ts


### gi...@appspot.gserviceaccount.com (2022-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/744d731b898cd068dd1b573194d6550ab5a11fad

commit 744d731b898cd068dd1b573194d6550ab5a11fad
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Mar 15 11:54:23 2022

Roll DevTools Frontend from 1a45cd5a5488 to 481955932917 (1 revision)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/1a45cd5a5488..481955932917

2022-03-15 jarin@chromium.org Block urls in console.log %c formatter styles

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1223475
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I88877920599087698ee81779825170d94325bd0a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3524507
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#981060}

[modify] https://crrev.com/744d731b898cd068dd1b573194d6550ab5a11fad/DEPS


### ja...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Thank you Hoang for this report! The VRP Panel would like to award you a $500 thank you reward for this issue. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and we appreciate you reporting this issue to us. 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-02)

This issue was migrated from crbug.com/chromium/1223475?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Platform>DevTools]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056332)*
