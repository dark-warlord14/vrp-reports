# File Download Origin Spoof Using Long Subdomain

| Field | Value |
|-------|-------|
| **Issue ID** | [410960670](https://issues.chromium.org/issues/410960670) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | sh...@chromium.org |
| **Created** | 2025-04-16 |
| **Bounty** | $500.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)
- [spooflongdomain.jpeg](attachments/spooflongdomain.jpeg) (image/jpeg, 109.0 KB)
- [longdomain.jpg](attachments/longdomain.jpg) (image/jpeg, 44.7 KB)
- [longdomain.mp4](attachments/longdomain.mp4) (video/mp4, 3.1 MB)

## Timeline

### sa...@gmail.com (2025-04-16)

VULNERABILITY DETAILS
This vulnerability is the same as https://issues.chromium.org/issues/40058315 

What is the expected behavior?
The long subdomain should be shifted to the left side inside the download section of the browser so that the main domain can be seen clearly.

What went wrong?
Long subdomain is shifting the main domain to the right side of the browser which can be ab-used to mask the domain of the downloaded files.

Did this work before? N/A

VERSION 
Chrome Version: 137.0.7126.0 (canary)
Operating System: Android 12

REPRODUCTION CASE
1. open http://you-can-billowy-nimble-login-secure-docs-google-source-attacker.com/google.jpg
2. choose menu then  press icon download
3. open download menu, the domain is truncated

or you can use POC  https://issues.chromium.org/issues/40058315 

### dr...@chromium.org (2025-04-16)

[security triage] I can reproduce this on Android M135. It looks like the fix in <https://crrev.com/c/4706260> was incomplete, so assigning to the CL author.

### ch...@google.com (2025-04-17)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dr...@chromium.org (2025-04-29)

Sorry about the hotlist spam, this is being looked into: <https://crbug.com/414669497>. For now I've moved the FoundIn back to M134 so it should settle on Extended.

### dr...@chromium.org (2025-04-30)

The bot should be fixed now, so restoring the FoundIn

### sa...@gmail.com (2025-10-31)

hello this bug is fixed and cannot be reproduced in Version 144.0.7501.3 (Official Build) canary (64-bit). , URL is no longer in download history, Seems this bug is fixed in this CL: https://chromium-review.googlesource.com/c/chromium/src/+/6701188. Can you set this bug to fixed?

### dr...@chromium.org (2025-10-31)

Thank you. Marking fixed per reporter comments.

### wf...@chromium.org (2025-12-16)

Please do not delete comments on issues - even if they are later found to be incorrect you must leave them in place and you can correct them in later comments. Failure to comply with these instructions might cause you to be disqualified from the Chrome VRP program.

### sa...@gmail.com (2025-12-16)

Im sorry for my mistakes

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
limited impact security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/410960670)*
