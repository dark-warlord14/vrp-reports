# Security: bypass CSP navigate-to feature with serviceWorker navigate function

| Field | Value |
|-------|-------|
| **Issue ID** | [40059525](https://issues.chromium.org/issues/40059525) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2022-04-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

bypass CSP navigate-to feature with serviceWorker navigate function

**VERSION**  

Chrome Version: Version 103.0.5033.0 (Developer Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**  

Add --enable-experimental-web-platform-features in the command or enable #enable-experimental-web-platform-features flags  

Add header("Content-Security-Policy", "navigate-to 'self'") in the response header

Visit <https://test.com/index.html>, it will navigate to <https://www.google.com> .

## Attachments

- [index.html](attachments/index.html) (text/plain, 134 B)
- [main.js](attachments/main.js) (text/plain, 220 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 515 B)

## Timeline

### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-30)

+CSP folks - assigning Impact=None as I assume navigate-to has not yet launched.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### an...@chromium.org (2022-05-02)

Indeed, navigate-to has not launched yet.

This might also require some clarification. According to the spec, the source browsing context of the navigation initiated by the service worker is the browsing context being navigated. So we would check the 'navigate-to' directive of the browsing context being navigated. On the other hand, it might have made sense to actually check the 'navigate-to' directive of the service worker itself?

In chrome, for reference, a service worker calling `navigate()` creates a navigation without initiator (https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_client_utils.cc;l=527;drc=6c807e33d27f2db0fd2cbe3ba78ef93e6c289eae), which is why we don't check any policies.



### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### is...@google.com (2023-02-16)

This issue was migrated from crbug.com/chromium/1321157?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ar...@chromium.org (2024-09-12)

Fixed by killing it:
<https://chromium-review.googlesource.com/c/chromium/src/+/5850982>

Note for VRP: `Impact=None`, as the feature was never launched.

### sp...@google.com (2024-09-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-18)

Congratulations asnine! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-12-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### me...@eligrey.com (2025-09-02)

I suspect that this method can bypass the Navigation API, given that the 'fix' was just removing navigate-to...

## Bounty Award

> report of lower impact web platform privilege escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059525)*
