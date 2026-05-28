# Security: Extensions are able to inject resources into Chrome URLs.

| Field | Value |
|-------|-------|
| **Issue ID** | [40948126](https://issues.chromium.org/issues/40948126) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Reporter** | fa...@gmail.com |
| **Assignee** | am...@chromium.org |
| **Created** | 2023-12-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Using declarativeNetRequest, an extension is able to redirect resources (images, scripts, or iframes) of Chrome URIs to any desired resource if they are loaded over the network. This could affect any part of the list of all Chrome URLs which use external resources via HTTPS or HTTP. For example, the proof-of-concept below showcases how a malicious Chrome extension could change the iframe content of the chrome://whats-new page to an attacker-controlled webpage.

**VERSION**  

Chrome Version: 121.0.6161.0 (Official Build) canary (64-bit) (cohort: Clang-64)

**REPRODUCTION CASE**

1. Download the attached files folder.
2. Load the same folder as an extension for testing.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [background.js](attachments/background.js) (text/plain, 49 B)
- [manifest.json](attachments/manifest.json) (text/plain, 570 B)
- [rules.json](attachments/rules.json) (text/plain, 218 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 550.6 KB)
- [sadscreenshot.png](attachments/sadscreenshot.png) (image/png, 77.1 KB)

## Timeline

### [Deleted User] (2023-12-02)

[Empty comment from Monorail migration]

### sr...@google.com (2023-12-04)

Hey there, thanks for the report.
I'm closing this as won't fix since this sounds working as intended to me. The extension is allowed to change the resources and I don't see any impact that escalates the privileges in this case.
For example, some chrome:// origins have access to special APIs, like chrome://downloads, but those shouldn't fetch external JS and run it with these permissions.
But please reopen if you find a way to make this escalate privileges, i.e. find a way that gives you more permissions than declarativeNetRequest.

### is...@google.com (2023-12-04)

This issue was migrated from crbug.com/chromium/1507431?no_tracker_redirect=1

### pe...@google.com (2024-03-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### fa...@gmail.com (2024-05-03)

deleted

### fa...@gmail.com (2024-05-03)

deleted

### fa...@gmail.com (2024-05-03)

FYI, I found out that changing the rules to redirect images could change images to attacker images under chrome://whatsnew. I guess there's no impact from this.

### fa...@gmail.com (2024-05-07)

Similar issue: <https://issues.chromium.org/issues/40086590>

Upon retesting recently, it seems it is fixed even though this report is made obsolete. It seems external site is blocked by csp policy newly set. Additionally, Please check the similar bug added in this comment, which is very similar to this issue, where it also allowed embedding webpages into a Chrome URL from outside. However, the report required `--disable-web-security` to make it work, whereas mine only required the same action by a malicious extension. I have also left a few comments on my current issue stating that I am still able to embed external resources like images using the vulnerable API. Please consider reopening the issue, as I still believe the core issue—that the 'declarativeNetRequest API can change resources of a chrome:// URI page'—is not resolved.

### fa...@gmail.com (2024-06-18)

Hey, I reported this same issue way before, December 2023: <https://issues.chromium.org/issues/328690293>. How come my bug report got rejected and this one got rewarded (which was probably reported after my bug went public.)?

The only difference between this bug and mine is that it had the part:

```
Security Bug

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

```

Also, if you guys have time, could you check this issue as well: <https://issues.chromium.org/issues/40946335>?

### fa...@gmail.com (2024-06-18)

If you read both my report and the report at <https://issues.chromium.org/issues/328690293>, you can clearly see that I provided a full PoC (Working Extension) instead of requiring the user to go to the console log.

### fa...@gmail.com (2024-06-18)

deleted

### pe...@google.com (2024-06-19)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### am...@chromium.org (2024-06-19)

Hi Shaheen, apologies that this got closed as WAI while the other issue was resolved. I think the core issue in how you demonstrated this issue with an extension using declarative\_net\_request which appears to be WAI, as we also discussed over email, rather than reporting / focusing on the issue with CSP child-src directive being set to be "child-src chrome://webui-test https: google.com/chrome/whats-new/;" and allowing for any HTTPS page to be loaded in an iframe on chrome://whats-new/, which is the focus and key description of the other report.
I will go ahead and mark this as fixed and we'll review this in a future VRP panel to see if this should still be reward eligible.
Please understand there are many bugs in our queue at present and we are about to have a series of holidays in the US, so there will be some delays in VRP panel and reward decisions.

### am...@chromium.org (2024-06-19)

Another issue of note upon reviewing this report. Please do not comment on bugs closed as WontFix and expect a response. We have to close many issues, some as spam, as WontFix, so we do not monitor those reports. The best things to do in these cases is to open a new bug report with more information or to reach out to [security-vrp@chromium.org](mailto:security-vrp@chromium.org).

### sh...@gmail.com (2024-06-19)

deleted

### fa...@gmail.com (2024-06-19)

I had reported this issue at the moment I discovered that a Chrome URL can embed any external URL using declarative API, which you could understand as a CSP issue. I didn't call it a CSP issue because there was no particular iframe policy in place, and it was the developer's duty to add one (Also, regarding CSP, I tried to bypass the actual CSP inplace for an XSS, but it was not possible. So, this was my report). So, I just described the issue in my own words and provided a working proof of concept using a simple extension to demonstrate it.

In this issue the user does not need to go to the vulnerable Chrome URL, open devtools, or type any code; this can be exploited with the installed extension.

### fa...@gmail.com (2024-06-19)

[comment #15](https://issues.chromium.org/issues/40948126#comment15) Noted. Thank you, Amy, for considering this issue

### fa...@gmail.com (2024-06-19)

I referenced a bug in the comment I made here ([comment #9](https://issues.chromium.org/issues/40948126#comment9)). I think the awarded report used the same reproduction steps as the referenced bug (without the --disable-web-security part).

Even though my bug is public, I only feel good about the awarded bug <https://issues.chromium.org/issues/328690293>. Kudos to him for bringing up the issue again.

But I feel bad that I missed a CVE, and even though I tried, I couldn't bring attention to this issue after the "WAI".

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for the initial report of the CSP issues in the chrome://whats-new/ page that was highlighted and resolved in crbug.com/328690293


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Thanks for your efforts Shaheen! 

### fa...@gmail.com (2024-06-28)

I hoped I was getting the same 1k reward as the duplicate report, but nevertheless, thank you for the bounty. I guess the rationale for receiving half the bounty is that my report is less detailed. I thought I covered more by providing a working PoC and demo.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40948126)*
