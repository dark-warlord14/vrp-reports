# Clickjacking Exploit Leading to Unintentional Credit Card Submission in Chrome iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [392443457](https://issues.chromium.org/issues/392443457) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill>Payments |
| **Platforms** | Android, iOS |
| **Chrome Version** | 127.0.6533.103 |
| **CVE IDs** | CVE-2024-11111 |
| **Reporter** | ia...@gmail.com |
| **Assignee** | vi...@google.com |
| **Created** | 2025-01-26 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Autofill Bypass of CVE-2024-11111 ([issue 360520331](https://issues.chromium.org/issues/360520331)): Clickjacking Exploit Enabling Unintentional Credit Card Submission in Chrome Android

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

A bypass of the mitigations introduced in CVE-2024-11111 has been identified in Chrome Android. The exploit leverages autocomplete attributes (cc-csc, cc-number, cc-exp) in credit card input fields to enable unauthorized submission of sensitive data using the browser's autofill feature. This bypass allows attackers to trick users into unknowingly submitting credit card information to an attacker-controlled server via automated form submission triggered by autofill events.

The vulnerability lies in the improper handling of credit card input fields with autocomplete attributes. The inclusion of autocomplete="cc-csc", autocomplete="cc-number", and autocomplete="cc-exp" bypasses the restrictions previously implemented to mitigate CVE-2024-11111. These attributes enable browsers to autofill credit card fields based on saved payment methods, treating autofill as a valid user interaction.

This behavior allows attackers to exploit the browser's trust in autofill events to trigger programmatic form submission without explicit user intent. Using JavaScript, the form is submitted automatically as soon as the fields are populated via autofill, exfiltrating sensitive credit card details (e.g., card number, CVV, expiry date) to an attacker-controlled endpoint.

Tested on android chrome version 132.0.6834.122

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

1. please make sure that you have a Credit Card already set on Chrome > Settings > Payment Method
2. Host attached test.html on your domain or you can also use 12x.site/test.html as proof of concept to reproduce this vulnerability.
3. Continue click on Submit button and your card data will get posted to cross-origin website.

Impact
This bypass reintroduces the clickjacking vulnerability mitigated in CVE-2024-11111, allowing attackers to:

1. Exfiltrate Sensitive Data: Steal credit card information (number, expiry date, CVV) without the user’s consent.
2. Exploit Autofill Mechanisms: Abuse the browser's autofill functionality to perform automated submissions.
3. Conduct Phishing or Clickjacking Attacks: Trick users into visiting malicious pages that exfiltrate their sensitive information.

---

### The cause

#### What version of Chrome have you found the security issue in?

android chrome version 132.0.6834.122

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Clickjacking

#### How would you like to be publicly acknowledged for your report?

Armaan Pathan

## Attachments

- [test.html](attachments/test.html) (text/html, 2.3 KB)
- [video.mp4](attachments/video.mp4) (video/mp4, 16.9 MB)
- [test.html](attachments/test.html) (text/html, 2.3 KB)
- [Screen Recording 2025-02-22 at 7.53.16 PM.mov](attachments/Screen Recording 2025-02-22 at 7.53.16 PM.mov) (video/quicktime, 35.0 MB)
- [Screen Recording 2025-02-22 at 7.58.22 PM.mov](attachments/Screen Recording 2025-02-22 at 7.58.22 PM.mov) (video/quicktime, 18.3 MB)

## Timeline

### aj...@google.com (2025-01-27)

I'm not able to repro this but sending to the team for a look.

### pe...@google.com (2025-01-28)

Setting milestone because of s2 severity.

### pe...@google.com (2025-01-28)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ph...@google.com (2025-02-17)

smcgruer: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ar...@gmail.com (2025-02-17)

Hi team,
Any updates on this?

### sm...@chromium.org (2025-02-18)

Apologies for the delay. It's unclear to me from the reproduction video what the clickjacking attack is. From what I can see:

1. 0:22 the site is loaded. The submit button is initially at the bottom of the page (this doesn't happen for me when loading 12x.site/test.html on my phone)
2. 0:24 the submit button jumps to the middle of the page
3. 0:25 the submit button is *presumably* tapped, but there's no visual indicator of this in the video (I assume 'record user input' was not enabled on the recording app).
4. 0:26 the autofill prompt shows up, however only the very top of the dialog is anywhere near the submit button, and certainly not a card.
5. 0:27 the dialog dismisses and the page claims it was submitted but doesn't show any of the supposedly exfiltrated data.

It is true that in step #4 someone could have positioned the submit button to be actually under where the bottomsheet shows up, to get the user to click on the bottomsheet accidentally. In that case however, the [standard input protection](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/autofill/android/internal/java/src/org/chromium/chrome/browser/touch_to_fill/payments/TouchToFillPaymentMethodMediator.java;l=277;drc=798b98d70313e6a55bcf9cc85bc7ca7d42ca6d23) - a 500ms delay in accepting user input - should apply, and so the dialog is protected to the level that Chrome has presumably blessed as 'good enough' against clickjacking.

---

Reporter, could you please explain more clearly what the actual clickjacking attack is here, and post a video that shows user input?

### ph...@google.com (2025-02-20)

smcgruer: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-02-21)

smcgruer: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-02-21)

smcgruer: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sm...@chromium.org (2025-02-21)

Not sure why the spam from 'not updated', this was updated on Feb 18th and is Needs-Feedback.

### ar...@gmail.com (2025-02-22)

Hi there,
The design of the web page requires the user to click multiple times to activate the credit card input fields. This behavior can be exploited by an attacker to trick the user into repeatedly clicking, potentially leading them to unknowingly submit saved credit card form data. This could be leveraged to automatically submit sensitive information without the user's explicit intent, posing a risk of unauthorized data submission

this is a bypass of CVE-2024-11111, As requested I am uploading 2 different videos, one with opacity=0 and another normal video

### pe...@google.com (2025-02-22)

Thank you for providing more feedback. Adding the requester to the CC list.

### sm...@google.com (2025-02-24)

Thank you for the videos. From those, particularly `Screen Recording 2025-02-22 at 7.53.16 PM.mov` , to me it is clear that this is not a clickjacking attack (the user has to visibly see the browser UI offering autofill, and elect to click on it themselves - that is, the browser UI *is* their intended click target and thus its not clickjacking).

It looks like what you're trying to report is that one can have effectively hidden fields which can trigger autofill, and that *in theory* a user might then be confused and agree to the Autofill UX even though there aren't form fields visible, and thus give up their personal information to the site. This is a known and accepted vulnerability in Autofill (it's essentially impossible to 100% detect 'hidden' fields as CSS/JS offers far too many ways to make things effectively-hidden-but-still-there), and I'm afraid is not a new issue.

This is not a bypass of [issue 360520331](https://issues.chromium.org/issues/360520331).

### ch...@google.com (2025-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/392443457)*
