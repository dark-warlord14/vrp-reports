# Payment Request API permitted in CSP/iframe sandbox

| Field | Value |
|-------|-------|
| **Issue ID** | [40090857](https://issues.chromium.org/issues/40090857) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>FeaturePolicy, Blink>Payments, Blink>SecurityFeature>ContentSecurityPolicy, Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | am...@chromium.org |
| **Created** | 2018-03-20 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/sandboxed_PR.php

What is the expected behavior?
Payment Request fails.

What went wrong?
I think payment request API shouldn't be allowed in CSP/iframe sandbox.

Did this work before? N/A 

Chrome version: 65.0.3325.162  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [Screen Shot 2019-08-21 at 3.11.53 PM.png](attachments/Screen Shot 2019-08-21 at 3.11.53 PM.png) (image/png, 254.3 KB)
- [Screen Shot 2019-08-21 at 3.12.10 PM.png](attachments/Screen Shot 2019-08-21 at 3.12.10 PM.png) (image/png, 255.5 KB)
- [Screen Shot 2019-08-21 at 3.14.23 PM.png](attachments/Screen Shot 2019-08-21 at 3.14.23 PM.png) (image/png, 38.9 KB)
- [Spider_Man_meme.jpeg](attachments/Spider_Man_meme.jpeg) (image/jpeg, 94.6 KB)

## Timeline

### el...@chromium.org (2018-03-20)

Similar to the question of whether the password manager should autofill in sandboxed content; that variant is https://crbug.com/chromium/821636.

[Monorail components: Blink>Payments Blink>SecurityFeature>IFrameSandbox]

### mk...@chromium.org (2018-03-22)

+battre@, as we should probably make the same decision in both places.

### mk...@chromium.org (2018-03-27)

Handing this to zkoch@ for triage.

### zk...@chromium.org (2018-03-27)

I actually don't know enough about CSP to understand if this is correct or not. Mike, can you share some of the ways you think about CSP or any guidelines so we can make a judgement call?

### ro...@chromium.org (2018-03-27)

I don't see any iframes on https://test.shhnjk.com/sandboxed_PR.php. What am I missing?

### s....@gmail.com (2018-03-27)

In the PoC page, sandbox is applied via following CSP header.

"Content-Security-Policy: sandbox allow-scripts"

### ro...@chromium.org (2018-03-27)

Should this be in the W3C spec?

### s....@gmail.com (2018-03-28)

If the decision is to disable Payment Request API inside sandbox, then adding that to spec would be appreciated for the interop.

Though that's my personal opinion and the Question seems to be seeking the answer from Chromium folks?

### ro...@chromium.org (2018-03-28)

shhnjk@: Could you bring this up on https://github.com/w3c/payment-request/issues please?

### s....@gmail.com (2018-03-28)

Done: https://github.com/w3c/payment-request/issues/698

### ro...@chromium.org (2018-03-28)

Thank you!

### mm...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-08-21)

assigning to rouslan as zkoch is gone. Also, looks like this might have been fixed in https://github.com/w3c/payment-request/pull/822 - can this be closed?

### ro...@chromium.org (2019-08-21)

s.h.h.n.j.k@ - can you confirm whether this is still a problem and update steps to reproduce, please?

### s....@gmail.com (2019-08-21)

I still payment request prompt when I visit PoC in Chrome stable. So not fixed yet.

### ro...@chromium.org (2019-08-21)

s.h.h.n.j.k@ - is the PoC still valid? I don't see `Content-Security-Policy` headers. Should I be looking for something else?

### ro...@chromium.org (2019-08-21)

Was looking in the wrong spot, sorry.

### ro...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### ro...@chromium.org (2019-08-21)

wfh@ - Web Payment APIs are using feature policy. Is feature policy related to content security policy?

[Monorail components: Blink>FeaturePolicy]

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

### ro...@chromium.org (2020-10-22)

Let's pick this up in the next ZBB.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-18)

This issue has been Available for over a year. If it's no longer important or seems unlikely to be fixed, please consider closing it out. If it is important, please re-triage the issue.

Sorry for the inconvenience if the bug really should have been left as Available.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2022-03-25)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### ar...@chromium.org (2023-03-23)

+jkokatsu: Do you consider this bug fixed by:
https://github.com/w3c/payment-request/issues/698

We are now requiring:
f.allow = 'payment'

Do we consider this to be a sufficient mitigation? This should protect most sandboxed iframe.


I am asking because https://crbug.com/chromium/1407051.

### jk...@google.com (2023-03-23)

I think that should be good enough mitigation for this bug.

### s....@gmail.com (2023-03-23)

Agreed!

### jk...@google.com (2023-03-23)

[Empty comment from Monorail migration]

### is...@google.com (2023-03-23)

This issue was migrated from crbug.com/chromium/823737?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>FeaturePolicy, Blink>Payments, Blink>SecurityFeature>ContentSecurityPolicy, Blink>SecurityFeature>IFrameSandbox]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-05-15)

Going to consider this issue fixed per c#47 & c#48
thanks for the laugh from the spiderman meme moment above

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
low impact exploit mitigation bypass 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

One from the low severity bug archives! Thanks for your efforts in 2018 and 2023 confirming this was resolved. Sorry we didn't get this buttoned up until now! 

### s....@gmail.com (2024-06-28)

Thanks! Is there a way to receive bounty through Bugcrowd?

### am...@chromium.org (2024-06-28)

Not for this payment, sorry! You have to have a bugcrowd profile set up and associated in your bughunters profile and swap your payment option from `legacy` to `bugcrowd` before this reward went through SPUR. 
So unfortunately not for this payment, but if you go and set up all those things now, it will be set up in time for your next one. I'm positive there's still some of your bugs in our backlog. 😬

### s....@gmail.com (2024-06-28)

Got it, thanks!

### pe...@google.com (2024-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> low impact exploit mitigation bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090857)*
