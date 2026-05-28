# permission prompt obscured by black screen lead to spoof to allow permission

| Field | Value |
|-------|-------|
| **Issue ID** | [400761079](https://issues.chromium.org/issues/400761079) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ra...@google.com |
| **Created** | 2025-03-04 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

when the payment prompt is called and at the same time the permission prompt is called the permission prompt moves behind the black screen (which should be above the black screen) so this can obscure the permission prompt causing a trick to allow the permission

VERSION
Chrome Version :  135.0.7049.0 (Official Build) canary (64-bit)
Operating System: Windows 11

REPRODUCTION CASE

1. open chrome: chrome.exe --enable-features=PermissionElement

2. open dev tools then do 
window.open("https://thundering-unruly-windflower.glitch.me/pypip1.html", "_blank", "toolbar=yes,scrollbars=yes,resizable=yes,top=50000,left=11111,width=310,height=1");

3. press enter tab tab and enter

CREDIT INFORMATION
Reporter credit: [goes here]

## Attachments

- [bandicam 2025-03-05 03-40-23-623.mp4](attachments/bandicam 2025-03-05 03-40-23-623.mp4) (video/mp4, 3.3 MB)
- [pypi.html](attachments/pypi.html) (text/html, 17.4 KB)
- [bandicam 2025-11-05 13-40-56-043.mp4](attachments/bandicam 2025-11-05 13-40-56-043.mp4) (video/mp4, 2.7 MB)

## Timeline

### pg...@google.com (2025-03-06)

Thanks for the report!

I am able to repro this on M134

Setting S3 for UI spoofing requiring specific gestures

### pg...@google.com (2025-03-06)

Elias, this looks very similar to [issue 387312215](https://issues.chromium.org/issues/387312215) (if not the same) - please take a look when you get a chance!

### ch...@google.com (2025-03-06)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2025-07-20)

hello any updates?

### tu...@google.com (2025-07-22)

I think it's a duplicate of 403273926 

### sa...@gmail.com (2025-07-22)

Hi thank you, bug 403273926 should be a duplicate of this bug because my report ID is smaller (400761079) (I reported it first compared to 403273926)

### sa...@gmail.com (2025-11-05)

hello this bug is fixed because i can't reproduce this bug on Version 144.0.7509.0 (Official Build) canary (64-bit). the permission prompt is shown above black screen.  Can you set this bug to fixed?

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
limited impact UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/400761079)*
