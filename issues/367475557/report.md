# race condition on pip window lead to spoof address bar

| Field | Value |
|-------|-------|
| **Issue ID** | [367475557](https://issues.chromium.org/issues/367475557) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2024-09-17 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

I found a race condition vulnerability on pip window where when a page that opens pip window repeatedly and at the same time redirects to another page, the pip window should be closed but it doesn't and the url bar in pip window is the redirect address

VERSION
Chrome Version 130.0.6669.2 (Official Build) dev (64-bit)
Operating System: Windows 10

REPRODUCTION CASE

1. open https://thundering-unruly-windflower.glitch.me/paymentpip1.html or requestpaymentpip1.html on local web server
2. do many clicks on "do some clicks" button (fast click) until the page is redirected
3. click on pip window page

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If
this bug is included, how would you like to be credited?
Reporter credit: Hafiizh (https://www.linkedin.com/in/hafiizh-7aa6bb31/)

## Attachments

- [bandicam 2024-09-17 20-33-05-444.mp4](attachments/bandicam 2024-09-17 20-33-05-444.mp4) (video/mp4, 2.7 MB)
- [bandicam 2024-09-17 20-53-51-182.mp4](attachments/bandicam 2024-09-17 20-53-51-182.mp4) (video/mp4, 3.1 MB)
- [paymentpip1.html](attachments/paymentpip1.html) (text/html, 3.0 KB)
- [bandicam 2025-10-31 14-29-07-497.mp4](attachments/bandicam 2025-10-31 14-29-07-497.mp4) (video/mp4, 4.2 MB)

## Timeline

### ma...@google.com (2024-09-18)

I can't repro this on macOS; FoundIn and OS provisional based on original report.

liberato@, could you PTAL or help route this to a better owner if necessary? Thanks.

### pe...@google.com (2024-09-19)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2024-10-24)

hello any updates?

### sa...@gmail.com (2025-03-24)

Hello any updates?

### sa...@gmail.com (2025-10-31)

hello this bug is fixed and cannot be reproduced in Version 144.0.7503.0 (Official Build) canary (64-bit). After there are UI changes in the PIP window, this bug is fixed. Can you set this bug to fixed?

### ch...@google.com (2025-10-31)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sa...@gmail.com (2025-10-31)

Hi thank you, but the bot changed it again to assigned.

### sp...@google.com (2025-12-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Security UI Spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security UI Spoofing

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/367475557)*
