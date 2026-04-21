# 'unsafe-inline' is not ignored even though 'strict-dynamic' is specified in dafault-src.

| Field | Value |
|-------|-------|
| **Issue ID** | [40059762](https://issues.chromium.org/issues/40059762) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Windows |
| **Reporter** | tj...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2022-05-26 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Access to the following page

<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="Content-Security-Policy" content="default-src 'unsafe-inline' 'strict-dynamic'">
</head>
<body>
<script>alert(1)</script>
</body>
</html>

2. We can observe that inline script is executed

**Problem Description:**  

According to the CSP spec for the usage of 'strict-dynamic' (<https://www.w3.org/TR/CSP3/#strict-dynamic-usage>), host-source and scheme-source expressions, as well as the 'unsafe-inline' and 'self' keyword-sources should be ignored when loading script if 'strict-dynamic' is specified in script-src or default-src.

I observed that:

1. When 'strict-dynamic' is specified in script-src, Chrome follows the spec.
2. When 'strict-dynamic' is specified in default-src, Chrome follows the spec by ignoring the following directive values: host-source, scheme-source, and 'self'.

However, I saw that Chrome does not ignore the 'unsafe-inline' even though 'strict-dynamic' is specified in default-src.

I know that the security risk of this bug is not serious since developers usually use 'strict-dynamic' and nonce/hash together. But very rarely, web developers unfamiliar with the CSP specification may specify 'strict-dynamic' 'unsafe-inline' to default-src, expecting 'unsafe-inline' to be ignored by CSP level 3-supported browsers, including Chrome.

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.5005.63 \*\*Channel: \*\* Stable

**OS:** Windows

## Timeline

### tj...@gmail.com (2022-05-26)

Oops...I think it was reported as a security-bug, but it is reported as a bug :( If you think there is a security implication for this report, please update it.

Thanks!

### dt...@chromium.org (2022-05-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### ah...@chromium.org (2022-05-30)

[OWP Security bug triage] Converting to a security bug to be conservative.

[Monorail components: -Blink>SecurityFeature Blink>SecurityFeature>ContentSecurityPolicy]

### [Deleted User] (2022-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-30)

[Empty comment from Monorail migration]

### ar...@chromium.org (2022-06-07)

I am not totally familiar with "strict-dynamic". However thanks to this great description of the problem (Thanks!), I am convinced this is indeed a bug.

We should definitively:
- Add a WPT to ensure every web browser converge toward the same "correct" behavior.
- Fix Chrome's behavior. It looks like “default-src” must be added inside IsScriptDirective. It is also possible to simplify CSPSourceListAllowAllInline after that.

I agree with reporter's statement about the low severity.

This bugs looks like a good opportunity to ramp up on Chrome. I will reassign it in the next few days.

### ar...@google.com (2022-06-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/02495a2c0b813fd89d2759482255d08f2b0643f8

commit 02495a2c0b813fd89d2759482255d08f2b0643f8
Author: Paul Semel <paulsemel@chromium.org>
Date: Thu Jun 23 08:32:00 2022

[CSP] default-src with 'strict-dynamic' must discard 'unsafe-inline'

As per https://www.w3.org/TR/CSP3/#strict-dynamic-usage, 'unsafe-inline'
is ignored when 'strict-dynamic' is used with 'script-src' or
'default-src' directives.

Bug: 1329460
Change-Id: I48cb4c4e221a8d7defaad8b08f4d094d5b18681b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714438
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1017073}

[modify] https://crrev.com/02495a2c0b813fd89d2759482255d08f2b0643f8/services/network/public/cpp/content_security_policy/csp_source_list_unittest.cc
[modify] https://crrev.com/02495a2c0b813fd89d2759482255d08f2b0643f8/services/network/public/cpp/content_security_policy/csp_source_list.cc
[modify] https://crrev.com/02495a2c0b813fd89d2759482255d08f2b0643f8/third_party/blink/renderer/core/frame/csp/content_security_policy.h
[modify] https://crrev.com/02495a2c0b813fd89d2759482255d08f2b0643f8/third_party/blink/renderer/core/frame/csp/source_list_directive.cc
[add] https://crrev.com/02495a2c0b813fd89d2759482255d08f2b0643f8/third_party/blink/web_tests/external/wpt/content-security-policy/default-src/default-src-strict_dynamic_and_unsafe_inline.html


### ar...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please provide the name/handle or other identifier you would like us to use when acknowledging you for this issue when the fix is released. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-09-29)

This issue was migrated from crbug.com/chromium/1329460?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059762)*
