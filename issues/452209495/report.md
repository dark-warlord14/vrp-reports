# truncated long domain on Digital Credentials API prompt lead to spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [452209495](https://issues.chromium.org/issues/452209495) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Payments |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2025-10-15 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

When the Digital Credentials API dialog is invoked, the dialog appears with the name "Do you trust this site with your data" and the long domain name causes the domain name to be truncated. As seen in the second video at
https://developer.chrome.com/blog/digital-credentials-api-shipped?hl=en . In the second video, the dialog appears to be "9000--firebase-studio-1758636784187.cluster-64pjnskmlbaxowh5lzq6i7v4ra.clo" instead of 9000--firebase-studio-1758636784187.cluster-64pjnskmlbaxowh5lzq6i7v4ra.cloudworkstations.dev, thus causing the dialog to be spoofed.

1. Create a Digital Credentials API application using the example at https://developer.chrome.com/blog/digital-credentials-api-shipped?hl=en using a long domain.
2. Open the page as shown on https://verifier.multipaz.org/ and click one of the button and show the confirm dialog



## Attachments

- [longdomaintruncated.png](attachments/longdomaintruncated.png) (image/png, 324.3 KB)

## Timeline

### el...@chromium.org (2025-10-15)

Security shepherd: thanks for the report. I have not reproduced this myself but from [code inspection](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/digital_credentials/digital_identity_safety_interstitial_controller_desktop.cc;l=109?q=IDS_WEB_DIGITAL_CREDENTIALS_INTERSTITIAL_HIGH_RISK_DIALOG_TEXT&ss=chromium) I can see that the bug is present - this code needs to use `ElideUrl` ([docs](https://chromium.googlesource.com/chromium/src/+/main/docs/security/url_display_guidelines/url_display_guidelines.md#Eliding-URLs)) when choosing how to display this URL.

Over to mamir@, and provisional Sev-2 / Pri-2 :)

### ch...@google.com (2025-10-16)

Setting milestone because of s2 severity.

### ch...@google.com (2025-10-29)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2025-10-30)

mamir: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ma...@chromium.org (2025-10-31)

[Fix CL](https://crrev.com/c/7083387) is in review

### dx...@google.com (2025-11-03)

Project: chromium/src  

Branch:  main  

Author:  Mohamed Amir Yosef [mamir@chromium.org](mailto:mamir@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7083387>

[DC] Elide the origin for display in the interstitial

---


Expand for full commit details
```
     
    This CL properly elides the origins to be displayed in the digital 
    credentials UIs. 
     
    More details are in the linked bug. 
     
    Bug: 452209495 
     
    Change-Id: Icdf97292f42b91c7911a0397c7f40ab0659f1b82 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7083387 
    Reviewed-by: Elly FJ <ellyjones@chromium.org> 
    Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1539496}

```

---

Files:

- M `chrome/browser/digital_credentials/digital_identity_provider_desktop.cc`
- M `chrome/browser/ui/views/digital_credentials/digital_identity_safety_interstitial_controller_desktop.cc`

---

Hash: [9f349d7e49bf8f162840ce82f3368fc81996ff16](https://chromiumdash.appspot.com/commit/9f349d7e49bf8f162840ce82f3368fc81996ff16)  

Date: Mon Nov 3 19:08:40 2025


---

### sp...@google.com (2025-11-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
low impact ui spoofing issue


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-01-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2026-01-30)

1. <https://crrev.com/c/7531220>
2. Low, there was a conflict and the fix wasn't applicable to one of the files.
3. 144-146
4. Yes

### an...@google.com (2026-02-03)

Merge approved for LTS-138

### ch...@google.com (2026-02-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2026-02-10)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Mohamed Amir Yosef [mamir@chromium.org](mailto:mamir@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7531220>

[M138-LTS][DC] Elide the origin for display in the interstitial

---


Expand for full commit details
```
     
    M138 merge issues: 
      chrome/browser/digital_credentials/digital_identity_provider_desktop.cc: 
      - In 138, DigitalIdentityProviderDesktop::ShowQrCodeDialog() uses only 
        one body ID, the switch to get the correct id doesn't exist and 
        caused the conflict. Also, the origin url isn't used to compose the 
        text. So the fix was skipped for this file. 
     
    This CL properly elides the origins to be displayed in the digital 
    credentials UIs. 
     
    More details are in the linked bug. 
     
    Bug: 452209495 
     
    (cherry picked from commit 9f349d7e49bf8f162840ce82f3368fc81996ff16) 
     
    Change-Id: Icdf97292f42b91c7911a0397c7f40ab0659f1b82 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7083387 
    Reviewed-by: Elly FJ <ellyjones@chromium.org> 
    Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1539496} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7531220 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3486} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `chrome/browser/ui/views/digital_credentials/digital_identity_safety_interstitial_controller_desktop.cc`

---

Hash: [b28df33d78847f7a951831d7acc25e4934aa587a](https://chromiumdash.appspot.com/commit/b28df33d78847f7a951831d7acc25e4934aa587a)  

Date: Tue Feb 10 20:31:48 2026


---

## Bounty Award

> low impact ui spoofing issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/452209495)*
