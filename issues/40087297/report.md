# Security: <link rel='prerender'> causes same-site cookies to be sent along with cross-site requests

| Field | Value |
|-------|-------|
| **Issue ID** | [40087297](https://issues.chromium.org/issues/40087297) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Internals>Preload |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ge...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2017-04-10 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

If an HTML-page contains a <link rel="prerender">-tag with the href pointing to a page on another domain than the domain hosting this HTML-page, then upon visiting this HTML-page the browser will send along all strict and lax same-site cookies with this cross-site request.

For example: An HTML-page residing on attacker.com contains the following tag <link rel="prerender" href="https://example.com">. Upon visiting this HTML-page the browser will send along all strict and lax same-site cookies of example.com in a cross-site request to example.com.

The internet-draft concerning same-site cookies (\*) states that:  

"If the "SameSite" attribute's value is "Strict", or if the value is  

invalid, the cookie will only be sent along with "same-site"  

requests. If the value is "Lax", the cookie will be sent with "same-  

site" requests, and with "cross-site" top-level navigations, as  

described in section 4.1.1."  

(\*) <https://tools.ietf.org/html/draft-west-first-party-cookies-07>

In this case, however, the strict same-site cookie is sent along with a cross-site request, while it should not be. Also, the lax same-site cookie is sent along with a cross-site request which does not cause a top-level navigation, while it should not be.

This makes websites vulnerable to attacks like CSRF, XSSI and cross-site timing attacks.

**VERSION**  

Chrome Version: [57.0.2987.98] stable  

Operating System: Ubuntu 16.04 (64-bit)

**REPRODUCTION CASE**  

See the attached HTML-file for a reproduction case. This reproduction case compares the cookies being sent along with a prerender request and an image request (both cross-site).

## Attachments

- [prerender.html](attachments/prerender.html) (text/plain, 2.5 KB)

## Timeline

### do...@chromium.org (2017-04-10)

+mkwst, do you mind triaging this please? Not sure of the specific level of vulnerability here - it potentially seems like a bug rather than a security issue since the cookies aren't being exposed to attacker.com - just to example.com when they shouldn't be.

[Monorail components: Blink>SecurityFeature]

### do...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### mk...@chromium.org (2017-04-19)

https://tools.ietf.org/html/draft-ietf-httpbis-cookie-same-site-00#section-4.1.1 calls out features like prerender as being more or less indistinguishable from a top-level navigation; `lax` cookies should be sent along with the request.

If we're sending `strict` cookies as well, though, that's certainly an issue. I'll take a look.

### sh...@chromium.org (2017-05-03)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2017-05-05)

Seems like low severity is probably more appropriate if I understand this correctly, but agreed that it's worth fixing. Feel free to flip it back if I missed something.

### sh...@chromium.org (2017-05-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### ge...@gmail.com (2018-08-13)

Also interesting: we found that cross-site requests initiated by Location header redirects (with various 30x status codes) include SameSite=strict cookies starting from Chrome 63.

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mp...@google.com (2018-09-10)

Re https://crbug.com/chromium/709946#c21, as I understand it, this is a bypass of SameSite=strict (treating it like SameSite=lax)? If so, can you file a new bug?

Also, ping on this original bug. Even though it's Low-Severity (debatably Medium-Severity, I don't know how many sites use SameSite as CSRF protection) it hopefully won't be a very complicated fix?

### mp...@google.com (2018-09-10)

Also, ping because this is a publicly known bypass published in https://www.usenix.org/conference/usenixsecurity18/presentation/franken.

### ge...@gmail.com (2018-09-13)

Yes, in this case SameSite=strict is indeed also treated like SameSite=lax. Thanks for your response, I have started a separate bug thread here:
https://bugs.chromium.org/p/chromium/issues/detail?id=883661

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### ge...@gmail.com (2019-02-06)

Friendly FYI: This bug also manifested in Brave Browser, due to their switch to the Chromium base. Because it still isn't fixed in Chromium (and because there doesn't seem to be any progress :-( ), I also reported it to them and got awarded a bug bounty.

### mm...@chromium.org (2019-02-06)

[Empty comment from Monorail migration]

[Monorail components: Internals>Preload]

### mk...@chromium.org (2019-02-12)

CCing some folks who might have bandwidth.

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### ev...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ge...@gmail.com (2020-11-19)

It seems that another report describing the exact same bug was awarded a bounty of $2000 (https://bugs.chromium.org/p/chromium/issues/detail?id=831725). This report was submitted one year after mine.

Why didn't I receive a bounty?

### mm...@chromium.org (2020-11-19)

That is an excellent question - believe this label will get it in the queue for reward consideration, and also marking it fixed, since I don't believe rewards are given until issues are addressed, and the bug you linked has been marked as fixed.

### ge...@gmail.com (2020-11-19)

Thank you!

### [Deleted User] (2020-11-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-30)

Re https://crbug.com/chromium/709946#c48, https://crbug.com/chromium/709946#c49 - just to confirm, the correct labels have been applied to this bug and so it will go before the VRP panel for consideration.

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

Thanks again for bringing this to our attention. The VRP panel agrees that you should indeed receive a $2000 reward. Someone from our finance team will be in touch.

We'll also edit the Chrome 77 release notes to say that you also reported this bug. How would you like to be credited?

### ge...@gmail.com (2020-12-03)

Thanks for the swift response!

You can credit me by my full name: Gertjan Franken.

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

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

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/709946?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Internals>Preload]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087297)*
