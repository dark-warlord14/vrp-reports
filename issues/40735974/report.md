# Security:  IDN Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40735974](https://issues.chromium.org/issues/40735974) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2020-12-08 |
| **Bounty** | $500.00 |

## Description

Root cause:- This is IDN Spoofing using unicode character “კ” (U+10D9)  

**-------------------------**

**VERSION**  

Chrome Version: 86.0.4240.198 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 Pro x64

**REPRODUCTION CASE**  

<http://xn--16-1ik.com/>

**CREDIT INFORMATION**

Reporter credit: Kirtikumar Anandrao Ramchandani

## Attachments

- [idn_image.png](attachments/idn_image.png) (image/png, 2.9 KB)

## Timeline

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-08)

Thanks for your report. meacer@chromium.org can you take a look at this potential IDN spoof?

### wf...@chromium.org (2020-12-09)

[Empty comment from Monorail migration]

[Monorail components: UI>Security>UrlFormatting]

### wf...@chromium.org (2020-12-09)

[Empty comment from Monorail migration]

### ki...@gmail.com (2020-12-09)

Is this issue eligible for CVE or I will need to report other issues for it? 

### [Deleted User] (2020-12-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ki...@gmail.com (2021-01-29)

Friendly ping!


### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### ki...@gmail.com (2021-03-14)

Any update?

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ki...@gmail.com (2021-04-22)

This issue as well. Thanks!

### es...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-09)

Opening visibility for the upcoming FixIt. Please be aware that the information on this bug report may be sensitive.

### me...@chromium.org (2022-05-17)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-05-17)

Assigning to rezvan@ as a starter bug. We could potentially fix this by marking this character as a digit lookalike. See https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/spoof_checks/idn_spoof_checker.h;drc=05eaa06bcd62d80432d379ad2287abb690ffc112;l=205 as a starting point.

### [Deleted User] (2022-05-17)

[Empty comment from Monorail migration]

### re...@google.com (2022-05-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d1bf11591db26be629ab39d0f86cd3931dbc0e44

commit d1bf11591db26be629ab39d0f86cd3931dbc0e44
Author: Rezvan Mahdavi Hezaveh <rezvan@google.com>
Date: Sat May 28 01:48:48 2022

Fix IDN Spoofing with Georgian Letter Kan U+10D9

This cl:
* Marks the character კ as a digit lookalike.
Also, the skleton of it is mapped to 3. These allow the lookalike URL
checks to flag spoofs containing this character. So, the 16კ[.]com
is matched to 163[.]com,
* Adds a missing skeleton mapping for
gurmukhi letter rra (ੜ) to 3,
* Adds comments for IsDigitLookalike checks for clarification.

Bug: 1156531
Change-Id: I00aa13c6279e41738c1d4f116b0d415e973ff79f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3673677
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Chris Thompson <cthomp@chromium.org>
Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@google.com>
Cr-Commit-Position: refs/heads/main@{#1008524}

[modify] https://crrev.com/d1bf11591db26be629ab39d0f86cd3931dbc0e44/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc
[modify] https://crrev.com/d1bf11591db26be629ab39d0f86cd3931dbc0e44/components/url_formatter/spoof_checks/skeleton_generator.cc
[modify] https://crrev.com/d1bf11591db26be629ab39d0f86cd3931dbc0e44/components/url_formatter/spoof_checks/idn_spoof_checker.cc


### re...@google.com (2022-05-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations! The VRP Panel has decided to award you a $500 thank you for reporting this issue. While these types of issues are no longer considered to be security issues. We did, however, want to award you an appreciation reward for taking the time to report this and given that we were still considering this to be a low severity issue at the time of reporting. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### is...@google.com (2022-08-01)

This issue was migrated from crbug.com/chromium/1156531?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40735974)*
