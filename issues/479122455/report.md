# Mini bar not rendering when omnibox is hidden on Pixel 8 and 9

| Field | Value |
|-------|-------|
| **Issue ID** | [479122455](https://issues.chromium.org/issues/479122455) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Mobile>Toolbar |
| **Platforms** | Android |
| **Chrome Version** | 146.0.7651.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2026-01-27 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

[Issue 467448811](https://issues.chromium.org/issues/467448811) appears to be fixed on other devices, but I am still able to consistently reproduce the problem on Pixel 8 and Pixel 9.
I am not able to reproduce the issue on Pixel 7 or on Samsung devices using the same Chrome Canary build and reproduction steps.

1. Open the testcase.
2. Scroll down to the middle of the page until the omnibox disappears (normal fullscreen scroll behavior).
3. Tap inside the <textarea>.

# Problem Description

In Chrome Canary on Android, when the omnibox auto-hides during scroll, tapping inside a <textarea> causes the keyboard accessory bar (mini bar above the virtual keyboard) to fail to render. The layout space for the accessory bar is still reserved, but the UI is completely blank—no icons, background, or controls are visible.

This behavior was addressed in [issue 467448811](https://issues.chromium.org/issues/467448811) and no longer reproduces on several devices (e.g., Pixel 7 and Samsung devices). However, the problem is still consistently reproducible on Pixel 8 and Pixel 9, using the same Chrome Canary build and reproduction steps.

The blank UI region appears exactly where users expect browser controls to be displayed. This creates a potential UI spoofing risk, as a website could use CSS to position a fake omnibox or browser controls beneath the empty area, misleading users.

# Summary

Mini bar not rendering when omnibox is hidden on Pixel 8 and 9

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A \

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 3.3 KB)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 3.3 MB)

## Timeline

### el...@google.com (2026-01-27)

Security shepherd: thanks for the report! I don't have one of these devices to repro with, but the video looks convincing enough. I'm going to send this to the owner of 467448811 to look at :)

### ch...@google.com (2026-01-28)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@gmail.com (2026-02-19)

I have re-tested this issue on the previously affected devices (Pixel 8 and Pixel 9) using the current Chrome Canary version (146.0.7680.3) and am no longer able to reproduce the problem. It appears that the behavior has been addressed in recent changes.

### ch...@gmail.com (2026-03-11)

I believe this issue may have been fixed by the following change: https://chromium-review.googlesource.com/c/chromium/src/+/7560758

I also noticed that issue 482433856, which was reported after this one, appears to have been fixed by the same CL.

### ch...@gmail.com (2026-04-23)

Any update on the reward?

### sp...@google.com (2026-05-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Low impact. Security UI Spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@gmail.com (2026-06-12)

Dear Chrome VRP Panel,

Thank you for the reward on this report. I would like to respectfully request a reassessment based on the following inconsistency.

This report falls under the same vulnerability class (Security UI Spoofing, S3) as three other reports on the same surface, all rewarded during the same period:

- Issue 467448811: Mini bar blank when omnibox hidden → $2,000
- Issue 482433856: Mini bar color spoof on virtual keyboard → $2,000
- Issue 484082189: RTL omnibox truncation → $2,000

All three received $2,000 as the baseline reward for Security UI Spoofing at S3. This report was assessed at the same severity but received only $1,000 with the rationale "Low impact."

I would also note that this report demonstrated a device-specific bypass of the fix for Issue 467448811, proving the original fix was incomplete for Pixel 8 and Pixel 9. Finding a bypass of an already-patched vulnerability arguably warrants at least equal treatment to the original report.

I respectfully ask the panel to reconsider the reward in light of these comparable decisions.

Thank you for your time.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/479122455)*
