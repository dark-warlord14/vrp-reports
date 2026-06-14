# Security: IDN URL Spoofing with U+02ec

| Field | Value |
|-------|-------|
| **Issue ID** | [40092758](https://issues.chromium.org/issues/40092758) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **Platforms** | Windows |
| **Reporter** | ev...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-10-18 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36

Steps to reproduce the problem:
### SPOOF CASE

(\u02ec) "ˬ" looks like an ".", it's not easy to catch the spoofing.

Real: https://accountsˬgoogle.com --- Spoof domain: https://xn--accountsgoogle-7uh.com

What is the expected behavior?

What went wrong?
IDNSPOOF

Did this work before? N/A 

Chrome version: 70.0.3538.67  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [ee082f5e46ac662229b55cb8770eea8.png](attachments/ee082f5e46ac662229b55cb8770eea8.png) (image/png, 2.3 KB)

## Timeline

### in...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### sh...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-30)

+tommycli for bug visibility. Patch at https://chromium-review.googlesource.com/c/chromium/src/+/1303037/

### bu...@chromium.org (2018-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4e4fec21ebd26d2ef20ac9f1ca0d2a16329f22bd

commit 4e4fec21ebd26d2ef20ac9f1ca0d2a16329f22bd
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Wed Oct 31 03:10:25 2018

Block modifier-letter-voicing character from domain names

This character (ˬ) is easy to miss between other characters. It's one of the three characters from Spacing-Modifier-Letters block that ICU lists in its recommended set in uspoof.cpp. Two of these characters (modifier-letter-turned-comma and modifier-letter-apostrophe) are already blocked in crbug/678812.

Bug: 896717
Change-Id: I24b2b591de8cc7822cd55aa005b15676be91175e
Reviewed-on: https://chromium-review.googlesource.com/c/1303037
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/master@{#604128}
[modify] https://crrev.com/4e4fec21ebd26d2ef20ac9f1ca0d2a16329f22bd/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/4e4fec21ebd26d2ef20ac9f1ca0d2a16329f22bd/components/url_formatter/url_formatter_unittest.cc


### me...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-05)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-11-05)

+awhalley@ (Security TPM) for M71 merge review.

### aw...@google.com (2018-11-05)

govind@ - good for 71

### go...@chromium.org (2018-11-05)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/896717#c12. Please merge ASAP. Thank you.

### cr...@appspot.gserviceaccount.com (2018-11-05)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/863175d508d607bfea907815f3e512d67af955a6

Commit: 863175d508d607bfea907815f3e512d67af955a6
Author: meacer@chromium.org
Commiter: meacer@chromium.org
Date: 2018-11-05 21:18:56 +0000 UTC

[Merge M-71] Block modifier-letter-voicing character from domain names

This character (ˬ) is easy to miss between other characters. It's one of the three characters from Spacing-Modifier-Letters block that ICU lists in its recommended set in uspoof.cpp. Two of these characters (modifier-letter-turned-comma and modifier-letter-apostrophe) are already blocked in crbug/678812.

TBR=meacer@chromium.org

(cherry picked from commit 4e4fec21ebd26d2ef20ac9f1ca0d2a16329f22bd)

Bug: 896717
Change-Id: I24b2b591de8cc7822cd55aa005b15676be91175e
Reviewed-on: https://chromium-review.googlesource.com/c/1303037
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#604128}
Reviewed-on: https://chromium-review.googlesource.com/c/1318544
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#524}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### bu...@chromium.org (2018-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/863175d508d607bfea907815f3e512d67af955a6

commit 863175d508d607bfea907815f3e512d67af955a6
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Mon Nov 05 21:18:56 2018

[Merge M-71] Block modifier-letter-voicing character from domain names

This character (ˬ) is easy to miss between other characters. It's one of the three characters from Spacing-Modifier-Letters block that ICU lists in its recommended set in uspoof.cpp. Two of these characters (modifier-letter-turned-comma and modifier-letter-apostrophe) are already blocked in crbug/678812.

TBR=meacer@chromium.org

(cherry picked from commit 4e4fec21ebd26d2ef20ac9f1ca0d2a16329f22bd)

Bug: 896717
Change-Id: I24b2b591de8cc7822cd55aa005b15676be91175e
Reviewed-on: https://chromium-review.googlesource.com/c/1303037
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#604128}
Reviewed-on: https://chromium-review.googlesource.com/c/1318544
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#524}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/863175d508d607bfea907815f3e512d67af955a6/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/863175d508d607bfea907815f3e512d67af955a6/components/url_formatter/url_formatter_unittest.cc


### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

$500 for this report, thanks evi1m0.bat@

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/896717?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092758)*
