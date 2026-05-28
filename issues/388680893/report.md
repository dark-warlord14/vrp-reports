# the autofill prompt obscured by permission prompt lead to spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [388680893](https://issues.chromium.org/issues/388680893) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Permissions>PermissionElement |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | tu...@google.com |
| **Created** | 2025-01-09 |
| **Bounty** | $500.00 |

## Description

redacted

## Attachments

- index6.js (text/javascript, 1.2 KB)
- [pxtm.html](attachments/pxtm.html) (text/html, 2.9 KB)
- bandicam 2025-01-09 15-01-06-539.mp4 (video/mp4, 2.5 MB)

## Timeline

### jd...@chromium.org (2025-01-09)

andypaicu@: would you mind taking a look at this? I don't think this is the most severe thing in the world, but I definitely agree that the focus is confusing. Thanks!

### pe...@google.com (2025-01-10)

Setting milestone because of s2 severity.

### pe...@google.com (2025-01-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2025-01-24)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ja...@chromium.org (2025-02-04)

[secondary shepherd]
Hi andypaicu, are you still a good owner for this issue? Could you take a look and leave a comment that explains any plans for addressing this issue?

Thanks!

### pe...@google.com (2025-02-08)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### tu...@google.com (2025-02-17)

The issue didn't show up on my Linux machine, but I still added a check to cancel the autofill if it overlaps with the prompt.

### sp...@google.com (2025-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
thank you reward for report of a low impact security UI issue with low potential for exploitability and user harm; since we were able to make a beneficial change here, we do want to acknowledge your efforts with a small reward


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-20)

Thank you for your efforts and reporting this issue to us.

### sa...@gmail.com (2025-02-20)

thank you amy..

### ch...@google.com (2025-05-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/388680893)*
