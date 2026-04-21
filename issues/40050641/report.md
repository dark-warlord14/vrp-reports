# Security: SameSite=Lax cookie sent with cross-origin request inside iframe

| Field | Value |
|-------|-------|
| **Issue ID** | [40050641](https://issues.chromium.org/issues/40050641) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | ch...@chromium.org |
| **Created** | 2019-11-08 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

If a site on origin A contains an iframe containing a site on origin B, and you click a link on site B which navigates to site A inside the iframe, SameSite=Lax cookies for origin A will be sent with the request even though it is cross-origin (B to A).

**VERSION**  

Chrome Version: 78.0.3904.70 + stable  

Operating System: macOS High Sierra 10.13.6 (17G9016)

**REPRODUCTION CASE**  

Attached is a nodejs script for reproducing this issue. Run the script with 'node <script name>' and visit localhost:4000 in chrome to view the page. Loading this page sets a SameSite=Lax cookie, and loads an iframe with 127.0.0.1:4000, a different origin. Click the link in the iframe to initiate a cross-origin request back to localhost:4000, which sends the cookie.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Sean Lafferty, Andre Marianiello

## Attachments

- [samesite-leak.js](attachments/samesite-leak.js) (text/plain, 939 B)

## Timeline

### me...@chromium.org (2019-11-11)

Thanks, I was able to reproduce this.

But I think this behavior works as intended.

From the RFC on first-party cookies (https://tools.ietf.org/html/draft-west-first-party-cookies-07#section-4.1.1):
"
 developers may set the "SameSite" attribute in a "Lax" enforcement mode that carves out an exception which sends same-site
   cookies along with cross-site requests if and only if they are top-
   level navigations which use a "safe" (in the [RFC7231] sense) HTTP
   method.
"
Since this is a get request caused by clicking a link I think this qualifies as a "safe" and "top level navigation" where a Lax cookie should be sent.

mkwst@, ryansturm@ or chlily@ What do you think? Should this be closed as WontFix?

[Monorail components: Blink>SecurityFeature Internals>Network>Cookies]

### ch...@chromium.org (2019-11-11)

+morlovich@

So this would not be a top-level navigation (since it's inside an iframe).

This is essentially this testcase: https://cs.chromium.org/chromium/src/content/browser/frame_host/render_frame_host_impl_browsertest.cc?q=render_frame_host_impl_browsertest.cc&ss=chromium&l=2822-2827

I think this is WAI, though maybe there's an argument to be made for a spec change.

Mike, wdyt?

### [Deleted User] (2019-11-11)

Some additional context for interested parties:

We came across this behavior when we noticed that an iframe Oauth login workflow worked in Chrome but not in Firefox. We noticed that Firefox was not sending the oauth_state (lax) cookie, which seemed to be intentional behavior based on the discussion on https://bugzilla.mozilla.org/show_bug.cgi?id=1454027 . We didn't know if this was intentional behavior in Chrome or not, but we thought we would file this, just to be safe.

### sh...@chromium.org (2019-11-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2019-11-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

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

### ch...@chromium.org (2021-07-29)

Apologies for the delay, coming back to this after a long time...

I'm really sorry, I think I may have misunderstood the original report. I don't remember what I thought the description was saying before, but I believe now that this is the scenario described in https://crbug.com/1166211, which should be fixed by https://crrev.com/c/2653663.

### [Deleted User] (2021-07-29)

No worries, happy it got fixed!

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

The VRP Panel has decided to award you $1,000 for this report! A member of our finance team will be in touch shortly to arrange payment. Thank you for reporting this issue! 

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-19)

I have been notified that my enrollment in the payment system is complete, but did not receive any additional instructions. What are next steps?

### am...@chromium.org (2021-08-19)

Hi, no other instructions for you. Once enrollment in the payment system is complete, finance is notified that they can process payment and have it sent to the account you specified in enrollment. You'll be able to see that transaction in the payment system as it is completed. 

### [Deleted User] (2021-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

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

This issue was migrated from crbug.com/chromium/1022790?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Internals>Network>Cookies]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050641)*
