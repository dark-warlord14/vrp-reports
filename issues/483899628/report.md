# URL Spoofing on Block or allow pop-ups in Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [483899628](https://issues.chromium.org/issues/483899628) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Services (Use Subcomponents)>Safebrowsing |
| **Platforms** | Windows |
| **Chrome Version** | 145.0.7632.46 |
| **Reporter** | mu...@gmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2026-02-12 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Save this 2 HTML files (orig.html and fake.html) and analyze the link in the popup message, it looks the same
2. Allow the popup
3. The victim redirected to evil.com instead of google.com

# Problem Description

When using window.open, Chrome shows a popup listing temporarily blocked URLs and waits for the user’s approval. If a suspicious URL is detected, the user can choose to keep it blocked. However, in this popup Chrome displays only the URL’s prefix and suffix. By inserting a malicious URL in the middle using @, an attacker can disguise it. If the user allows the popup, instead of opening a safe website, Chrome will open the malicious URL.

# Summary

URL Spoofing on Block or allow pop-ups in Chrome

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [2026-02-13 00-34-36.mp4](attachments/2026-02-13 00-34-36.mp4) (video/mp4, 3.4 MB)
- [fake.html](attachments/fake.html) (text/html, 126 B)
- [orig.html](attachments/orig.html) (text/html, 103 B)

## Timeline

### ts...@google.com (2026-02-12)

Improper URL elision when URL contains an embedded auth username/password.

### dx...@google.com (2026-02-19)

Project: chromium/src  

Branch:  main  

Author:  Nathan Parker [nparker@chromium.org](mailto:nparker@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7577181>

Fix URL spoofing on "Pop-ups blocked" dialog in Chrome.

---


Expand for full commit details
```
     
    Switched to FormatUrl() which removes the username:password@ component. 
     
    Example of new formatting, with hover: http://screen/M4wV4PuQ4vu2zDr 
     
    Bug: 483899628 
    Change-Id: Iff473a1718f7f4662abddbeff29223973c7de845 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7577181 
    Reviewed-by: Ravjit Uppal <ravjit@chromium.org> 
    Commit-Queue: Nathan Parker <nparker@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1587161}

```

---

Files:

- M `chrome/browser/ui/content_settings/content_setting_bubble_model.cc`
- M `chrome/browser/ui/content_settings/content_setting_bubble_model_unittest.cc`

---

Hash: [848a7a9f1feeba1debc2abfc9b9b1b38ec2b28d1](https://chromiumdash.appspot.com/commit/848a7a9f1feeba1debc2abfc9b9b1b38ec2b28d1)  

Date: Thu Feb 19 16:18:27 2026


---

### mu...@gmail.com (2026-02-20)

Can we mark this as fixed?

### mu...@gmail.com (2026-02-20)

bounty?

### mu...@gmail.com (2026-03-05)

Hi, any update here? and I forgot to fill in the acknowledgment name in this report report. Could you please add `daffainfo` as the public acknowledgment? Thanks!

### mu...@gmail.com (2026-03-19)

Any update?

### ch...@google.com (2026-04-07)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline, Security UI Spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483899628)*
