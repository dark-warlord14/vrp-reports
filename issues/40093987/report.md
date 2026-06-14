# Security:  Idn-spoof with using U+00F0 (ð)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093987](https://issues.chromium.org/issues/40093987) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2019-02-07 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 74.0.3694.0  

Operating System: All

**REPRODUCTION CASE**

U+00F0 "ð" looks like an "o".

Visit [https://myaccount.gðogle.com](https://myaccount.g%C3%B0ogle.com)

## Attachments

- [Screen Shot 2019-02-07 at 16.19.06.png](attachments/Screen Shot 2019-02-07 at 16.19.06.png) (image/png, 25.8 KB)

## Timeline

### do...@chromium.org (2019-02-08)

Doesn't much look like an "o" to me..... +meacer, WDYT?

[Monorail components: UI>Browser>Omnibox]

### mm...@chromium.org (2019-02-08)

Yes, it looks very different. meacer@, feel free to reopen.

### sh...@chromium.org (2019-05-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2019-10-25)

Reopened. We decided to address this at https://chromium-review.googlesource.com/c/chromium/src/+/1881344

I think this is low severity at best, adjusting labels.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9

commit 1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9
Author: meacer <meacer@chromium.org>
Date: Fri Oct 25 19:29:59 2019

Restrict Latin Small Letter Eth (U+00F0) to Icelandic domains

crrev.com/c/1879992 restricted Latin Small Letter Thorn to Icelandic
domains. This CL does the same for Eth (ð) as it can be confused with
the characters "o" and "d" in some fonts.

This change affects less than 10 real world domains with limited popularity.

Bug: 1017707, 929711
Change-Id: I037054530feb1d34e9243ef5da35cf431f3b80b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1881344
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#709580}

[modify] https://crrev.com/1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9/components/url_formatter/spoof_checks/idn_spoof_checker.h
[modify] https://crrev.com/1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc


### me...@chromium.org (2019-10-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-10-25)

+pabrai so that VRP panel does not miss this bug.

### sh...@chromium.org (2019-10-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-10)

This issue was migrated from crbug.com/chromium/929711?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093987)*
