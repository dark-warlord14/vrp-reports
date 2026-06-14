#  Extension popup can render over FEDCM prompts

| Field | Value |
|-------|-------|
| **Issue ID** | [376497151](https://issues.chromium.org/issues/376497151) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2024-10-31 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
This vulnerability is almost the same as https://issues.chromium.org/issues/40058873 , https://issues.chromium.org/issues/361711121,
https://issues.chromium.org/issues/367771116,
https://issues.chromium.org/issues/359949844

but it occurs on FEDCM request prompt


VERSION
Chrome Version 132.0.6808.0 (Official Build) canary (64-bit)
Operating System: Windows 10

REPRODUCTION CASE

1. Install attached extension: manifest.json + bg-keyboard.js + popup.html.

2. Reload manifest-keyboard.json extension using chrome://extensions
Press Ctrl+A when requested by the attacker page.

3. Click the Web page then wait then Press Ctrl+A when requested by the attacker page.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [bandicam 2024-10-31 09-12-50-722.mp4](attachments/bandicam 2024-10-31 09-12-50-722.mp4) (video/mp4, 1.6 MB)
- [bg-keyboard.js](attachments/bg-keyboard.js) (text/javascript, 1.1 KB)
- [manifest.json](attachments/manifest.json) (application/json, 462 B)
- [popup.html](attachments/popup.html) (text/html, 2.3 KB)
- popup.html (text/html, 2.3 KB)
- [manifest (1).json](attachments/manifest (1).json) (application/json, 462 B)
- bg-keyboard.js (text/javascript, 1.1 KB)
- [bandicam 2024-10-31 09-12-50-722 (1).mp4](attachments/bandicam 2024-10-31 09-12-50-722 (1).mp4) (video/mp4, 1.6 MB)

## Timeline

### sr...@google.com (2024-10-31)

kerenzhu@, should this just be marked as duplicate of 367771116 or 359949844? It seems to have the same root cause.

### pe...@google.com (2024-10-31)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ke...@google.com (2024-10-31)

Stephen, yes they have the same cause. To prevent security dialogs from being occluded by the extension bubble they should be marked so using [extensions::SecurityDialogTracker](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/extensions/security_dialog_tracker.h;l=23?q=extensions::SecurityDialogTracker&sq=&ss=chromium).

I will leave these bugs separately open. Otherwise I anticipate that a general bug will be repeatedly re-open as new security dialogs are added.

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

### pe...@google.com (2024-11-08)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### ke...@chromium.org (2024-11-08)

This is not a regression and I think this is low-risk and therefore does not need branch merging.

### sp...@google.com (2024-11-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI spoofing issue


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-22)

Congratulations! Thank you for your efforts and reporting this issue to us.

### sa...@gmail.com (2024-11-22)

Awesome thank you amy

### ph...@google.com (2025-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2025-02-18)

re-uploading original report since original report was submitted under restricted settings

VULNERABILITY DETAILS
This vulnerability is almost the same as <https://issues.chromium.org/issues/40058873> , <https://issues.chromium.org/issues/361711121>,
<https://issues.chromium.org/issues/367771116>,
<https://issues.chromium.org/issues/359949844>

but it occurs on FEDCM request prompt

VERSION
Chrome Version 132.0.6808.0 (Official Build) canary (64-bit)
Operating System: Windows 10

REPRODUCTION CASE

1. Install attached extension: manifest.json + bg-keyboard.js + popup.html.
2. Reload manifest-keyboard.json extension using chrome://extensions
   Press Ctrl+A when requested by the attacker page.
3. Click the Web page then wait then Press Ctrl+A when requested by the attacker page.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/376497151)*
