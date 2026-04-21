# Android fullscreen notification is not shown when Chrome is in split-screen

| Field | Value |
|-------|-------|
| **Issue ID** | [373746918](https://issues.chromium.org/issues/373746918) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Fullscreen |
| **Platforms** | Android |
| **Reporter** | fa...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2024-10-16 |
| **Bounty** | $1,000.00 |

## Description

Security Bug
VULNERABILITY DETAILS
When the Chrome Android browser is open in split-screen mode after an app, activating fullscreen does not show the security fullscreen notification indicating that the user has switched to fullscreen. Therefore, this can be used for spoofing the address bar.

VERSION
Chrome Version: 132 + [stable, beta, or dev]
Operating System: Android 14

REPRODUCTION CASE
1. Open an app and then switch to split-screen view on Android.
2. Then, choose Chrome as the second split-screen view option.
3. Visit permission.site, click on the fullscreen button, and observe that no fullscreen notification is shown.

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 3.0 MB)
- [repro-fixed.mp4](attachments/repro-fixed.mp4) (video/mp4, 1.2 MB)

## Timeline

### fa...@gmail.com (2024-10-16)

Similar issue: <https://issues.chromium.org/issues/325419412>

### mp...@google.com (2024-10-16)

CC fjacky@ who worked on the similar bug. Since it is a Fullscreen bug I will assign to takumif@.

### ta...@chromium.org (2024-10-16)

Muyao, would you mind triaging?

### pe...@google.com (2024-10-17)

Setting milestone because of s2 severity.

### pe...@google.com (2024-10-17)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mu...@google.com (2024-10-17)

Setting priority to P2 to match priorities of other fullscreen toast issues.

### fa...@gmail.com (2025-01-21)

Friendly ping.

### fa...@gmail.com (2025-04-30)

Hi, it seems this issue is fixed — fullscreen toasts now properly show in split-screen view on the latest Android Chrome 135 version. Can we confirm this and close the issue as fixed if that's the case? Thank you!

### fa...@gmail.com (2025-12-13)

Hi — this seems to be fixed, so kindly close this issue as resolved. Thanks.

### aj...@chromium.org (2025-12-22)

Marking fixed as reporter claims it is fixed.

### sp...@google.com (2026-01-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Low impact UI spoofing with user gestures


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Low impact UI spoofing with user gestures

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/373746918)*
