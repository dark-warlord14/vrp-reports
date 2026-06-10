# Security: Extension popup can render over permission prompts and screen share dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [359949844](https://issues.chromium.org/issues/359949844) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2024-08-15 |
| **Bounty** | $5,000.00 |

## Description


VULNERABILITY DETAILS
This vulnerability is almost the same as https://issues.chromium.org/issues/40058873 but it occurs on PWA prompt


VERSION
Chrome Version:  129.0.6657.0 (Official Build) canary (64-bit)
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

- [extension.zip](attachments/extension.zip) (application/zip, 2.3 KB)
- [bandicam 2024-08-15 11-37-54-824.mp4](attachments/bandicam 2024-08-15 11-37-54-824.mp4) (video/mp4, 2.0 MB)
- [bandicam 2024-08-15 11-37-54-824 (1).mp4](attachments/bandicam 2024-08-15 11-37-54-824 (1).mp4) (video/mp4, 2.0 MB)
- [extension.zip](attachments/extension.zip) (application/zip, 2.3 KB)

## Timeline

### ad...@google.com (2024-08-15)

Security shepherd here.

This does seem like a realistic spoofing scenario, along the lines of [issue 40058873](https://issues.chromium.org/issues/40058873), with the following mitigating factors:

- it has the precondition of the user having already installed an extension
- the PWA dialog is probably a little less sensitive than the permissions dialog. (It's difficult to think of abuse scenarios where this would offer an attacker any benefit)

So I'm opting for S3. I haven't attempted to reproduce this, but per <https://issues.chromium.org/issues/40058873#comment13> and the following few, this doesn't seem to be a new class of problems so I'm assuming it impacts the current extended stable branch. Assigning to kerenzhu@ for thoughts about how this should be fixed, plus cc devlin.

### pe...@google.com (2024-08-15)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2024-10-08)

hello any updates?

### ad...@google.com (2024-10-08)

This is an S3 bug and there is no SLO for fixing S3 bugs. Please do not post messages requesting updates -- we want to keep this space clear for discussion of how to actually fix the bug.

### ap...@google.com (2024-11-08)

Project: chromium/src  

Branch: main  

Author: Keren Zhu <[kerenzhu@chromium.org](mailto:kerenzhu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5995850>

Mark some dialogs as security-sensitive for extension

---


Expand for full commit details
```
Mark some dialogs as security-sensitive for extension 
 
This CL marks the FedCM account selection dialog and the PWAs 
installation dialog as security-sensitive for extensions. This 
effectively prevents the extension bubble from rendering above these 
dialogs, so that a malicious extension cannot trick users into 
interacting with them. 
 
Fixed: 376497151, 359949844 
Change-Id: I74448a677523da74d83d1c05d5d5da8e0ee3b29c 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5995850 
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
Commit-Queue: Keren Zhu <kerenzhu@chromium.org> 
Reviewed-by: Allen Bauer <kylixrd@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1380525}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/pwa_confirmation_bubble_view.cc`
- M `chrome/browser/ui/views/webid/account_selection_bubble_view.cc`
- M `chrome/browser/ui/views/webid/account_selection_modal_view.cc`

---

Hash: e0674d25b198c5240d276c9cb823bad1a67604d0  

Date:  Fri Nov 08 19:22:50 2024


---

### sp...@google.com (2024-11-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-22)

Congratulations Hafiizh! Thank you for your efforts and reporting this issue to us!

### sa...@gmail.com (2024-11-22)

Awesome Thank you amy

### ph...@google.com (2025-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2025-02-18)

VULNERABILITY DETAILS
This vulnerability is almost the same as <https://issues.chromium.org/issues/40058873> but it occurs on PWA prompt

VERSION
Chrome Version: 129.0.6657.0 (Official Build) canary (64-bit)
Operating System: Windows 10

REPRODUCTION CASE

1. Install attached extension: manifest-keyboard.json + bg-keyboard.js + popup.html. Rename the manifest file to manifest.json
2. Reload manifest-keyboard.json extension using chrome://extensions
   Press Ctrl+A when requested by the attacker page.
3. Click the Web page then Press Ctrl+A when requested by the attacker page.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

### am...@chromium.org (2025-02-18)

uploading the original information from this report since it was original reported with restrictions set

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/359949844)*
