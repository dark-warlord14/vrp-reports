# Security: Extension popup can render over permission prompts and screen share dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [361711121](https://issues.chromium.org/issues/361711121) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2024-08-23 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS
This vulnerability is almost the same as https://issues.chromium.org/issues/40058873 but it occurs on Payment request prompt


VERSION
Chrome Version 130.0.6670.0 (Official Build) canary (64-bit)
Operating System: Windows 10

REPRODUCTION CASE

1. Install attached extension: manifest-keyboard.json + bg-keyboard.js + popup.html. Rename the manifest file to manifest.json

2. Reload manifest-keyboard.json extension using chrome://extensions
Press Ctrl+A when requested by the attacker page.

3. Click the Web page then Press Ctrl+A when requested by the attacker page.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [bandicam 2024-08-24 00-49-56-017.mp4](attachments/bandicam 2024-08-24 00-49-56-017.mp4) (video/mp4, 2.7 MB)
- [extensionpopup.zip](attachments/extensionpopup.zip) (application/zip, 2.4 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### ar...@chromium.org (2024-08-26)

Thanks!

I can reproduce. See screenshot.

It seems we would like to display the extension popup under the Request payment prompt.

Since this is the almost the same as [bug 40058873](https://issues.chromium.org/issues/40058873), I am going to copy the **assignee** and **severity**. [kerenzhu@chromium.org](mailto:kerenzhu@chromium.org), could you please help triage this bug?

- **Os**: All except iOS and Android, where extensions aren't supported.
- **Found In**: The current extended stable version, assuming this was a problem for a long time.

### ke...@chromium.org (2024-08-27)

smcgruer@, do you happen to know which class shows the WebUI payment dialog?

### ke...@chromium.org (2024-08-27)

nvm, I figured out myself. The dialog is PaymentRequestDialogView.

### ap...@google.com (2024-08-27)

Project: chromium/src
Branch: main

commit e50b37d5ceb888e47e5ea63b401efb32d5468ece
Author: Keren Zhu <kerenzhu@chromium.org>
Date:   Tue Aug 27 17:52:43 2024

    Don't show extension popup when a payment dialog is visible
    
    We don't want extension popup to cover the payment dialog due to the
    risk of spoofing.
    
    Bug: 361711121
    Change-Id: I016234326b03e97093a05c0b060435d54497653c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5815888
    Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
    Reviewed-by: Stephen McGruer <smcgruer@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1347484}

M       chrome/browser/ui/views/payments/payment_request_dialog_view.cc
M       chrome/browser/ui/views/payments/secure_payment_confirmation_dialog_view.cc
M       chrome/browser/ui/views/payments/secure_payment_confirmation_no_creds_dialog_view.cc

https://chromium-review.googlesource.com/5815888


### sp...@google.com (2024-09-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$3,000 for report of lower impact security UI / web platform privilege escalation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-13)

Congratulations, Hafiizh! Thank you for your efforts and reporting this issue to us!

### sa...@gmail.com (2024-09-13)

thank you amy for the rewards

### pe...@google.com (2024-12-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361711121)*
