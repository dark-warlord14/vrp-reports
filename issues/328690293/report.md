# chrome://whats-new/ CSP allows loading any HTTPS page

| Field | Value |
|-------|-------|
| **Issue ID** | [328690293](https://issues.chromium.org/issues/328690293) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>UserEducation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | rb...@chromium.org |
| **Created** | 2024-03-08 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
In https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/whats_new/whats_new_ui.cc;l=47-51?q=kOpenAISettings&ss=chromium, the Content Security Policy child-src directive is set to be "child-src chrome://webui-test https: google.com/chrome/whats-new/;". The comment above indicates the intent might have been to allow google.com/chrome/whats-new/ over HTTPS to load in an iframe on chrome://whats-new/, but in reality this CSP allows any HTTPS page to load in an iframe on chrome://whats-new/.

This means for instance if an attacker has an XSS or is able to insert a link on google.com/chrome/whats-new/ to their site, their site would load inside chrome://whats-new/. Since chrome://whats-new/ is what is shown in the URL bar, the attacker can abuse this for phishing.

Perhaps this was intentional but I'm not sure why this page needs to allow loading any HTTPS page. The guidelines in https://chromium.googlesource.com/chromium/src/+/main/docs/webui_explainer.md#Security-considerations state: "WebUIs have a default Content Security Policy which disallows embedding any frames. If you want to include any web content in an you will need to update the policy for your WebUI. When doing so, allow only known origins and avoid making the policy more permissive than strictly necessary."

VERSION
Chrome Version: Version 122.0.6261.112 (Official Build) (arm64) stable
Operating System: Macos 14.4 (23E214)

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

Here are steps to checking that this CSP indeed allows loading an arbitrary HTTPS site
1. Open chrome://whats-new/ in Chrome.
2. Open the devtools console and execute the following:
```
const i = document.createElement('iframe')
i.src = 'https://example.com'
document.body.appendChild(i)
```
Note the iframe is loaded without any CSP errors. Screenshot attached.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Yan Zhu 

## Attachments

- [Screenshot 2024-03-08 at 09.13.50.png](attachments/Screenshot 2024-03-08 at 09.13.50.png) (image/png, 379.3 KB)

## Timeline

### ma...@chromium.org (2024-03-09)

I reproduced this using the provided instructions on macOS with Chrome 124.0.6329.0. It seems unexpected that chrome://whats-new/'s CSP policy permits external web content to be loaded.

Rebekah, you're an owner and recent reviewer of changes within whats\_new\_ui.cc. Please feel free to re-assign if someone is better suited to look into this.

### rb...@chromium.org (2024-03-09)

candidate fix at https://chromium-review.googlesource.com/c/chromium/src/+/5357281

### ap...@google.com (2024-03-11)

Project: chromium/src
Branch: main

commit 3bd9d470059a4b3463a741001183c9499f347e1e
Author: rbpotter <rbpotter@chromium.org>
Date:   Mon Mar 11 17:24:43 2024

    What's New: Update CSP to accurately limit https sources
    
    Fixed: 328690293
    Change-Id: Id7dd4a836d90b457b3f6071da18ed0110a0214e3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5357281
    Commit-Queue: Rebekah Potter <rbpotter@chromium.org>
    Reviewed-by: Mickey Burks <mickeyburks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1271036}

M       chrome/browser/ui/webui/whats_new/whats_new_ui.cc

https://chromium-review.googlesource.com/5357281


### am...@google.com (2024-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-22)

Congratulations, Yan Zhu! The Chrome VRP Panel has decided to award you $1,000 for this exploit mitigation bypass. A member of the Google p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your effort in discovering and reporting this issue to us!

### pe...@google.com (2024-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/328690293)*
