# The extension popup can appear over the PWA install prompt

| Field | Value |
|-------|-------|
| **Issue ID** | [384068255](https://issues.chromium.org/issues/384068255) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Windows |
| **Chrome Version** | 133.0.6893.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2024-12-15 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

1. Install the attached extension
2. Click the web page then Press Ctrl+A

# Problem Description

The extension can display its popup over the PWA install prompt, allowing it to spoof parts of the prompt's UI, such as the origin. This could trick the victim into falling for a scam and installing a malicious extension.

This is similar to [issue 40058873](https://issues.chromium.org/issues/40058873)

# Summary

The extension popup can appear over the PWA install prompt

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [bg-keyboard.js](attachments/bg-keyboard.js) (text/javascript, 1.9 KB)
- [manifest.json](attachments/manifest.json) (application/json, 494 B)
- [popup.html](attachments/popup.html) (text/html, 2.1 KB)
- [screen-capture.webm](attachments/screen-capture.webm) (video/webm, 1.7 MB)
- [screen.webm](attachments/screen.webm) (video/webm, 2.1 MB)

## Timeline

### an...@chromium.org (2024-12-16)

[security shepherd]: Hi [msiem@google.com](mailto:msiem@google.com), similar to the [issue 382190924](https://issues.chromium.org/issues/382190924), triaging to you for any updates on this. Thanks!

### ch...@gmail.com (2024-12-16)

deleted

### pe...@google.com (2024-12-17)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@gmail.com (2025-01-28)

msiem@ frinedly ping. 

### ch...@gmail.com (2025-02-17)

This is similar to issue 359949844.

### ch...@gmail.com (2025-03-30)

This issue is fixed in issue 406023321, as seen in the fix at https://chromium-review.googlesource.com/q/I21817060ebfdb6fcc06698a5acf78e10e657e676.

Verified on Canary 136.0.7098.0 on Windows 10.

### aj...@chromium.org (2025-04-01)

(Fixed by CL attributed to later report in [issue 406023321](https://issues.chromium.org/issues/406023321))

### ch...@google.com (2025-04-01)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-04-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
report of lower impact security UI issue, with low potential for exploitability and low potential for user harm


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue, with low potential for exploitability and low potential for user harm

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/384068255)*
