# [Security] Tapjacking on payment request dialog using window alert

| Field | Value |
|-------|-------|
| **Issue ID** | [361611809](https://issues.chromium.org/issues/361611809) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Payments |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2024-08-23 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

I found a tapjacking vulnerability on payment request (android). When tapped once, the payment request continues to run even though the dialog is closed by user.

VERSION
Chrome Version 122.0.6170.3 (Official Build) dev (64-bit)
Operating System: Android 12

REPRODUCTION CASE

1. open https://thundering-unruly-windflower.glitch.me/payment.html
2  click on "buy button"
2. double tap on ok button

CREDIT INFORMATION

Reporter credit: Hafiizh (https://www.linkedin.com/in/hafiizh-7aa6bb31/)

## Attachments

- [video6214974538107588499.mp4](attachments/video6214974538107588499.mp4) (video/mp4, 6.4 MB)
- [payment.html](attachments/payment.html) (text/html, 16.2 KB)
- [video6273551694387221470.mp4](attachments/video6273551694387221470.mp4) (video/mp4, 3.1 MB)
- [2025_03_26_21_17_32.mp4](attachments/2025_03_26_21_17_32.mp4) (video/mp4, 11.2 MB)
- [2025_03_26_22_17_23.mp4](attachments/2025_03_26_22_17_23.mp4) (video/mp4, 12.2 MB)
- [2025_03_26_22_29_18.mp4](attachments/2025_03_26_22_29_18.mp4) (video/mp4, 9.9 MB)

## Timeline

### ar...@chromium.org (2024-08-23)

I observe we can stack the `window.alert` and the `payment flow` on Android. The alert is displayed on top contrary to Desktop.

`smcgruer@chromium.org` could you please help triage this bug?

We may want to detect when the payment flow is on "top", and add a clickjacking protection: a delay before we can interact with the surface.
We may also want to disable the payment flow when an alert is displayed.

This falls behind [I can hijack a user gesture and trick a user into accepting a permission or downloading a file - is this a security bug?](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#i-can-hijack-a-user-gesture-and-trick-a-user-into-accepting-a-permission-or-downloading-a-file-is-this-a-security-bug) as a low severity bug, given we need to trick the user into clicking multiple time on the button.

### sa...@gmail.com (2024-08-23)

it is affected on Chrome Version 130.0.6669.0 (Canary)

### pe...@google.com (2024-08-24)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2025-01-20)

hello any updates?

### ro...@google.com (2025-01-21)

No updates at this time. Thank you for checking in.

### sa...@gmail.com (2025-03-25)

redacted

### sa...@gmail.com (2025-03-26)

hello this bug is fixed and cannot be reproduced in version 135.0.7049.26 (Official Build). window.alert appears behind the payment prompt so tapjacking cannot be reproduced. can  you set this bug to fixed? thank you

### sm...@chromium.org (2025-03-26)

We have landed no changes that I'm aware of from the Payments side to fix this. It may have been fixed by incidental changes, but we should be sure of that (and preferably be sure that regression testing is in place) before we close this out.

The next step would be a bisection between known-bad and known-good revisions of Chrome. It looks like 135.0.7049.26 should be known-good based on sas.kunz@'s comment. Latest known-bad in this thread is 130.0.6669.0, but sas.kunz@ do you know if it still reproduced on newer versions than that? (e.g., on M131-M134). Thanks!

### sa...@gmail.com (2025-03-26)

II haven't tried it on version 131-134. Okay, I'll try that version.

### sa...@gmail.com (2025-03-26)

This is version 134. I cannot reproduced the bug

### sa...@gmail.com (2025-03-26)

This is version 132. I can reproduced the bug

### sa...@gmail.com (2025-03-26)

This is version 133. I cannot reproduced the bug

### sa...@gmail.com (2025-03-26)

This bug has already fixed in version 133.

Version 131 : still can reproduced the bug
Version  132 : still can reproduced the bug
Version 133 : cannot reproduced the bug (fixed)
Version 134 : cannot reproduced the bug

### sm...@chromium.org (2025-04-10)

Thank you for summarizing that! I finally found some time to do a bisect:

You are probably looking for a change made after 1387033 (known bad), but no later than 1387034 (first known good).
CHANGELOG URL:
<https://chromium.googlesource.com/chromium/src/+log/58802c145e5081488f412b6594fc30650e4c079b..124c1c22af90f2558e847d61cca8c703105972b7>
The script might not always return single CL as suspect as some perf builds might get missing due to failure.

The result is <https://chromium.googlesource.com/chromium/src/+/124c1c22af90f2558e847d61cca8c703105972b7>, which doesn't look like a deliberate security fix, so it seems like this might just be serendipitous. cc-ing the author of that change to confirm if they were attempting to fix a security issue or not.

In any case, we should figure out how to introduce a test here to avoid regressing the behavior in the future.

### sa...@gmail.com (2025-05-09)

Pinging friendly,..

any updates?

### sa...@gmail.com (2025-06-14)

hello any updates? because this bug already fixed..

### sm...@chromium.org (2025-06-20)

Apologies for the delay here. I would really have liked to introduce a regression test for this, but given how long its been and how we haven't gotten to that, I think it's reasonable to just close it Fixed by <https://chromium.googlesource.com/chromium/src/+/124c1c22af90f2558e847d61cca8c703105972b7>, even if that CL wasn't directly intended to fix this issue.

### ch...@google.com (2025-06-20)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-06-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI / web platform privilege escalation bug


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-26)

Congratulations! Thank you for reporting this issue to us.

### sa...@gmail.com (2025-06-26)

Thank you amy..

### ch...@google.com (2025-09-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@chromium.org (2025-10-23)

Hi - it is Chrome VRP policy and a requirement for receiving VRP payments that information about issues is made public and not unnecessarily restricted. Please unrestrict your attachments and comments.

### sa...@gmail.com (2025-10-23)

hi sorry i have unrestricted it thank you

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361611809)*
