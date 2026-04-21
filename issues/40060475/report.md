# Security: console.log still allows loading images via %c formatter

| Field | Value |
|-------|-------|
| **Issue ID** | [40060475](https://issues.chromium.org/issues/40060475) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2022-08-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

I noticed that the fix for <https://crbug.com/chromium/1223475> is imcomplete.  

An attacker can still load images via the console.log.

PoC #1:  

console.log("%caaa","background:url([httpS://attacker.example.com/](https://attacker.example.com/))")

PoC #2:  

console.log("%caaa","background:url(https\0009://attacker.example.com/)")

This is because the check is performed by String#includes().

**VERSION**  

106.0.5215.0（Official Build）canary

**CREDIT INFORMATION**  

Reporter credit: Masato Kinugawa

## Timeline

### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### ma...@google.com (2022-08-04)

Looking at https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3522264/4/front_end/panels/console/ConsoleFormat.ts, this seems plausible, and I can get it to work in DevTools console. (I.e. picking some random image URL, the image shows with "httpS://..." but not "https://").

Severity-Low to match the original issue.

FoundIn-101 based on CL:3522264

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy Platform>DevTools]

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### bm...@chromium.org (2022-08-04)

Simon, please take a look while jarin@ is out. This should be straight-forward to fix (maybe a matter of using a RegExp instead).

### gi...@appspot.gserviceaccount.com (2022-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/e9d28467f96044e6ffc6e521cf2378c4f7fae524

commit e9d28467f96044e6ffc6e521cf2378c4f7fae524
Author: Simon Zünd <szuend@chromium.org>
Date: Mon Aug 08 08:40:12 2022

[console] Block more urls in console.log %c formatter styles

This CL expands upon https://crrev.com/c/3522264 to prevent console.log
from triggering arbitray loads via CSS `url()` function.

Compared to the original CL we turn the scheme block list into an
allow list and only allow `data` URLs. That change makes it necessary
to iterate over all possible `url()`s and check them all.

The CL expands the corresponding test suite appropriately.

R=mathias@chromium.org

Fixed: 1349493
Change-Id: Iff3239513ad504194a52eeb17119d53a45d1a37c
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3810245
Reviewed-by: Mathias Bynens <mathias@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>

[modify] https://crrev.com/e9d28467f96044e6ffc6e521cf2378c4f7fae524/test/unittests/front_end/panels/console/ConsoleFormat_test.ts
[modify] https://crrev.com/e9d28467f96044e6ffc6e521cf2378c4f7fae524/front_end/panels/console/ConsoleFormat.ts


### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations, Masato! The VRP Panel has decided to award you $500 as a thank you reward for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### ja...@chromium.org (2022-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-12)

Raised https://crbug.com/chromium/1400224 for the fact this didn't make it into the release notes.

This was released in M106. Labelling thusly and ensuring we retroactively fix release notes.

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1349493?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Platform>DevTools]
[Monorail mergedwith: crbug.com/chromium/1375814]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060475)*
